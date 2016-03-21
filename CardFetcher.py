import re
from WikiaHandler import WikiaHandler

WIKIA_BASE_URL = "http://cardfight.wikia.com"


class CardFetcher:
    def __init__(self):
        self.url_pattern = re.compile("^cardfight\.wikia.com/wiki/[^/\s]*$")
        self.a_pattern = re.compile("(<a[^>]*>[^<]*</a>)")
        self.a_href_pattern = re.compile("(?<=<a href=\")[^\"]*")
        self.a_body_pattern = re.compile("(?<=>)[^<]*(?=</a>)")
        self.wikia_handler = WikiaHandler()

    def get_card_by_url(self, url):
        if not url.startswith("http://"):
            url = "http://" + url
        return self.wikia_handler.get_card_info_by_url(url)

    def a_to_reddit_link(self, text):
        match = re.findall(self.a_pattern, text)
        for m in match:
            link = re.search(self.a_href_pattern, m).group(0)
            body = re.search(self.a_body_pattern, m).group(0)
            reddit_link = "[" + body + "](" + WIKIA_BASE_URL + link + ")"
            text = text.replace(m, reddit_link)
        return text

    def escape_url(self, url):
        url = url.replace("(", "\(")
        url = url.replace(")", "\)")
        return url

    def format_effect(self, effect):
        effect = effect.strip()
        effect = effect.replace("<br>", "\n\n")
        effect = effect.replace("<br/>", "\n\n")
        effect = effect.replace("<b>", "**")
        effect = effect.replace("</b>", "**")
        effect = effect.replace("<i>", "*")
        effect = effect.replace("</i>", "*")
        # Escape some markdown. No idea what it's for, or why it doesn't effect EVERY instance, but this is invisible
        effect = effect.replace("]:", "]\:")
        effect = self.a_to_reddit_link(effect)
        return effect

    def format_card(self, card_info):
        if card_info is not None:
            effect = None
            if 'Effect' in card_info:
                effect = self.format_effect(card_info['Effect'])

            shield = ""
            if 'Shield' in card_info:
                shield = " / Shield " + card_info['Shield']

            url = self.escape_url(card_info['Url'])

            name = "[" + card_info['Name'] + "](" + card_info['Img'] + ")"
            wikia = "- [wikia](" + url + ")"
            unit_type = card_info['Unit Type']
            if unit_type == "Trigger Unit":
                unit_type = unit_type + " (" + card_info['Trigger effect'] + ")"
            # We just want "Grade x", not the skill (can be derived from grade)
            grade = card_info['Grade / Skill'][:7]

            card_text = (name + " " + wikia + "\n\n" +
                         grade + " / " + unit_type + "\n\n" +
                         "Power " + card_info['Power'] + shield + "\n\n" +
                         card_info['Clan'] + " / " + card_info['Race']
                         )

            if effect is not None:
                card_text = card_text + "\n\n" + effect

            card_text += "\n\n"
            return card_text
        return None

    def fetch_card(self, card_name: str):
        if re.match(self.url_pattern, card_name):
            # If we've got a URL, just use that
            card_info = self.get_card_by_url(card_name)
        else:
            # Else, we just use the name
            card_info = self.wikia_handler.get_card_info_by_name(card_name)

        return self.format_card(card_info)
