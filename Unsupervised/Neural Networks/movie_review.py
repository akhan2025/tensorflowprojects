from tensorflow import keras
from tensorflow.keras.models import load_model
from os import path
import string

data = keras.datasets.imdb
(train_data, train_labels), (test_data, test_labels) = data.load_data(num_words = 88000)

word_index = data.get_word_index()
word_index = {k: (v + 3) for k, v in word_index.items()}
word_index["<PAD>"] = 0
word_index["<START>"] = 1
word_index["<UNK>"] = 2
word_index["<UNUSED>"] = 3

reverse_word_index = dict([value, key] for (key, value) in word_index.items())

train_data = keras.preprocessing.sequence.pad_sequences(train_data, value = word_index["<PAD>"], padding = "post",
                                                        maxlen = 250)
test_data = keras.preprocessing.sequence.pad_sequences(test_data, value = word_index["<PAD>"], padding = "post",
                                                       maxlen = 250)


def decoder(text):
    return " ".join([reverse_word_index.get(i, "?") for i in text])


if path.exists('movieGoer.h5'):
    model = load_model('movieGoer.h5')
else:
    model = keras.Sequential()
    model.add(keras.layers.Embedding(88000, 16))
    model.add(keras.layers.GlobalAveragePooling1D())
    model.add(keras.layers.Dense(16, activation = "relu"))
    model.add(keras.layers.Dense(1, activation = "sigmoid"))

    model.compile(optimizer = "adam", loss = "binary_crossentropy", metrics = ["accuracy"])

"""x_val = train_data[:10000]
x_train = train_data[10000:]

y_val = train_labels[:10000]
y_train = train_labels[10000:]

fitModel = model.fit(train_data, train_labels, epochs=25, batch_size= 512, validation_data = (test_data, 
test_labels), verbose = 1) model.save('movieGoer.h5') results = model.evaluate(test_data, test_labels) 

review_test = test_data[47]
predict = model.predict([review_test])
print(f"review: {decoder(review_test)}\n Prediction: {predict[47]}\n actual: {test_labels[47]}"""


def review_encode(s):
    encoded = [1]

    for word in s:
        if word.lower() in word_index:
            encoded.append(word_index[word.lower()])
        else:
            encoded.append(2)
    return encoded


with open("review.txt", encoding = "utf-8") as f:
    for line in f.readlines():
        nline = line.translate(str.maketrans('', '', string.punctuation)).split()
        encode = review_encode(nline)
        encode = keras.preprocessing.sequence.pad_sequences([encode], value = word_index["<PAD>"], padding = "post",
                                                            maxlen = 250)
        predict = model.predict(encode)