import pandas as pd
import numpy as np
import sklearn
from sklearn.utils import shuffle
from sklearn.neighbors import KNeighborsClassifier
from sklearn import linear_model, preprocessing
import pickle
from random import seed, randint

data = pd.read_csv("car.data")

encoder = preprocessing.LabelEncoder()
buying = encoder.fit_transform(list(data["buying"]))
maint = encoder.fit_transform(list(data["maint"]))
door = encoder.fit_transform(list(data["door"]))
persons = encoder.fit_transform(list(data["persons"]))
lug_boot = encoder.fit_transform(list(data["lug_boot"]))
safety = encoder.fit_transform(list(data["safety"]))
cls = encoder.fit_transform(list(data["class"]))

predict = "class"

X = list(zip(buying,maint,door,persons,lug_boot,safety))
Y = list(cls)

X_train, X_test, Y_train, Y_test = sklearn.model_selection.train_test_split(X, Y, test_size=0.1)

"""best = 0
for _ in range(100):
    X_train, X_test, Y_train, Y_test = sklearn.model_selection.train_test_split(X, Y, test_size=0.1)

    seed()
    random = randint(1, 15)
    model = KNeighborsClassifier(n_neighbors=random)

    model.fit(X_train, Y_train)

    acc = model.score(X_test, Y_test) * 100
    print(f"model is {acc}% accurate\n")

    if acc > best:
        #pickle saves the model for later use
        with open("KNNmodel.pickle", "wb") as f:
            pickle.dump(model, f)
        best = acc
        print(best)"""

pickle_file = open("KNNmodel.pickle", "rb")
model = pickle.load(pickle_file)

accuracy = model.score(X_test, Y_test)
print(f"{accuracy}% accurate ate predicting classes of cars")

prediction = model.predict(X_test)

for x in range(len(prediction)):
    print(f"prediction:{prediction[x]} data passed through:{X_test[x]} actual value:{Y_test[x]}")

