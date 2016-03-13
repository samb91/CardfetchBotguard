import requests
import difflib
from pyquery import PyQuery
from collections import defaultdict

API_URL = "http://cardfight.wikia.com/api/v1"


class WikiaHandler:
    def get_url_from_name(self, name):
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
                    return item['url']

            return None
        except:
            return None

    def get_card_info(self, url):
        html = requests.get(url)
        page = PyQuery(html.text)
        cftable = page('.cftable')
        info_table = cftable.find('.info-main')
        card_info = defaultdict(dict)
        for tr in info_table('tr').items():
            info_list = [i.text() for i in tr('td').items()]
            if len(info_list) == 2:
                card_info[info_list[0]] = info_list[1]
                print(card_info)

        return card_info
