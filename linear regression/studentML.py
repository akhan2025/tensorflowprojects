import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model

# reads the data from the file provided
data = pd.read_csv("student-mat.csv", sep=";")
data = data[["G1", "G2", "G3", "studytime", "failures", "absences"]]

# picks a label to predict
predict = "G3"

# creates a dataset for the data and one for the predictor
X = np.array(data.drop([predict], 1))
Y = np.array(data[[predict]])

# create the training and testing variables and sample size
# test_size=0.1 means 10% of the data is reserved for when testing so the
# computer doesnt have access to it beforehand
X_train, X_test, Y_train, Y_test = sklearn.model_selection.train_test_split(X, Y, test_size=0.1)

# using a linear regression algorithm or line of best fit
linear = linear_model.LinearRegression()

# plug in the data and train the machine
linear.fit(X_train, Y_train)

# scores the accuracy of the machine algorithm after training
acc = linear.score(X_test, Y_test) * 100
print("model is", acc, "% accurate\n")
print("slope:", linear.coef_)
print("y-intercept:", linear.intercept_)

prediction = linear.predict(X_test)
prediction = np.round(prediction)

for x in range(len(prediction)):
    print(f"prediction:{prediction[x]} data passed through:{X_test[x]} actual value:{Y_test[x]}")
