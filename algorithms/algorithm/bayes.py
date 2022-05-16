import matplotlib.pyplot as plt
import numpy as np
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import KFold
from tqdm import tqdm

from utilities.processing import data_preprocessing, split_data
from utilities.plot import plot_confusion_matrix, print_statistics


def run(df):
   LABEL = "Count Vectors MultinomialNB"
   # LABEL = "GaussianNB"
   df = data_preprocessing(df)
   y_tests = np.empty([0], dtype=int)
   y_predictions = np.empty([0], dtype=int)

   kfold = KFold(n_splits=10, random_state=42, shuffle=True)
   for train, test in tqdm(kfold.split(df), total=kfold.get_n_splits(), desc="K-Fold"):
      x_train, y_train, x_test, y_test = tokenize(df.iloc[train], df.iloc[test])
      model = MultinomialNB()
      model.fit(x_train, y_train)
      y_tests =  np.append(y_tests, y_test, axis=0)
      y_predictions = np.append(y_predictions, model.predict(x_test), axis=0)
    
   print_statistics(y_tests, y_predictions)
   plot_confusion_matrix(y_tests, y_predictions, LABEL)
   plt.show()


def tokenize(train_df, test_df):
   # vectorizing data, i.e., converting text to numbers
   # vectorizer = CountVectorizer(stop_words="english")
   vectorizer = CountVectorizer()
   # vectorizer = TfidfVectorizer(stop_words="english")
   # vectorizer = TfidfVectorizer()
   x_train = vectorizer.fit_transform(train_df.text).toarray()
   x_test = vectorizer.transform(test_df.text).toarray()
   y_train = train_df.sentiment
   y_test = test_df.sentiment
   return x_train, y_train, x_test, y_test


"""
CountVectorize()
Accuracy-score: 0.7099273607748184
Class-report:
              precision    recall  f1-score   support

           0       0.71      0.71      0.71      2065
           1       0.71      0.71      0.71      2065

    accuracy                           0.71      4130
   macro avg       0.71      0.71      0.71      4130
weighted avg       0.71      0.71      0.71      4130

F1-score: 0.7097868217054263

TfidfVectorizer()
Accuracy-score: 0.7033898305084746
Class-report:
              precision    recall  f1-score   support

           0       0.79      0.55      0.65      2065
           1       0.66      0.86      0.74      2065

    accuracy                           0.70      4130
   macro avg       0.72      0.70      0.70      4130
weighted avg       0.72      0.70      0.70      4130

F1-score: 0.7429171038824764
"""
