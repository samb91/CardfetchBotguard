from CommentBuilder import CommentBuilder
import time
import praw
import Settings


# Process submissions every 5 minutes
SUBMISSIONS_INTERVAL = 300

class CardfetchBotguard(object):
    def __init__(self):
        user_agent = Settings.user_agent
        self.r = praw.Reddit(user_agent=user_agent)
        self.r.set_oauth_app_info(client_id=Settings.client_id, client_secret=Settings.client_secret,
                                  redirect_uri=Settings.redirect_uri)
        self.r.refresh_access_information(Settings.refresh_access_info)
        self.subreddit = self.r.get_subreddit(Settings.subbredit)

        self.submissions_already_done = []
        self.last_submissions_time = 0

        self.comments_already_done = []

        self.comment_builder = CommentBuilder()

    def run(self):
        comments = praw.helpers.comment_stream(self.r, self.subreddit, limit=1000, verbosity=0)
        for comment in comments:

            if (time.time() - self.last_submissions_time) > SUBMISSIONS_INTERVAL:
                self.process_submissions()
                self.last_submissions_time = time.time()

            if comment.id in self.comments_already_done:
                continue

            try:
                author = comment.author.name
            except Exception:
                self.comments_already_done.append(comment.id)
                continue

            if author == "CardfetchBotguard":
                self.comments_already_done.append(comment.id)
                continue

            reply = self.comment_builder.build_comment(comment.body)
            if reply is not None:
                comment.reply(reply)

            self.comments_already_done.append(comment.id)

    def process_submissions(self):
        for submission in self.subreddit.get_new(limit=100):
            if submission.id not in self.submissions_already_done:
                if submission.author.name is not "CardfetchBotguard":
                    op_text = submission.url if "cardfight.wikia.com" in submission.url else submission.selftext
                    reply = self.comment_builder.build_comment(op_text)
                    if reply is not None:
                        submission.add_comment(reply)
                    self.submissions_already_done.append(submission.id)