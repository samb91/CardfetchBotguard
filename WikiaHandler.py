import re
import requests
import difflib
from pyquery import PyQuery

API_URL = "http://cardfight.wikia.com/api/v1"


class WikiaHandler:
    def __init__(self):
        self.url_pattern = re.compile("^cardfight\.wikia.com/wiki/[^/\s]*$")
        # Pattern used to truncate an img url to everything up to and including the extension
        self.img_ext_pattern = re.compile(".*\.(png|jpg|jpeg|gif)")
        # Pattern used to extract trigger effect from trigger img url
        # File takes format of "Tr_[type].gif". This captures [type]
        self.trigger_pattern = re.compile("(?<=Tr_)([a-z]*)")

    def get_card_info_by_name(self, name):
        try:
            # Build API search query
            search_query = "/Search/List?query="
            res_lim = "&limit=5"
            results = requests.get(API_URL + search_query + name + res_lim)
            titles = [item['title'] for item in results.json()['items']]
            # Get closest matching title, with 85% confidence cutoff
            closest = difflib.get_close_matches(name, titles, 1, 0.85)[0]
            # Get the URL corresponding to the closest title, get the info from the URL's HTML
            for item in results.json()['items']:
                if item['title'] == closest:
                    return self.get_card_info_by_url(item['url'])
            # If we don't have a confident match, return None
            return None

        except:
            return None

    def get_card_info_by_url(self, url):
        # Get the page, PyQuery-ify it for parsing
        html = requests.get(url)
        page = PyQuery(html.text)

        # div class that contains all the card info
        cftable = page('.cftable')
        img = cftable('.image').attr['href']

        # Image URLs by default have revision after the extension. Strip it.
        m = re.search(self.img_ext_pattern, img)
        if m:
            img = m.group(0)

        # Initial dict with info we already have
        card_info = {'Url': url, 'Img': img}

        # Card attributes
        info_table = cftable.find('.info-main')

        # Iterate through table, storing 1st entry in table row in dict as key, and second as value
        for tr in info_table('tr').items():
            td_items = tr('td').items()

            info_list = []

            handle_trigger = False
            for i in td_items:
                text = i.text()
                # Trigger effects are not text-only friendly, so we have to handle them manually
                if handle_trigger:
                    m = re.search(self.trigger_pattern, i.html())
                    if m:
                        info_list.append(m.group(0).capitalize())
                        continue
                if text == "Trigger effect":
                    handle_trigger = True

                info_list.append(text)

            #info_list = [i.text() for i in td_items]
            if len(info_list) == 2:
                card_info[info_list[0]] = info_list[1]

        # Card effects
        effect_table = cftable.find('.info-extra').find('.effect')
        for tr in effect_table('tr').items():
            # Want to keep the html for formatting
            effect_list = [i.html() for i in tr('td').items()]
            if len(effect_list) == 1:
                card_info['Effect'] = effect_list[0]

        return card_info
