import re
from keras.preprocessing.text import Tokenizer
import gensim
from keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from keras.layers import Embedding
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Bidirectional
# from tensorflow import CuDNNLSTM
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from keras.models import load_model
import tensorflow as tf

from tqdm import tqdm

from utilities.processing import data_preprocessing, split_data
from utilities.plot import plot_model_history, plot_confusion_matrix, print_statistics

LENGTH = 512


def now_str():
    return datetime.now().strftime("%H:%M:%S")


def run(df):
    INIT = True
    if INIT:
        init(df)
    else:
        text = """
        Advanced Micro Devices Q1 Adj. EPS $1.13 Beats $0.91 Estimate, Sales $5.89B Beat $5.52B Estimate
        Advanced Micro Devices (NASDAQ:AMD) reported quarterly earnings of $1.13 per share which beat the analyst consensus estimate of $0.91 by 24.18 percent. This is a 117.31 percent increase over earnings of $0.52 per share from the same period last year. The company reported quarterly sales of $5.89 billion which beat the analyst consensus estimate of $5.52 billion by 6.65 percent. This is a 70.89 percent increase over sales of $3.44 billion the same period last year.
        """
        text = text.lower()
        text = re.sub("[^a-zA-z0-9\s]", "", text)

        print("*" * 80)
        print(text)
        print("*" * 80)
        model = load_model("lstm")
        predict(model, text)


def predict(model, text):
    tokenizer = Tokenizer()
    # start_at = time.time()
    # Tokenize text
    x_test = pad_sequences(tokenizer.texts_to_sequences([text]), maxlen=LENGTH)
    # Predict
    score = model.predict([x_test])[0]
    print("Positive" if score > 0.5 else "Negative")


def init(df):
    # Constants
    LSTM_UNITS = 32
    # DROPOUT = 0.2
    EPOCHS = 13 # With Dropout
    # EPOCHS = 120 # Without Dropout
    BATCH_SIZE = 16
    LEARNING_RATE = 1e-4
    LABEL = "LSTM"

    # Data pre-processing
    df = data_preprocessing(df)

    # Tokenizing our dataframe after we split it into training/test data
    train, test = split_data(df, stratisfy=True)
    x_train, y_train, x_test, y_test, tokenizer, vocab_size = tokenize(train, test)

    # # Encoding the Categorical target into 0 and 1
    labelencoder = LabelEncoder()
    y_train = labelencoder.fit_transform(y_train)
    y_test = labelencoder.fit_transform(y_test)

    # Embedding Layer
    # Word2Vec Embedding Layer
    w2v_model = get_w2v_model()
    # w2v_model = get_w2v_model(True, train)
    embedding_layer = create_embedding_layer(vocab_size, tokenizer, w2v_model)

    # Glove Embedding Layer
    # embedding_layer = create_glove_embedding_layer(
    #     vocab_size=vocab_size, token=tokenizer
    # )

    """
    Build LSTM model and then fitting it
    """
    model = Sequential()
    # model.add(embedding_layer)
    model.add(embedding_layer)
    # model.add(Dropout(DROPOUT))
    # model.add(Bidirectional(LSTM(LSTM_UNITS)))
    model.add(LSTM(LSTM_UNITS, dropout=0.2))
    # model.add(LSTM(LSTM_UNITS))
    model.add(Dense(1, activation="sigmoid"))
    # model.add(Dense(1)),
    # model.summary()

    """
    Compile model
    """

    # model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
    model.compile(
        loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
        optimizer=tf.keras.optimizers.Adam(LEARNING_RATE),
        metrics=["accuracy"],
    )

    model_history = model.fit(
        x_train,
        y_train,
        batch_size=BATCH_SIZE,
        epochs=EPOCHS,
        validation_split=0.2,
        verbose=1,
    )
    # model.save("models/lstm")

    """
    Metrics & Predictions
    """

    # results = model.evaluate(x_test, y_test, batch_size=4)
    y_predictions = model.predict(x_test)
    y_predictions = y_predictions > 0.5

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

    # Paddining training and test
    x_train = pad_sequences(tokenizer.texts_to_sequences(train_df.text), maxlen=LENGTH)
    x_test = pad_sequences(tokenizer.texts_to_sequences(test_df.text), maxlen=LENGTH)
    y_train = train_df.sentiment
    y_test = test_df.sentiment

    return x_train, y_train, x_test, y_test, tokenizer, vocab_size


def create_glove_embedding_layer(vocab_size, token):
    embedding_vector = {}
    # f = open("models/glove.6B/glove.6B.300d.txt")
    f = open("models/glove.6B/glove.6B.300d.txt", encoding="utf8")
    for line in tqdm(f):
        value = line.split(" ")
        word = value[0]
        coef = np.array(value[1:], dtype="float32")
        embedding_vector[word] = coef

    embedding_matrix = np.zeros((vocab_size, LENGTH))
    for word, i in tqdm(token.word_index.items()):
        embedding_value = embedding_vector.get(word)
        if embedding_value is not None:
            embedding_matrix[i] = embedding_value

    return Embedding(
        vocab_size,
        LENGTH,
        weights=[embedding_matrix],
        input_length=300,
        trainable=False,
    )


def create_embedding_layer(vocab_size, tokenizer, w2v_model):
    embedding_matrix = np.zeros((vocab_size, LENGTH))
    for word, i in tokenizer.word_index.items():
        if word in w2v_model.wv:
            embedding_matrix[i] = w2v_model.wv[word]
    # print(embedding_matrix.shape)

    embedding_layer = Embedding(
        vocab_size,
        LENGTH,
        weights=[embedding_matrix],
        input_length=LENGTH,
        trainable=False,
    )

    return embedding_layer


def get_w2v_model(build=False, train_df=None):
    """
    Word2Vec Model

    # ignore this with gensim < 4.2.0 size parameter was not working, bug fixed by https://stackoverflow.com/questions/53195906/getting-init-got-an-unexpected-keyword-argument-document-this-error-in

    rolled back to
    pip install gensim==3.8.1
    as to avoid error:
    AttributeError: The vocab attribute was removed from KeyedVector in Gensim 4.0.0.
    Use KeyedVector's .key_to_index dict, .index_to_key list, and methods .get_vecattr(key, attr) and .set_vecattr(key, attr, new_val) instead.
    See https://github.com/RaRe-Technologies/gensim/wiki/Migrating-from-Gensim-3.x-to-4
    """
    if build:
        documents = [text.split() for text in train_df.text]
        # print(len(documents))

        w2v_model = gensim.models.word2vec.Word2Vec(
            size=LENGTH, window=7, min_count=10, workers=8
        )

        w2v_model.build_vocab(documents)
        words = w2v_model.wv.vocab.keys()
        vocab_size = len(words)
        print("vocab size: ", vocab_size)
        # print(w2v_model.wv.most_similar("good"))

        print(f"{now_str()} | Training word2vec model")
        w2v_model.train(documents, total_examples=len(documents), epochs=30)
        print(f"{now_str()} | Done training")
        w2v_model.save(f"models/word2vec/word2vec_{LENGTH}_v2.model")
    else:
        w2v_model = gensim.models.word2vec.Word2Vec.load(
            f"models/word2vec/word2vec_{LENGTH}_v2.model"
        )
    return w2v_model


"""
Accuracy-score: 0.6973365617433414
Class-report:
              precision    recall  f1-score   support

           0       0.70      0.70      0.70       413
           1       0.70      0.69      0.70       413

    accuracy                           0.70       826
   macro avg       0.70      0.70      0.70       826
weighted avg       0.70      0.70      0.70       826

F1-score: 0.6958637469586374
"""
