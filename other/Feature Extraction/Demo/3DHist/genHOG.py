# import the necessary packages
from matplotlib import pyplot as plt
import numpy as np
import argparse
import cv2
from PIL import Image

# load the image and show it
image3 = np.asarray(Image.open("sample4.jpg").convert('RGBA').resize((32,32),Image.ANTIALIAS))
image1 = np.asarray(Image.open("1.png").convert('RGBA').resize((32,32),Image.ANTIALIAS))
image2 = np.asarray(Image.open("4.png").convert('RGBA').resize((32,32),Image.ANTIALIAS))
# cv2.imshow("image", image)

# grab the image channels, initialize the tuple of colors,
# the figure and the flattened feature vector
i=1
for image in [image1,image2,image3]:
	chans = cv2.split(image)
	colors = ("r", "g", "b")
	plt.figure()
	plt.title("'Flattened' Color Histogram")
	plt.xlabel("Bins")
	plt.ylabel("# of Pixels")
	features = []

	# loop over the image channels
	for (chan, color) in zip(chans, colors):
		# create a histogram for the current channel and
		# concatenate the resulting histograms for each
		# channel
		hist = cv2.calcHist([chan], [0], None, [8], [0, 256])
		hist = hist / sum(hist)

		features.extend(hist)

		# plot the histogram
		plt.plot(hist, color = color)
		plt.xlim([0, 8])
		plt.ylim([0,0.4])

	plt.savefig("Flat3DHist"+str(i))
	i+=1
