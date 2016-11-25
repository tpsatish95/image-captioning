import os
"""import numpy as np
from scipy.misc import imread, imsave, imresize"""
from PIL import Image
import cv2
import pickle
import numpy as np
from sklearn.cross_validation import train_test_split

# dataPath = "Data/Hist8/"
# dataPath = "Data/NoBGHist8/"
# dataPath = "Data/NoBGHist8_100x100/"
# dataPath = "Data/NoBGWholeHist/"
dataPath = "Data/WithBGKantoHist16/"

def save_obj(obj, name ):
    with open( dataPath + name + ".pkl", 'wb') as f:
        pickle.dump(obj, f,  protocol=2)

path = "pokemon_blended_cards/32x32/antialias/"
# path = "resized_datasets/32x32/antialias/"
# path = "pokemon_dataset_completeF/"

folders = os.listdir(path)

nameList = [i.strip() for i in open("names.txt").readlines()]

numPokemon = 718

nameLabelDict = {nameList[i] : i+1 for i in range(len(nameList))}

count = 0
data = []
labels = []


Kanto = [i.strip() for i in open("Kanto.txt").readlines()]
folders = list(set(folders).intersection(set(Kanto)))

iBin = 16
for folder in folders:
    images = os.listdir(path + folder)

    print (folder)
    for image in images:
        image = cv2.imread(path + folder + "/" + image,cv2.IMREAD_UNCHANGED)
        hist = cv2.calcHist([image], [0, 1, 2], None, [iBin, iBin, iBin], [0, 256, 0, 256, 0, 256])
        # hist = cv2.normalize(hist,hist)

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

categories = sorted([i.strip() for i in open("names.txt").readlines()])
print("%d categories" % len(categories))
print()

print("n_samples: "+str(len(X_train))+", n_features: "+str(len(X_train[0])))
print()

print("n_samples: "+str(len(X_test))+", n_features: "+str(len(X_test[0])))
print()

save_obj(X_train,"X_train")
save_obj(X_test,"X_test")
save_obj(y_train,"Y_train")
save_obj(y_test,"Y_test")
save_obj(nameLabelDict,"namelabelmap")
