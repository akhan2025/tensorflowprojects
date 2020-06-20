import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
import matplotlib.pyplot as pyplot
import pickle
from matplotlib import style

# reads the data from the file provided
data = pd.read_csv("student-mat.csv", sep=";")
data = data[["G1", "G2", "G3", "studytime", "failures", "absences"]]

# picks a label to predict
predict = "G3"

# creates a dataset for the data and one for the predictor
X = np.array(data.drop([predict], 1))
Y = np.array(data[[predict]])
X_train, X_test, Y_train, Y_test = sklearn.model_selection.train_test_split(X, Y, test_size=0.1)
# for loop to improve model
"""best = 0
for _ in range(100):
    X_train, X_test, Y_train, Y_test = sklearn.model_selection.train_test_split(X, Y, test_size=0.1)

    linear = linear_model.LinearRegression()

    linear.fit(X_train, Y_train)

    acc = linear.score(X_test, Y_test) * 100
    print("model is", acc, "% accurate\n")

    if acc > best:
        #pickle saves the model for later use
        with open("linearModel.pickle", "wb") as f:
            pickle.dump(linear, f)
        best= acc"""

#readd the saved model
pickle_file = open("linearModel.pickle", "rb")
linear = pickle.load(pickle_file)

prediction = linear.predict(X_test)
prediction = np.round(prediction)

for x in range(len(prediction)):
    print(f"prediction:{prediction[x]} data passed through:{X_test[x]} actual value:{Y_test[x]}")

style.use("ggplot")
p = "G1"
pyplot.scatter(data[p],data["G3"])
pyplot.xlabel(p)
pyplot.ylabel("Final Grades")
pyplot.show()