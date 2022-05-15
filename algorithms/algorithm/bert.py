from transformers import BertTokenizer, TFBertForSequenceClassification
from transformers import InputExample, InputFeatures
from sklearn.model_selection import train_test_split
import tensorflow as tf
import pandas as pd
import re
import torch
import pandas as pd
from tqdm import tqdm
from transformers import pipeline

# Load and tokenizing data...
from transformers import BertTokenizer
from torch.utils.data import TensorDataset

# BERT pre-trained
from transformers import BertForSequenceClassification

# Creating data loaders
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler

# Setting Up Optimisers and Scheduler
from transformers import AdamW, get_linear_schedule_with_warmup

# Defining our Performance Metrics
import numpy as np
from sklearn.metrics import f1_score

# Creating our Training Loop
import random


import matplotlib.pyplot as plt
from transformers.pipelines.text_classification import TextClassificationPipeline

# For confusion matrix plot
# from sklearn.metrics import confusion_matrix
import pandas as pd
import numpy as np
from sklearn.metrics import (
    f1_score,
)

from nltk.corpus import stopwords
from .graphing import graph_and_stats

LENGTH = 256


def run(df):
    """
    Warning: I do not take credit for this code, I closely followed a tutorial developing this.
    I do not take ownership of this BERT implementation.

    Closely followed along this tutorial:
    https://www.youtube.com/watch?v=hinZO--TEk4&t=2873s
    """
    INIT = False
    if INIT:
        init(df)
    else:
        load(df)


def load(df):
    df = data_preprocessing(df)

    # Counting labels
    possible_labels = df.sentiment.unique()
    label_dict = {}
    for index, possible_label in enumerate(possible_labels):
        label_dict[possible_label] = index
    print(f"Label count: {len(label_dict)}")  # Should be two without neutral

    model = BertForSequenceClassification.from_pretrained(
        "bert-base-uncased",
        num_labels=2,
        output_attentions=False,
        output_hidden_states=False,
    )
    X_train, X_val, y_train, y_val = train_test_split(
        df.index.values,
        df.sentiment.values,
        test_size=0.1,
        # random_state=17,
        random_state=65,
        stratify=df.sentiment.values,
    )
    df.loc[X_train, "data_type"] = "train"
    df.loc[X_val, "data_type"] = "val"

    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased", do_lower_case=True)

    model.load_state_dict(torch.load("finetuned_BERT_epoch_3.model"))
    model.eval()

    pipe = TextClassificationPipeline(
        model=model,
        tokenizer=tokenizer,
        return_all_scores=True,
    )
    # pipe = TextClassificationPipeline(model=model, return_all_scores=True)

    test_df = df.loc[(df.data_type == "val")].reset_index(drop=True)
    tokenizer_kwargs = {
        "padding": True,
        "truncation": True,
        "max_length": LENGTH,
    }  # ,'return_tensors':'pt'}
    x_test = test_df["text"].tolist()
    y_test = test_df["sentiment"].tolist()

    p = pipe(x_test, **tokenizer_kwargs)
    y_pred = get_predictions(p)
    graph_and_stats(y_test, y_pred, "BERT")
    plt.show()


def get_predictions(p):
    res = []
    for pred in p:
        negative = pred[0]
        positive = pred[1]

        if negative["score"] < positive["score"]:
            res.append(1)
        else:
            res.append(0)
    return res


def init(df):
    df = data_preprocessing(df)

    # Counting labels
    possible_labels = df.sentiment.unique()
    label_dict = {}
    for index, possible_label in enumerate(possible_labels):
        label_dict[possible_label] = index
    print(f"Label count: {len(label_dict)}")  # Should be two without neutral

    X_train, X_val, y_train, y_val = train_test_split(
        df.index.values,
        df.sentiment.values,
        test_size=0.15,
        random_state=17,
        stratify=df.sentiment.values,
    )
    df.loc[X_train, "data_type"] = "train"
    df.loc[X_val, "data_type"] = "val"
    # print(df)
    # return
    """
    Loading Tokenizer and Encoding our Data
    """

    # model = TFBertForSequenceClassification.from_pretrained("bert-base-uncased")
    # tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased", do_lower_case=True)
    # model.summary()

    encoded_data_train = tokenizer.batch_encode_plus(
        df[df.data_type == "train"].text.values,
        add_special_tokens=True,
        return_attention_mask=True,
        # pad_to_max_length=True,  # deprecetated
        # padding=True,
        # padding='max_length',
        padding=True,
        truncation=True,
        max_length=LENGTH,
        return_tensors="pt",
    )

    encoded_data_val = tokenizer.batch_encode_plus(
        df[df.data_type == "val"].text.values,
        add_special_tokens=True,
        return_attention_mask=True,
        # pad_to_max_length=True,  # deprecetated
        # padding=True,
        # padding='max_length',
        padding=True,
        truncation=True,
        max_length=LENGTH,
        return_tensors="pt",
    )
    # return

    input_ids_train = encoded_data_train["input_ids"]
    attention_masks_train = encoded_data_train["attention_mask"]
    labels_train = torch.tensor(df[df.data_type == "train"].sentiment.values)

    input_ids_val = encoded_data_val["input_ids"]
    attention_masks_val = encoded_data_val["attention_mask"]
    labels_val = torch.tensor(df[df.data_type == "val"].sentiment.values)

    dataset_train = TensorDataset(input_ids_train, attention_masks_train, labels_train)
    dataset_val = TensorDataset(input_ids_val, attention_masks_val, labels_val)
    print(len(dataset_train))
    print(len(dataset_val))
    # return

    """
    Setting up BERT Pretrained Model
    """

    model = BertForSequenceClassification.from_pretrained(
        "bert-base-uncased",
        num_labels=len(label_dict),
        output_attentions=False,
        output_hidden_states=False,
    )

    """
    Creating Data Loaders
    """

    batch_size = 32

    dataloader_train = DataLoader(
        dataset_train, sampler=RandomSampler(dataset_train), batch_size=batch_size
    )

    dataloader_validation = DataLoader(
        dataset_val, sampler=SequentialSampler(dataset_val), batch_size=batch_size
    )

    # Setting Up Optimiser and Scheduler

    optimizer = AdamW(model.parameters(), lr=1e-5, eps=1e-8)
    epochs = 3

    scheduler = get_linear_schedule_with_warmup(
        optimizer, num_warmup_steps=0, num_training_steps=len(dataloader_train) * epochs
    )

    """
    Defining our Performance Metrics
    """

    def f1_score_func(preds, labels):
        preds_flat = np.argmax(preds, axis=1).flatten()
        labels_flat = labels.flatten()
        return f1_score(labels_flat, preds_flat, average="weighted")

    def accuracy_per_class(preds, labels):
        label_dict_inverse = {v: k for k, v in label_dict.items()}

        preds_flat = np.argmax(preds, axis=1).flatten()
        labels_flat = labels.flatten()

        for label in np.unique(labels_flat):
            y_preds = preds_flat[labels_flat == label]
            y_true = labels_flat[labels_flat == label]
            print(f"Class: {label_dict_inverse[label]}")
            print(f"Accuracy: {len(y_preds[y_preds==label])}/{len(y_true)}\n")

    """
    Creating our Training Loop
    """
    seed_val = 17  # Importance?
    random.seed(seed_val)
    np.random.seed(seed_val)
    torch.manual_seed(seed_val)
    torch.cuda.manual_seed_all(seed_val)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    print(device)

    def evaluate(dataloader_val):

        model.eval()

        loss_val_total = 0
        predictions, true_vals = [], []

        for batch in dataloader_val:
            batch = tuple(b.to(device) for b in batch)
            inputs = {
                "input_ids": batch[0],
                "attention_mask": batch[1],
                "labels": batch[2],
            }

            with torch.no_grad():
                outputs = model(**inputs)

            loss = outputs[0]
            logits = outputs[1]
            loss_val_total += loss.item()

            logits = logits.detach().cpu().numpy()
            label_ids = inputs["labels"].cpu().numpy()
            predictions.append(logits)
            true_vals.append(label_ids)

        loss_val_avg = loss_val_total / len(dataloader_val)

        predictions = np.concatenate(predictions, axis=0)
        true_vals = np.concatenate(true_vals, axis=0)

        return loss_val_avg, predictions, true_vals

    """
    Training
    """

    for epoch in tqdm(range(1, epochs + 1)):

        model.train()

        loss_train_total = 0

        progress_bar = tqdm(
            dataloader_train,
            desc="Epoch {:1d}".format(epoch),
            leave=False,
            disable=False,
        )
        for batch in progress_bar:

            model.zero_grad()

            batch = tuple(b.to(device) for b in batch)

            inputs = {
                "input_ids": batch[0],
                "attention_mask": batch[1],
                "labels": batch[2],
            }

            outputs = model(**inputs)

            loss = outputs[0]
            loss_train_total += loss.item()
            loss.backward()
            # loss.backward(create_graph=True)

            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

            optimizer.step()
            scheduler.step()

            progress_bar.set_postfix(
                {"training_loss": "{:.3f}".format(loss.item() / len(batch))}
            )

        torch.save(model.state_dict(), f"finetuned_BERT_epoch_{epoch}.model")

        tqdm.write(f"\nEpoch {epoch}")

        loss_train_avg = loss_train_total / len(dataloader_train)
        tqdm.write(f"Training loss: {loss_train_avg}")

        val_loss, predictions, true_vals = evaluate(dataloader_validation)
        val_f1 = f1_score_func(predictions, true_vals)
        tqdm.write(f"Validation loss: {val_loss}")
        tqdm.write(f"F1 Score (Weighted): {val_f1}")


def data_preprocessing(df, drop_neutral=True):
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

    return df


"""
Epoch 1
Training loss: 0.6133673236601882
Validation loss: 0.5366526979666489
F1 Score (Weighted): 0.7565988202564079


accuracy score: 0.769041769041769
class report:
              precision    recall  f1-score   support

           0       0.81      0.60      0.69       173
           1       0.75      0.89      0.82       234

    accuracy                           0.77       407
   macro avg       0.78      0.75      0.75       407
weighted avg       0.77      0.77      0.76       407

f1 score: 0.81640625

Epoch 3
class report:
              precision    recall  f1-score   support

           0       0.69      0.72      0.71       173
           1       0.79      0.76      0.78       234

    accuracy                           0.75       407
   macro avg       0.74      0.74      0.74       407
weighted avg       0.75      0.75      0.75       407

f1 score: 0.7765726681127982
"""
