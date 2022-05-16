import re
import nltk
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split


def data_preprocessing(df, drop_neutral=True, balance_classes=True):
    """
    Data Pre-processing
    """
    # creating new dataframe with specific columns
    df = df[["title", "text", "sentiment"]].copy()

    # appending title as start of text cells and then dropping title column from df
    df.text = df.title.astype(str) + "\n" + df.text
    df = df.drop(columns=["title"])

    if drop_neutral:
        # Dropping neutral row....
        df.drop(df.loc[df["sentiment"] == 0].index, inplace=True)
        df.reset_index(drop=True, inplace=True)

    # # Relabeling -1 Negative label to 0, This has no effect on result
    df["sentiment"].replace({-1: 0}, inplace=True)

    # nltk.download('stopwords')
    stop_words = set(stopwords.words("english"))

    corpus = []
    for i in range(0, len(df)):
        review = re.sub("@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+", " ", df.text[i])
        review = review.lower()
        review = review.split()
        review = [word for word in review if not word in stop_words]
        review = " ".join(review)
        corpus.append(review)
    df.text = corpus

    if balance_classes:
        # Dropping the additional positive features (positive - negative features)
        # Due to unfairness
        positive_length = len(df.loc[df.sentiment == 1])
        negative_length = len(df.loc[df.sentiment == 0])
        skew = positive_length - negative_length
        df.drop(
            df.loc[df.sentiment == 1][:skew].index,
            inplace=True,
        )
        df.reset_index(drop=True, inplace=True)

    return df


def split_data(df, random_state=42, stratisfy=False, test_size=0.2):
    if stratisfy:
        train_df, test_df = train_test_split(
            df, test_size=test_size, stratify=df.sentiment, random_state=random_state
        )
    else:
        train_df, test_df = train_test_split(
            df, test_size=test_size, random_state=random_state
        )

    return train_df, test_df
