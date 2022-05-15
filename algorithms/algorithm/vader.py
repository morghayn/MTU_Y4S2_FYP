import random
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# For confusion matrix plot
# from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


from sklearn.metrics import classification_report

from utilities.plot import plot_confusion_matrix, print_statistics

def run(df):
    LABEL = "VADER"
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

    """
    a positive sentiment, compound ≥ 0.05
    a negative sentiment, compound ≤ -0.05
    a neutral sentiment, the compound is between ]-0.05, 0.05[
    """
    y = []
    y_prediction = []
    for index, row in df.iterrows():
        sentiment_dict = sid_obj.polarity_scores(row.title + row.text)

        prediction = -1
        if sentiment_dict['compound'] >= 0.05:
            prediction = 1
        elif sentiment_dict['compound'] <= -0.05:
            prediction = -1
        else:
            prediction = 0
        
        y.append(row.sentiment)
        y_prediction.append(prediction)
    
    clas_rep = classification_report(y, y_prediction)
    print(f"Class-report: \n{clas_rep}")
    plot_confusion_matrix(y, y_prediction, LABEL, two_classes=False)
    plt.show()


"""
Class-report:
              precision    recall  f1-score   support

          -1       0.62      0.29      0.40      2065
           0       0.19      0.02      0.03       898
           1       0.54      0.90      0.68      2970

    accuracy                           0.55      5933
   macro avg       0.45      0.40      0.37      5933
weighted avg       0.52      0.55      0.48      5933
"""