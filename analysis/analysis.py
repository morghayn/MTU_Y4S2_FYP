import database
import pandas as pd

from datetime import datetime

ANNOTATOR_ID = 3


def count_unannotated_per_month(subreddit):
    """
    counts number of unannotated posts pulled per month
    """
    db = database.Connection()
    year = 2021
    months = [4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5]

    for i, month in enumerate(months):
        # if last item in list break
        if i == len(months) - 1:
            break

        after = int(datetime(year, month, 1).timestamp())

        # increment on new year
        if months[i + 1] == 1:
            year += 1

        before = int(datetime(year, months[i + 1], 1).timestamp())
        count = db.count_unannotated(after, before, subreddit)

        print(f"After: {after}\tBefore: {before}\tCount: {count}")


def get_monthly_price_change_ticker_from_yahoo_finance_api(ticker, start, end):
    interval = "1mo"
    query_string = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={start}&period2={end}&interval={interval}&events=history&includeAdjustedClose=true"

    df = pd.read_csv(query_string)

    changes = []
    for index, row in df.iterrows():
        open = row["Open"]
        close = row["Close"]
        change = ((close - open) / open) * 100
        changes.append(change)

    changes.pop()
    return changes


def get_top_x_mentioned_tickers(number):
    db = database.Connection()
    ticker_lists = db.get_all_ticker_lists()
    # print(ticker_lists)
    res = {}
    for ticker_list in ticker_lists:
        # splitting single tuple value
        tickers = ticker_list[0].split(",")
        for ticker in tickers:
            if ticker in res:
                res[ticker] += 1
            else:
                res[ticker] = 1

    res = {k: v for k, v in sorted(res.items(), key=lambda item: item[1], reverse=True)}

    t = []
    f = []
    for i, (key, value) in enumerate(res.items()):
        if i == number:
            break
        else:
            t.append(key)
            f.append(value)

    return t, f


def get_average_sentiment_each_month_for_spy():
    """
    gets average sentiment for each month for past year spy
    """
    db = database.Connection()
    year = 2021
    months = [4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5]

    average_sentiments = []
    for i, month in enumerate(months):
        annotator_id = ANNOTATOR_ID  # babbage for now...
        # if last item in list break
        if i == len(months) - 1:
            break

        after = int(datetime(year, month, 1).timestamp())

        if months[i + 1] == 1:
            year += 1

        before = int(datetime(year, months[i + 1], 1).timestamp())
        average_sentiment_for_month = db.get_spys_average_sentiment_for_month(
            annotator_id, before, after
        )
        average_sentiments.append(average_sentiment_for_month)
    return average_sentiments


def get_average_sentiment_for_unknown_ticker_for_period_before_after(ticker):
    """
    gets average sentiment for each month for past year spy
    """
    db = database.Connection()
    year = 2021
    months = [4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5]

    average_sentiments = []
    for i, month in enumerate(months):
        annotator_id = ANNOTATOR_ID
        if i == len(months) - 1:
            break

        after = int(datetime(year, month, 1).timestamp())
        if months[i + 1] == 1:
            year += 1

        before = int(datetime(year, months[i + 1], 1).timestamp())
        average_sentiment_for_month = (
            db.get_average_sentiment_for_unknown_ticker_for_period_before_after(
                annotator_id, before, after, ticker
            )
        )
        average_sentiments.append(average_sentiment_for_month)
    return average_sentiments
