import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.preprocessing import scale
from sklearn import metrics

# K means clustering is using the idea of randomly placed centroids and taking
# the distance between them, averging it, and moving them to create more accurate
# predictions of data points


# load the dataset from the data provided by sklearn
digit = load_digits()

# scale the data down for faster computations and save it
data = scale(digit.data)
y = digit.target
k = len(np.unique(y))

# i forget
samples, features = data.shape

# allows the algorithm to utilize multiple different scoring methods
# documentation for what they mean can be found here:
# https://scikit-learn.org/stable/modules/clustering.html#clustering-evaluation
def bench_k_means(estimator, name, data):
    estimator.fit(data)
    print('%-9s\t%i\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f'
          % (name, estimator.inertia_,
             metrics.homogeneity_score(y, estimator.labels_),
             metrics.completeness_score(y, estimator.labels_),
             metrics.v_measure_score(y, estimator.labels_),
             metrics.adjusted_rand_score(y, estimator.labels_),
             metrics.adjusted_mutual_info_score(y,  estimator.labels_),
             metrics.silhouette_score(data, estimator.labels_,
                                      metric='euclidean')))

# K centroids and k-means++ allows for them to start equidistant from each other
# n_init allows for it to run the algo that many times and picking the best one
clf = KMeans(n_clusters=k, init='k-means++', n_init=15)
bench_k_means(clf, "inertia and accuracy scores:", data)
