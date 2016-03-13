import re
import requests
import difflib
from pyquery import PyQuery

API_URL = "http://cardfight.wikia.com/api/v1"


class WikiaHandler:
    def __init__(self):
        self.url_pattern = re.compile("^cardfight\.wikia.com/wiki/[^/\s]*$")

    def get_card_info_by_name(self, name):
        results = None
        try:
            search_query = "/Search/List?query="
            res_lim = "&limit=5"
            results = requests.get(API_URL + search_query + name + res_lim)
            titles = [item['title'] for item in results.json()['items']]
            print(titles)
            closest = difflib.get_close_matches(name, titles, 1, 0.85)[0]

            for item in results.json()['items']:
                if item['title'] == closest:
                    return self.get_card_info_by_url(item['url'])

            return None

        except:
            return None

    def get_card_info_by_url(self, url):
        html = requests.get(url)
        page = PyQuery(html.text)
        cftable = page('.cftable')
        card_info = {'Url': url}
        # Card attributes
        info_table = cftable.find('.info-main')
        for tr in info_table('tr').items():
            info_list = [i.text() for i in tr('td').items()]
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
