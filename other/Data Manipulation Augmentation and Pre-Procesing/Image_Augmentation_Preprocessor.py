import numpy as np
from skimage.io import imread, imshow, imsave
import random
from skimage import transform as tf
from PIL import Image
import time
import os
# import math
# from skimage.viewer import ImageViewer
# import scipy.ndimage as ndimage
# import warnings
# warnings.filterwarnings("ignore")

# TO DO
# load images and form X and y for pre preprocessing

def horizontal_flip(x):
    for i in range(x.shape[0]):
        x[i] = np.flipud(x[i])
    return x

def vertical_flip(x):
	return tf.rotate(x, 180)

def random_barrel_transform(x, intensity):
    # TODO (fish eye transform)
    pass

def random_channel_shift(x, rg):
    # TODO
    pass

def array_to_img(x, scale=True):
    from PIL import Image
    x = x.transpose(1, 2, 0)
    if scale:
        x += max(-np.min(x), 0)
        x /= np.max(x)
        x *= 255
    if x.shape[2] == 3:
        # RGB
        return Image.fromarray(x.astype("uint8"), "RGB")
    else:
        # grayscale
        return Image.fromarray(x[:, :, 0].astype("uint8"), "L")


def img_to_array(img):
    x = np.asarray(img, dtype='float32')
    if len(x.shape) == 3:
        # RGB: height, width, channel -> channel, height, width
        x = x.transpose(2, 0, 1)
    else:
        # grayscale: height, width -> channel, height, width
        x = x.reshape((1, x.shape[0], x.shape[1]))
    return x

class image_data_augmenter(object):

	def __init__(self):
		self.rgAngle = 45
		self.rgShear = 0.5
		self.rgScale = 1.5 # Zoom
		self.rgTranslate = 10
		self.rgSwirl = 3
		self.reW = self.reH = 100

		self.angle = 0
		self.shear = 0
		self.scale = 0
		self.translate = 0
		self.swirl = 0

	def parameters_randomize(self,i=42):
		random.seed(i)

		self.angle = random.uniform(-self.rgAngle, self.rgAngle)
		self.shear = random.uniform(-self.rgShear, self.rgShear)

		sx = random.uniform(0.5, self.rgScale)
		sy = random.uniform(0.7, self.rgScale)
		self.scale = [sx,sy]

		tx = random.uniform(0, self.rgTranslate)
		ty = random.uniform(0, self.rgTranslate)
		self.translate = [tx,ty]

		self.swirl = random.uniform(1, self.rgSwirl)

	def random_transform(self,image):

		rotated = tf.rotate(image, self.angle)

		if random.random() < 0.5:
			rotated = horizontal_flip(rotated)
		if random.random() < 0.2: # 20%
			rotated = vertical_flip(rotated)

		# Create Afine transform
		afine_tf = tf.AffineTransform(scale = self.scale, shear = self.shear, translation = self.translate)
		# Apply transform to image data
		modified = tf.warp(rotated, afine_tf)

		if random.random() < 0.1: # 20%
			modified = tf.swirl(modified, rotation=0, strength = self.swirl, radius=image.shape[1]/2)

		return tf.resize(modified, [self.reW, self.reH])

class image_data_preprocessor(object):

	def __init__(self,
	         featurewise_center=True,  # set input mean to 0 over the dataset
	         samplewise_center=False,  # set each sample mean to 0
	         featurewise_std_normalization=True,  # divide inputs by std of the dataset
	         samplewise_std_normalization=False,  # divide each input by its std
	         zca_whitening=False):  # apply ZCA whitening

	    self.__dict__.update(locals())
	    self.mean = None
	    self.std = None
	    self.principal_components = None

	def fit(self, X):
		'''Required for featurewise_center, featurewise_std_normalization and zca_whitening.
		'''
		X = np.copy(X)

		if self.featurewise_center:
		    self.mean = np.mean(X, axis=0)
		    # X -= self.mean
		if self.featurewise_std_normalization:
		    self.std = np.std(X, axis=0)
		    # X /= self.std

		if self.zca_whitening:
		    flatX = np.reshape(X, (X.shape[0], X.shape[1]*X.shape[2]*X.shape[3]))
		    fudge = 10e-6
		    sigma = np.dot(flatX.T, flatX) / flatX.shape[1]
		    U, S, V = linalg.svd(sigma)
		    self.principal_components = np.dot(np.dot(U, np.diag(1. / np.sqrt(S + fudge))), U.T)

    # First fit then Normalize
	def normalize_save(self, X, y,save_to_dir=None, save_prefix="", save_format="jpeg"):
		assert len(X) == len(y)

		for i in range(len(X)):
		    x = X[i]
		    x = self.standardize(x)
		    X[i] = x

		if save_to_dir:
		    for i in range(len(X)):
		        img = array_to_img(X[i], scale=True)
		        img.save(save_to_dir + "/" + save_prefix + "_" + str(i) + "." + save_format)

		return X

	def standardize(self, x):
		if self.featurewise_center:
		    x -= self.mean
		if self.featurewise_std_normalization:
		    x /= self.std

		if self.zca_whitening:
		    flatx = np.reshape(x, (x.shape[0]*x.shape[1]*x.shape[2]))
		    whitex = np.dot(flatx, self.principal_components)
		    x = np.reshape(whitex, (x.shape[0], x.shape[1], x.shape[2]))

		if self.samplewise_center:
		    x -= np.mean(x)
		if self.samplewise_std_normalization:
		    x /= np.std(x)

		return x

baseDir = "Pokemon_Kanto/"
saveDir = "Pokemon_Kanto_Aug/"
numImages = 1000 # number images to be generated
aug = image_data_augmenter()

ex = "png"
rseed = 0
# temp = ['Machop', 'Magikarp', 'Magmar', 'Magnemite', 'Magneton', 'Mankey', 'Marowak', 'Meowth', 'Metapod', 'Mew', 'Mewtwo', 'Moltres', 'Mr Mime', 'Muk', 'Nidoking', 'Nidoqueen', 'Nidoran', 'Raticate']
for d in os.listdir(baseDir):
# for d in temp:
	os.makedirs(saveDir + d)

	fList = os.listdir(baseDir + d)

	num = numImages - len(fList)
	batchSize = int ((num / len(fList)) + 1)

	count = 0
	for f in fList:
		fPath = baseDir + d + "/" + f
		# image = imread(fPath)
		image = np.asarray(Image.open(fPath).convert("RGBA"))

		# resize original image
		imsave(saveDir+ d + "/" + str(count) + "." + ex,tf.resize(image, [aug.reW, aug.reH]),plugin = 'pil')
		count+=1

		for i in range(batchSize):
			rseed+=1

			aug.parameters_randomize(rseed)
			imageM = aug.random_transform(image)

			imsave(saveDir+ d + "/" + str(count) + "." + ex,imageM,plugin = 'pil')
			count+=1

		# time.sleep(5)
