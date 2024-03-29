import multiprocessing
import pandas as pd
import prawcore
import praw
import os

from tqdm.contrib.concurrent import process_map
from multiprocessing import Manager
from dotenv import load_dotenv
from datetime import datetime
from psaw import PushshiftAPI

load_dotenv()

USER = os.getenv("USER_ID")
PASSWORD = os.getenv("PASSWORD")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")

SUBREDDITS = [
    "stocks",
    "stockmarket",
    "wallstreetbets",
]

df = pd.read_csv("s&p-500.csv")


def get_tickers(text):
    text = text.split()
    tickers = list()
    for i, company in df.iterrows():
        name = company["Name"]
        ticker = company["Symbol"]

        if name in text or ticker in text:
            tickers.append(ticker)

    return tickers


class Reddit:
    def __init__(self) -> None:
        self.reddit = praw.Reddit(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            username=USER,
            password=PASSWORD,
            user_agent=USER_AGENT,
        )

        self.api = PushshiftAPI(self.reddit)

    def psaw_retrieval(self, subreddit_name, after, before, limit):
        after_str = datetime.fromtimestamp(after).strftime("%Y-%m-%d")
        before_str = datetime.fromtimestamp(before).strftime("%Y-%m-%d")
        now = datetime.now().strftime("%H:%M:%S")
        print(
            f"\n{now} | Retrieving posts from r/{subreddit_name} between {after_str} to {before_str}, have patience"
        )
        res = list(
            self.api.search_submissions(
                after=after,
                before=before,
                subreddit=subreddit_name,
                filter=["url", "author", "title"],
                limit=limit,
            )
        )
        now = datetime.now().strftime("%H:%M:%S")
        print(f"{now} | Retrieved {len(res)} posts, will begin processing\n")
        return res

    def pack_submission(self, submission, tickers):
        res = []
        url = f"https://www.reddit.com/r/{submission.subreddit.display_name}/comments/{submission.id}"

        try:
            res = [
                ("Unknown" if submission.author is None else submission.author.id),
                ("Unknown" if submission.author is None else submission.author.name),
                submission.subreddit.id,
                submission.subreddit.display_name,
                submission.id,
                submission.created_utc,
                submission.name,
                submission.title,
                ",".join([str(x) for x in tickers]),
                submission.selftext,
                submission.upvote_ratio,
                submission.score,
                submission.num_comments,
                submission.edited,
                submission.stickied,
                submission.locked,
                submission.over_18,
                submission.spoiler,
                url,
            ]
        except prawcore.NotFound:
            pass
        finally:
            return res

    def process_submission(self, submission):
        # skipping posts that are empty, or are just an image, or have been removed, or delete
        if (
            not submission.selftext
            or submission.selftext == "[removed]"
            or submission.selftext == "[deleted]"
        ):
            return

        tickers = get_tickers(f"{submission.title}\n{submission.selftext}")
        if tickers:
            res = self.pack_submission(submission, tickers)

            # if no errors occurred...
            if res:
                self.posts.append(res)

    def posts__from_subreddit(
        self, subreddit_name, after, before=int(datetime.now().timestamp()), limit=None
    ):
        manager = Manager()
        self.posts = manager.list()
        posts = self.psaw_retrieval(subreddit_name, after, before, limit)

        cpu_count = multiprocessing.cpu_count()
        process_map(self.process_submission, posts, max_workers=cpu_count, chunksize=1)

        posts = list(self.posts)
        return posts
