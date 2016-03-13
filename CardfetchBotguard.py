from CommentBuilder import CommentBuilder
import time
import praw
import Settings


class CardfetchBotguard(object):
    def __init__(self):
        user_agent = Settings.user_agent
        self.r = praw.Reddit(user_agent=user_agent)
        self.r.set_oauth_app_info(client_id=Settings.client_id, client_secret=Settings.client_secret,
                                  redirect_uri=Settings.redirect_uri)
        self.r.refresh_access_information(Settings.refresh_access_info)
        self.already_done = []
        self.subreddit = self.r.get_subreddit(Settings.subbredit)

        self.comment_builder = CommentBuilder()

    def run(self):
        for submission in self.subreddit.get_new(limit=10):
            if submission.id not in self.already_done:
                op_text = submission.selftext
                reply = self.comment_builder.build_comment(op_text)
                if reply is not None:
                    print(reply)
                    #        submission.add_comment(reply)
                self.already_done.append(submission.id)

        time.sleep(10)
