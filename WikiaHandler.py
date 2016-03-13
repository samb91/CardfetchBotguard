import requests
import difflib


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