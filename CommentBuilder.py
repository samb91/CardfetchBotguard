from CardFetcher import CardFetcher
import re

SIG_SEP = " ^^| "
SIG_HOWTO = "^^Call ^^me ^^with ^^[[card ^^name]] ^^or ^^by ^^linking ^^to ^^a ^^card ^^on [^^the ^^wiki](http://cardfight.wikia.com)^^!"
SIG_PM_SUB = "&subject=Problem+with+/u/CardfetchBotguard"
SIG_PM_BODY = "&message=Please+include+a+link+to+the+comment!"
SIG_PM = "[^^Did ^^I ^^get ^^something ^^wrong?](http://www.reddit.com/message/compose/?to=swabl" + SIG_PM_SUB + SIG_PM_BODY + ")"
SIG_SRC = "[^^src](https://github.com/swabl/CardfetchBotguard)"
SIGNATURE = SIG_HOWTO + SIG_SEP + SIG_PM + SIG_SEP + SIG_SRC

class CommentBuilder:
    def __init__(self):
        self.bracket_pattern = re.compile("\[\[([^\[\]]*)\]\]")
        self.url_pattern = re.compile("(?<!\w)cardfight.wikia.com/wiki/[^/\s\(\)]+(?:\([^/\s\(\)]+\))?")
        self.card_fetcher = CardFetcher()

    def remove_duplicates(self, name_list):
        seen = set()
        seen_add = seen.add
        return [x for x in name_list if not (x in seen or seen_add(x))]

    def build_comment(self, parent_text):
        found_bracket_patterns = self.bracket_pattern.findall(parent_text)
        found_url_patterns = self.url_pattern.findall(parent_text)
        found_patterns = self.remove_duplicates(found_url_patterns + found_bracket_patterns)
        if len(found_patterns) > 0:
            reply = ""
            for card in found_patterns:
                reply += self.card_fetcher.fetch_card(card) + "***\n\n"
            reply += SIGNATURE
            return reply
        return None
