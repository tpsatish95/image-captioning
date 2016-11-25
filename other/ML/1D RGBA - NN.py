import pickle
import numpy as np
import cv2

'''
Of the following :
  HISTCMP_BHATTACHARYYA = 3
  HISTCMP_CHISQR = 1
  HISTCMP_CHISQR_ALT = 4
  HISTCMP_CORREL = 0
  HISTCMP_HELLINGER = 3
  HISTCMP_INTERSECT = 2
  HISTCMP_KL_DIV = 5
HISTCMP_BHATTACHARYYA - Best for histograms (8 bins)
'''

# dataPath = "../Data/NoBGHist8/"
# dataPath = "../Data/NoBGWholeHist/"
# dataPath = "../Data/NoBGHist8_100x100/"
dataPath = "../Data/WithBGKantoHist8/"
# dataPath = "../Data/HOG/"
#iBin = 8 and bahtacharya accuracy: 0.419144 [Finished in 1038.4s]

def load_obj(name ):
    with open( dataPath + name + ".pkl", 'rb') as f:
        return pickle.load(f)

def save_obj(obj, name ):
    with open( dataPath +  namename + ".pkl" , 'wb') as f:
        pickle.dump(obj, f,  protocol=2)

class NearestNeighbor:
  def __init__(self):
    pass

  def train(self, X, y):
    """ X is N x D where each row is an example. Y is 1-dimension of size N """
    # the nearest neighbor classifier simply remembers all the training data
    self.Xtr = X
    self.ytr = y

  # def chi2_distance(self, histA, histB, eps = 1e-10):
  #   # compute the chi-squared distance
  #   d = 0.5 * np.sum([((histA - histB) ** 2) / (histA + histB + eps)], axis = 1)
  #   # return the chi-squared distance
  #   return d

  def chi2_distance(self, histsA, histB, eps = 1e-10):
    # compute the chi-squared distance
    d = []
    for h in histsA:
      d.append(cv2.compareHist(h,histB,cv2.HISTCMP_BHATTACHARYYA))
    # return the chi-squared distance
    return np.array(d)

  def predict(self, X):
    """ X is N x D where each row is an example we wish to predict label for """
    num_test = X.shape[0]
    # lets make sure that the output type matches the input type
    Ypred = np.zeros(num_test, dtype = self.ytr.dtype)

    # loop over all test rows
    for i in range(num_test):
      print ("Testing example " + str(i))
      distances = np.sum(np.abs(self.Xtr - X[i,:]), axis = 1)
      # distances = self.chi2_distance(self.Xtr, X[i,:])
      min_index = np.argmin(distances) # get the index with smallest distance
      Ypred[i] = self.ytr[min_index] # predict the label of the nearest example
      print ("Class Label: " + str(Yte[i]) + "    " + "Predicted label: " + str(Ypred[i]))
    return Ypred

trainPath = "../Data/Train/"
trainFile = "X_train.pkl"
trainLabelsFile = "Y_train.pkl"

testPath = "../Data/Test/"
testFile = "X_test.pkl"
testLabelsFile = "Y_test.pkl"

Xtr = np.asarray(np.load(trainPath + trainFile))
Ytr = np.asarray(np.load(trainPath + trainLabelsFile))

Xte = np.asarray(np.load(testPath + testFile))
Yte = np.asarray(np.load(testPath + testLabelsFile))

Xtr_rows = Xtr.reshape(Xtr.shape[0], 32 * 32 * 4)
Xte_rows = Xte.reshape(Xte.shape[0], 32 * 32 * 4)

###
Xtr = np.array(load_obj("X_train"))
Ytr = np.array(load_obj("Y_train"))

Xte = np.array(load_obj("X_test"))
Yte = np.array(load_obj("Y_test"))

###
# Training
nn = NearestNeighbor()
nn.train(Xtr, Ytr)

Yte_predict = nn.predict(Xte)
print ("accuracy: %f" % ( np.mean(Yte_predict == Yte) ))
