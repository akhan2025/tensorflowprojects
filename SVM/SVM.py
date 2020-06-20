import sklearn
from sklearn import datasets
from sklearn import svm, metrics
from sklearn.neighbors import KNeighborsClassifier

cancer = datasets.load_breast_cancer()

x = cancer.data
y = cancer.target
classes = ['malignant', 'benign']

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)

clf = svm.SVC(kernel="linear")
clf.fit(x_train,y_train)

y_predict = clf.predict(x_test)
acc = metrics.accuracy_score(y_test, y_predict)
for x in range(len(y_predict)):
    print(f"prediction:{classes[y_predict[x]]} actual value:{classes[y_test[x]]}")
print(acc)