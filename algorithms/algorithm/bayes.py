import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split


def run(df):
    x, x_test, y, y_test = transform(df)
    model = MultinomialNB()

    model.fit(x, y)
    score = model.score(x_test, y_test)
    print(score)


def transform(df):
    # creating new dataframe with specific columns
    df = df[["title", "text", "sentiment"]]

    # appending title as start of text cells and then dropping title column from df
    df = df.assign(text=(df["title"] + " " + df["text"]))

    # converting all text to lower case
    df = df.applymap(lambda s: s.lower() if type(s) == str else s)

    # splitting dataset
    x = df["text"]
    y = df["sentiment"]
    x, x_test, y, y_test = train_test_split(
        x, y, stratify=y, test_size=0.25, random_state=42
    )

    # vectorizing data, i.e., converting text to numbers
    vectorizer = CountVectorizer(stop_words="english")
    # vectorizer = TfidfVectorizer(stop_words="english")
    # vectorizer = CountVectorizer()
    x = vectorizer.fit_transform(x).toarray()
    x_test = vectorizer.transform(x_test).toarray()
    print("x_test", x)

    return x, x_test, y, y_test
