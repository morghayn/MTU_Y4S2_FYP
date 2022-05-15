import matplotlib.pyplot as plt
import numpy as np

from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from utilities.processing import data_preprocessing, split_data
from utilities.plot import plot_confusion_matrix, print_statistics
from sklearn.model_selection import KFold
from tqdm import tqdm


def run(df):
    LABEL = "RBF SVM"

    df = data_preprocessing(df)
    y_tests = np.empty([0], dtype=int)
    y_predictions = np.empty([0], dtype=int)

    kfold = KFold(n_splits=5, random_state=42, shuffle=True)
    for train, test in tqdm(kfold.split(df)):
        x_train, y_train, x_test, y_test = tokenize(df.iloc[train], df.iloc[test])
        # model = svm.SVC(kernel='linear')
        model = svm.SVC(kernel="rbf")
        model.fit(x_train, y_train)
        y_tests =  np.append(y_tests, y_test, axis=0)
        y_predictions = np.append(y_predictions, model.predict(x_test), axis=0)

    # Plotting
    print_statistics(y_tests, y_predictions)
    plot_confusion_matrix(y_tests, y_predictions, LABEL)
    plt.show()


def tokenize(train_df, test_df):
    # vectorizing data, i.e., converting text to numbers
    # vectorizer = CountVectorizer(stop_words="english")
    # vectorizer = TfidfVectorizer(stop_words="english")
    vectorizer = TfidfVectorizer()
    # vectorizer = CountVectorizer()
    x_train = vectorizer.fit_transform(train_df.text).toarray()
    x_test = vectorizer.transform(test_df.text).toarray()
    y_train = train_df.sentiment
    y_test = test_df.sentiment
    return x_train, y_train, x_test, y_test


"""
RBF TfidfVectorizer()
Accuracy-score: 0.7523114355231143
Class-report:
              precision    recall  f1-score   support

           0       0.76      0.74      0.75      2055
           1       0.74      0.77      0.76      2055

    accuracy                           0.75      4110
   macro avg       0.75      0.75      0.75      4110
weighted avg       0.75      0.75      0.75      4110

F1-score: 0.7564593301435407


Linear TfidfVectorizer()
Accuracy-score: 0.7322033898305085
Class-report:
              precision    recall  f1-score   support

           0       0.74      0.72      0.73      2065
           1       0.73      0.74      0.74      2065

    accuracy                           0.73      4130
   macro avg       0.73      0.73      0.73      4130
weighted avg       0.73      0.73      0.73      4130

F1-score: 0.7355332376853181
"""
