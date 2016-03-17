from CardFetcher import CardFetcher
import re


class CommentBuilder:
    def __init__(self):
        self.bracket_pattern = re.compile("\[\[([^\[\]]*)\]\]")
        self.url_pattern = re.compile("(?:http[s]?://(?:www.)?|www.)?(cardfight.wikia.com/wiki/[^/\s]*)+")
        self.card_fetcher = CardFetcher()

    def remove_duplicates(self, name_list):
        seen = set()
        seen_add = seen.add
        return [x for x in name_list if not (x in seen or seen_add(x))]

    def build_comment(self, parent_text):
        reply = None
        found_bracket_patterns = self.bracket_pattern.findall(parent_text)
        found_url_patterns = self.url_pattern.findall(parent_text)
        found_patterns = self.remove_duplicates(found_url_patterns + found_bracket_patterns)
        if len(found_patterns) > 0:
            reply = " "
            for card in found_patterns:
                reply += self.card_fetcher.fetch_card(card)
            #    print(card)
            return reply

