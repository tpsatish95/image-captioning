import os
"""import numpy as np
from scipy.misc import imread, imsave, imresize"""
from PIL import Image
import cv2
import pickle
import numpy as np

from sklearn.cross_validation import train_test_split
import sys
from time import time

from sklearn.feature_selection import SelectKBest, chi2
from sklearn.neighbors import KNeighborsClassifier
from sklearn.utils.extmath import density
from sklearn import metrics
from sklearn import cross_validation


dataF = "../Data/NoBG_Hist32/data.pkl"
labelF = "../Data/NoBG_Hist32/labels.pkl"

def load_obj(name ):
    with open( name, 'rb') as f:
        return pickle.load(f)

def save_obj(obj, name ):
    with open( name , 'wb') as f:
        pickle.dump(obj, f,  protocol=2)

dataPath = "../Data/NoBG_Hist32/"

path = "../pokemon_blended_cards/32x32/antialias/"
# path = "../resized_datasets/32x32/antialias/"
folders = os.listdir(path)
nameList = [i.strip() for i in open("../names.txt").readlines()]

# for index in range(len(nameList)):
#     nameList[index] = nameList[index].strip()

numPokemon = 150

nameLabelDict = {nameList[i] : i+1 for i in range(len(nameList))}
# Till 14 got 38% accuracy (3D Hist KNN SciKit Blind Implementation)

for iBin in range(15,65):
    print(iBin)
    count = 0
    data = []
    labels = []
    for folder in folders:
        images = os.listdir(path + folder)

        # print (folder)
        for image in images:
            image = cv2.imread(path + folder + "/" + image)
            hist = cv2.calcHist([image], [0, 1, 2], None, [iBin, iBin, iBin], [0, 256, 0, 256, 0, 256])
            # hist = cv2.normalize(hist)

            # 3D histogram as a flattened array
            hist = hist.flatten()
            # Normalize
            hist = hist / sum(hist)

            data.append(hist)
            labels.append(nameLabelDict[folder])

            # print (str(folder) + " " + str(nameLabelDict[folder]) + " " +str(count))
            count += 1

    X = data
    y = labels

    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01, train_size=0.10, random_state=42, stratify = y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify = y)

    print("Train Test split over!")

    def size_mb(docs):
        return sum(len(s) for s in docs) / 1e6
    data_train_size_mb = size_mb(X_train)
    data_test_size_mb = size_mb(X_test)

    print("%d documents - %0.3fMB (training set)" % (
        len(X_train), data_train_size_mb))
    print("%d documents - %0.3fMB (test set)" % (
        len(X_test), data_test_size_mb))

    categories = sorted([i.strip() for i in open("../names.txt").readlines()])
    # print(categories)
    print("%d categories" % len(categories))
    print()

    print("n_samples: "+str(len(X_train))+", n_features: "+str(len(X_train[0])))
    print()

    print("n_samples: "+str(len(X_test))+", n_features: "+str(len(X_test[0])))
    print()

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
        print()
        clf_descr = str(clf).split('(')[0]
        return clf_descr, score, train_time, test_time

    results = []

    print('=' * 80)
    print("kNN")
    results.append(benchmark(KNeighborsClassifier(n_neighbors=1,n_jobs=8)))

####
# Try different feature representation techniques
# Try 1NN explicit code
# Modify the KNN parameters used to train
    # Try Different Distance Metrics
# Compute 3D Colour Histograms (Properly)
# Pokemon Split it based on Region (Kanto, Sinoh, etc)
# Apply histograms on full size images (Do not scale)
