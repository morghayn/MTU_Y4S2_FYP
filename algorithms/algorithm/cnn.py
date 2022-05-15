import tensorflow as tf
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers import Dense, Flatten, Embedding, Dropout
from keras.layers.convolutional import Conv1D, MaxPooling1D
from keras.layers.embeddings import Embedding
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder

from utilities.processing import data_preprocessing, split_data
from utilities.plot import plot_model_history, plot_confusion_matrix, print_statistics

LENGTH = 1024

def run(df):
    initialize(df)

def initialize(df):
    """
    Constants
    """
    LABEL = "CNN"
    # EPOCHS = 15
    # BATCH_SIZE = 8
    # LEARNING_RATE = 1e-4
    # EPOCHS = 16
    EPOCHS = 12
    BATCH_SIZE = 16
    LEARNING_RATE = 1e-4
    # EPOCHS = 60
    # BATCH_SIZE = 32
    # LEARNING_RATE = 1e-5

    """
    Preparing data
    """

    df = data_preprocessing(df)
    train, test = split_data(df, stratisfy=True)
    x_train, y_train, x_test, y_test, vocab_size = tokenize(train, test)

    """
    Encoding the Categorical target into 0 and 1
    """

    labelencoder = LabelEncoder()
    y_train = labelencoder.fit_transform(y_train)
    y_test = labelencoder.fit_transform(y_test)

    """
    Build Model using LSTM
    """

    model = Sequential()
    model.add(Embedding(vocab_size, 32, input_length=LENGTH))
    model.add(Dropout(0.2))
    model.add(Conv1D(32, 3, padding="same", activation="relu"))
    model.add(MaxPooling1D())
    model.add(Flatten())
    # model.add(Dropout(0.5))
    # model.add(Dense(250, activation="relu"))
    # model.add(Dropout(0.5))
    model.add(Dense(1, activation="sigmoid"))

    """
    Compile model
    """

    # model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
    model.compile(
        loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
        optimizer=tf.keras.optimizers.Adam(LEARNING_RATE),
        metrics=["accuracy"],
    )
    model.summary()

    """
    Fit model
    """

    model_history = model.fit(
        x_train,
        y_train,
        batch_size=BATCH_SIZE,
        epochs=EPOCHS,
        validation_split=0.2,
    )

    model.save("models/cnn")

    """
    Metrics
    """

    # print("Evaluate on test data")
    # results = model.evaluate(X_test, y_test, batch_size=4)
    # print("test loss, test acc:", results)

    # Predicting and creating confusion matrix using testing data
    predictions = model.predict(x_test)
    y_predictions = predictions > 0.5

    # Plotting
    print_statistics(y_test, y_predictions)
    plot_confusion_matrix(y_test, y_predictions, LABEL)
    plot_model_history(model_history.history, LABEL)
    plt.show()


def tokenize(train_df, test_df):
    """
    Tokenizing
    """
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(train_df.text)

    vocab_size = len(tokenizer.word_index) + 1
    print("Vocab size:", vocab_size)

    x_train = pad_sequences(tokenizer.texts_to_sequences(train_df.text), maxlen=LENGTH)
    x_test = pad_sequences(tokenizer.texts_to_sequences(test_df.text), maxlen=LENGTH)
    y_train = train_df.sentiment
    y_test = test_df.sentiment
    return x_train, y_train, x_test, y_test, vocab_size


"""
Accuracy-score: 0.7094430992736077
Class-report:
              precision    recall  f1-score   support

           0       0.71      0.71      0.71       413
           1       0.71      0.71      0.71       413

    accuracy                           0.71       826
   macro avg       0.71      0.71      0.71       826
weighted avg       0.71      0.71      0.71       826

F1-score: 0.70873786407767
"""