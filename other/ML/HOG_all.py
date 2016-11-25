from sklearn.cross_validation import train_test_split
import pickle
import numpy as np
import sys
from time import time

from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import RidgeClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils.extmath import density
from sklearn import metrics
from sklearn import cross_validation
import pickle


# dataFile = "../Data/NoBG_Hist32/data"
# labelFile = "../Data/NoBG_Hist32/labels"

# def load_obj(name ):
#     with open( name + '.pkl', 'rb') as f:
#         return pickle.load(f)

# def save_obj(obj, name ):
#     with open( name + '.pkl', 'wb') as f:
#         pickle.dump(obj, f,  protocol=2)

# X = np.array(load_obj(dataFile))
# y = np.array(load_obj(labelFile))

# X = load_obj(dataFile)
# y = load_obj(labelFile)

dataPath = "../Data/HOGKanto/" # 98.1 % Random Forest
# dataPath = "../Data/HOG/" # 95.5 % 12NN

def load_obj(name ):
    with open( dataPath + name + ".pkl", 'rb') as f:
        return pickle.load(f)

def save_obj(obj, name ):
    with open( dataPath + name + ".pkl" , 'wb') as f:
        pickle.dump(obj, f,  protocol=2)

X_train = np.array(load_obj("X_train"))
y_train = np.array(load_obj("Y_train"))

X_test = np.array(load_obj("X_test"))
y_test = np.array(load_obj("Y_test"))

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01, train_size=0.10, random_state=42, stratify = y)
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify = y)

# print("Train Test split over!")

# def size_mb(docs):
#     return sum(len(s) for s in docs) / 1e6
# data_train_size_mb = size_mb(X_train)
# data_test_size_mb = size_mb(X_test)

# print("%d documents - %0.3fMB (training set)" % (
#     len(X_train), data_train_size_mb))
# print("%d documents - %0.3fMB (test set)" % (
#     len(X_test), data_test_size_mb))

# categories = sorted([i.strip() for i in open("../names.txt").readlines()])
# print(categories)
# print("%d categories" % len(categories))
# print()

# print("n_samples: "+str(len(X_train))+", n_features: "+str(len(X_train[0])))
# print()

# print("n_samples: "+str(len(X_test))+", n_features: "+str(len(X_test[0])))
# print()

# ### Vary K Value
# k=3500
# print("Extracting "+str(k) +" best features by a chi-squared test")
# t0 = time()
# ch2 = SelectKBest(chi2, k=k)
# X_train = ch2.fit_transform(X_train, y_train)
# X_test = ch2.transform(X_test)

# feature_names = [feature_names[i] for i in ch2.get_support(indices=True)]
# print("done in %fs" % (time() - t0))
# print()
# feature_names = np.asarray(feature_names)

def trim(s):
    """Trim string to fit on terminal (assuming 80-column display)"""
    return s if len(s) <= 80 else s[:77] + "..."

###############################################################################
# Benchmark classifiers
# Bench Mark Result Print Function
def benchmark(clf):
    print('_' * 80)
    print("Training: ")
    print(clf)
    t0 = time()
    clf.fit(X_train, y_train)
    train_time = time() - t0
    print("train time: %0.3fs" % train_time)

    t0 = time()
    pred = clf.predict(X_test)
    test_time = time() - t0
    print("test time:  %0.3fs" % test_time)

    score = metrics.accuracy_score(y_test, pred)
    print("accuracy:   %0.3f" % score)

    # if hasattr(clf, 'coef_'):
    #     print("dimensionality: %d" % clf.coef_.shape[1])
    #     print("density: %f" % density(clf.coef_))
    #     print()

    # print("classification report:")
    # print(metrics.classification_report(y_test, pred,target_names=categories))

    # print("confusion matrix:")
    # print(metrics.confusion_matrix(y_test, pred))
    save_obj(clf,"12NNHOGKanto")
    print()
    clf_descr = str(clf).split('(')[0]
    return clf_descr, score, train_time, test_time

results = []

print('=' * 80)
print("kNN")
results.append(benchmark(KNeighborsClassifier(n_neighbors=12,n_jobs=8)))
# print("Random Forest")
# results.append(benchmark(RandomForestClassifier(n_estimators=100,n_jobs=8)))

# for clf, name in (
#         (RidgeClassifier(tol=1e-2, solver="lsqr"), "Ridge Classifier"),
#         (Perceptron(n_iter=50,n_jobs=8), "Perceptron"),
#         (PassiveAggressiveClassifier(n_iter=50,n_jobs=8), "Passive-Aggressive"),
#         (KNeighborsClassifier(n_neighbors=1,n_jobs=8), "kNN"),
#         (RandomForestClassifier(n_estimators=100,n_jobs=8), "Random forest")
#         ):
#     print('=' * 80)
#     print(name)
#     results.append(benchmark(clf))

# for penalty in ["l2", "l1"]:
#     print('=' * 80)
#     print("%s penalty" % penalty.upper())
#     # Train Liblinear model
#     results.append(benchmark(LinearSVC(loss='l2', penalty=penalty,dual=False, tol=1e-3)))

#     # Train SGD model
#     results.append(benchmark(SGDClassifier(alpha=.0001, n_iter=50,penalty=penalty,n_jobs=8)))

# # Train SGD with Elastic Net penalty
# print('=' * 80)
# print("Elastic-Net penalty")
# results.append(benchmark(SGDClassifier(alpha=.0001, n_iter=50,penalty="elasticnet")))

# # Train NearestCentroid without threshold
# print('=' * 80)
# print("NearestCentroid (aka Rocchio classifier)")
# results.append(benchmark(NearestCentroid()))

# # Train sparse Naive Bayes classifiers
# print('=' * 80)
# print("Naive Bayes")
# # results.append(benchmark(MultinomialNB(alpha=.01)))
# results.append(benchmark(BernoulliNB(alpha=.01)))

# print('=' * 80)
# print("LinearSVC with L1-based feature selection")
# # The smaller C, the stronger the regularization.
# # The more regularization, the more sparsity.
# results.append(benchmark(Pipeline([
#   ('feature_selection', LinearSVC(penalty="l1", dual=False, tol=1e-3)),
#   ('classification', LinearSVC())
# ])))
