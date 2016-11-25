import os
import pickle
from PIL import Image
from skimage.feature import hog
from skimage.io import imread

modelPath ="../Data/HOGKanto/12NNHOGKanto"
labelFile ="../Data/HOGKanto/namelabelmap"

def load_obj(name ):
    with open(name + ".pkl", 'rb') as f:
        return pickle.load(f)

Timgs = os.listdir("TestImages")

model = load_obj(modelPath)
labels = load_obj(labelFile)
labels2Poke = {v: k for k, v in labels.items()}

width = 32
height = 32

for img in Timgs:
	print(img)
	im1 = Image.open("TestImages/" + img)
	im2 = im1.resize((width, height), Image.ANTIALIAS)
	im2.save("TestImages/" + img)

	image = imread("TestImages/" + img, as_grey=True)
	h = hog(image)
	label = model.predict([h])[0]
	print(str(labels2Poke[label]))
