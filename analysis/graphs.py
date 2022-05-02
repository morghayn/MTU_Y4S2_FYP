import analysis
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime
import numpy as np

MONTHS = [
    "21-Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
    "22-Jan",
    "Feb",
    "Mar",
    "Apr",
]


def top_x_mentioned_tickers(number):
    """
    here we will be plotting the top 15 most mentioned tickers from the s&p 500
    x axis = ticker name
    y axis = mentions
    """
    fig, ax = plt.figure(), plt.subplot(111)
    tickers, mentions = analysis.get_top_x_mentioned_tickers(number)
    df = pd.DataFrame(list(zip(tickers, mentions)), columns=["Tickers", "Mentions"])

    sns.barplot(x="Tickers", y="Mentions", data=df, palette="winter", ax=ax)
    ax.set_title(f"Top {number} Tickers Mentioned")


def spy_price_movement_with_reddit_sentiment():
    """
    Here we will have a bar chart consisting of the monthly price changes (as %) of spy
    we will then overlay a line showing the sentiment observed
    """
    fig, ax = plt.figure(), plt.subplot(111)
    monthly_sentiment = analysis.get_average_sentiment_each_month_for_spy()
    monthly_price_change = (
        analysis.get_monthly_price_change_ticker_from_yahoo_finance_api(
            "SPY",
            int(datetime(2021, 4, 1).timestamp()),
            int(datetime(2022, 5, 1).timestamp()),
        )
    )

    # Plotting negative price changes
    negative_price_changes = [0 if i > 0 else i for i in monthly_price_change]
    ax.bar(MONTHS, negative_price_changes, width=1, color="r")

    # Plotting positive price changes
    positive_price_changes = [0 if i < 0 else i for i in monthly_price_change]
    ax.bar(MONTHS, positive_price_changes, width=1, color="g")

    # Plotting Reddit sentiment
    amplifier = abs(max(monthly_price_change, key=abs))
    monthly_sentiment_amplified = [i * amplifier for i in monthly_sentiment]
    ax.plot(monthly_sentiment_amplified, color="b", label="sentiment")

    # Making final adjustments to plot...
    ax.legend(loc="lower left")
    ax.set_xticks(MONTHS)
    ax.set_ylabel("Price Change in %")
    ax.set_xlabel("Month")
    ax.set_title("S&P500 Price Movement with Reddit Sentiment")


def _price_movement_with_reddit_sentiment(ticker):
    """
    Here we will have a bar chart consisting of the monthly price changes (as %) of spy
    we will then overlay a line showing the sentiment observed
    """
    fig, ax = plt.figure(), plt.subplot(111)
    monthly_sentiment = (
        analysis.get_average_sentiment_for_unknown_ticker_for_period_before_after(
            f"{ticker}"
        )
    )
    monthly_price_change = (
        analysis.get_monthly_price_change_ticker_from_yahoo_finance_api(
            f"{ticker}",
            int(datetime(2021, 4, 1).timestamp()),
            int(datetime(2022, 5, 1).timestamp()),
        )
    )

    # Plotting negative price changes
    negative_price_changes = [0 if i > 0 else i for i in monthly_price_change]
    ax.bar(MONTHS, negative_price_changes, width=1, color="r")

    # Plotting positive price changes
    positive_price_changes = [0 if i < 0 else i for i in monthly_price_change]
    ax.bar(MONTHS, positive_price_changes, width=1, color="g")

    # Plotting Reddit sentiment
    amplifier = abs(max(monthly_price_change, key=abs))
    monthly_sentiment_amplified = [i * amplifier for i in monthly_sentiment]
    ax.plot(monthly_sentiment_amplified, color="b", label="sentiment")

    # Making final adjustments to plot...
    ax.legend()
    ax.set_xticks(MONTHS)
    ax.set_ylabel("Price Change in %")
    ax.set_xlabel("Month")
    ax.set_title(f"{ticker} Price Movement with Reddit Sentiment")


def our_dataset():
    X = ["r/wallstreetbets", "r/stockmarket", "r/stocks"]
    retrieved = [405444, 37347, 63349]
    selected = [4158, 1645, 4615]


def graphs():
    sns.set_style("whitegrid")
    sns.set_context("poster")

    # top_x_mentioned_tickers(17)
    # spy_price_movement_with_reddit_sentiment()
    # _price_movement_with_reddit_sentiment("AWK")
    t, f = analysis.get_top_x_mentioned_tickers(75)
    for i, ticker in enumerate(t):
        print(f"{ticker}\t{f[i]}")

    _price_movement_with_reddit_sentiment("TSLA")
    _price_movement_with_reddit_sentiment("AAPL")
    _price_movement_with_reddit_sentiment("AMZN")
    _price_movement_with_reddit_sentiment("MSFT")
    _price_movement_with_reddit_sentiment("TWTR")
    _price_movement_with_reddit_sentiment("ALL")
    plt.show()


graphs()