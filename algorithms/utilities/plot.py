from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    classification_report,
    f1_score,
)

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def set_style():
    sns.set_style("whitegrid")
    sns.set_context("poster")


def print_statistics(y_test, y_predictions):
    a_score = accuracy_score(y_test, y_predictions)
    clas_rep = classification_report(y_test, y_predictions)
    f1_sc = f1_score(y_test, y_predictions)

    print(f"Accuracy-score: {a_score}")
    print(f"Class-report: \n{clas_rep}")
    print(f"F1-score: {f1_sc}")


def plot_confusion_matrix(y_true, y_predictions, label, two_classes=True):
    set_style()
    matrix = confusion_matrix(y_true=y_true, y_pred=y_predictions)
    fig, ax = plt.figure(), plt.subplot(111)

    if two_classes:
        group_names = [
            "TN",
            "FN",
            "FP",
            "TP",
        ]
    else:
        group_names = ["", "", "", "", "", "", "", "", ""]

    group_counts = ["{0:0.0f}".format(value) for value in matrix.flatten()]
    group_percentages = [
        "{0:.2%}".format(value) for value in matrix.flatten() / np.sum(matrix)
    ]
    labels = [
        f"{v1}\n{v2}\n{v3}"
        for v1, v2, v3 in zip(group_names, group_counts, group_percentages)
    ]
    
    if two_classes:
        labels = np.asarray(labels).reshape(2, 2)
    else:
        labels = np.asarray(labels).reshape(3, 3)

    ax.set_title(f"{label} Confusion Matrix")
    ax = sns.heatmap(matrix, annot=labels, fmt="", cmap="Blues")

    if two_classes:
        ax.xaxis.set_ticklabels(["bearish", "bullish"])
        ax.yaxis.set_ticklabels(["bearish", "bullish"])
    else:
        ax.xaxis.set_ticklabels(["bearish", "neutral", "bullish"])
        ax.yaxis.set_ticklabels(["bearish", "neutral", "bullish"])


"""
Model Training History
"""


def plot_model_history(history, label):
    training_accuracy = history["accuracy"]
    validation_accuracy = history["val_accuracy"]
    training_loss = history["loss"]
    validation_loss = history["val_loss"]
    epochs = range(len(training_accuracy))

    plot_training_and_validation(label, epochs, training_accuracy, validation_accuracy)
    plot_training_and_validation_loss(label, epochs, training_loss, validation_loss)


def plot_training_and_validation(label, epochs, training_accuracy, validation_accuracy):
    set_style()
    fig, ax = plt.figure(), plt.subplot(111)
    ax.plot(epochs, training_accuracy, label="Training Accuracy", color="blue")
    ax.plot(epochs, validation_accuracy, label="Validation Accuracy", color="red")
    ax.legend()
    ax.set_title(f"{label} Training and Validation Accuracy")
    ax.set_ylabel("Accuracy")
    ax.set_xlabel("Epoch #")


def plot_training_and_validation_loss(label, epochs, training_loss, validation_loss):
    set_style()
    fig, ax = plt.figure(), plt.subplot(111)
    ax.plot(epochs, training_loss, label="Training Loss", color="blue")
    ax.plot(epochs, validation_loss, label="Validation Loss", color="red")
    ax.legend()
    ax.set_title(f"{label} Training and Validation Loss")
    ax.set_ylabel("Loss")
    ax.set_xlabel("Epoch #")
