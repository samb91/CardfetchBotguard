import re
from WikiaHandler import WikiaHandler


class CardFetcher:
    def __init__(self):
        self.url_pattern = re.compile("^cardfight\.wikia.com/wiki/[^/\s]*$")
        self.wikia_handler = WikiaHandler()

    def upper_char(self, m):
        return m.group(1) + m.group(2).upper()

    def lower_char(self, m):
        return m.group(1) + m.group(2).lower()

    def get_card_by_url(self, url):
        if not url.startswith("http://"):
            url = "http://" + url

        return url

    def correct_name(self, name):
        # First, uppercase the first letter in each word
        correct_name = re.sub("(^|\s)(?!of)(\S)", self.upper_char, name)
        # Need to find a better regex so I don't have to do this just to handle " and (
        correct_name = re.sub("(^|\"|\()(\S)", self.upper_char, correct_name)

        # Lower any characters following a hyphen
        correct_name = re.sub("(\-)(\S)", self.lower_char, correct_name)

        # In the case of Reverse/Re-birth, sub in backwards R
        correct_name = correct_name.replace("Reverse", "Яeverse")
        correct_name = correct_name.replace("Re-birth", "Яe-birth")

        return correct_name

    def get_url_by_name(self, name):
        url_name = self.correct_name(name)
        print(self.wikia_handler.get_url_from_name(url_name))
        # Replace all spaces with underscores
        url_name = url_name.replace(" ", "_")

        url = "http://cardfight.wikia.com/wiki/" + url_name

        return self.get_card_by_url(url)

    def fetch_card(self, card_name: str):
        # If we've got a URL, just use that
        if re.match(self.url_pattern, card_name):
            assert isinstance(card_name, str)
            return self.get_card_by_url(card_name)

        # We're using a name, so use it to try and construct the URL
        card_text = self.get_url_by_name(card_name)
        return card_text
