import pandas as pd
import praw
import os

from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

USER = os.getenv("USER_ID")
PASSWORD = os.getenv("PASSWORD")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")

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

    def posts__from_subreddit__since__limited_to(
        self, subreddit_name, time_filter="week", limit=10
    ):
        res = []

        print("Commencing post retrieval")
        for submission in tqdm(
            list(
                self.reddit.subreddit(subreddit_name).top(
                    time_filter=time_filter, limit=limit
                )
            ),
            desc="Processing",
        ):
            tickers = get_tickers(f"{submission.title}\n{submission.selftext}")
            if tickers:
                res.append(
                    [
                        (
                            "Unknown"
                            if submission.author is None
                            else submission.author.id
                        ),
                        (
                            "Unknown"
                            if submission.author is None
                            else submission.author.name
                        ),
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
                        submission.permalink,
                    ]
                )

        return res
