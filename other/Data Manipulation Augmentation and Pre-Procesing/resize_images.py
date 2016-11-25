from PIL import Image
from os import listdir
import os

###Change
width = 32
height = 32

srcDirectory = "pokemon_dataset_complete"
dstDirectory = "resized_datasets/" + str(width) + "x" + str(height)
imageList = listdir(srcDirectory)

errorDirectory = "error_log"
errorFile = open("resize_errors", 'w')
# nameList = [i.strip() for i in open("names.txt", 'r').readlines()]

# for imageFile in nameList:
# 	name = imageFile
# 	os.makedirs(dstDirectory + "/nearest/" + name)
# 	os.makedirs(dstDirectory + "/bilinear/" + name)
# 	os.makedirs(dstDirectory + "/bicubic/" + name)
# 	os.makedirs(dstDirectory + "/antialias/" + name)

for imageFile in imageList:

	im1 = Image.open(srcDirectory + "/" + imageFile)

	print (imageFile)

	try:
		im2 = im1.resize((width, height), Image.NEAREST)
		im3 = im1.resize((width, height), Image.BILINEAR)
		im4 = im1.resize((width, height), Image.BICUBIC)
		im5 = im1.resize((width, height), Image.ANTIALIAS)

		# name = ''.join([i for i in imageFile if not i.isdigit()])
		# name = name[0:-4]+"/"
		name = ""

		ext = ".png"
		im2.save(dstDirectory + "/nearest/" + name + imageFile)
		im3.save(dstDirectory + "/bilinear/" + name + imageFile)
		im4.save(dstDirectory + "/bicubic/" + name + imageFile)
		im5.save(dstDirectory + "/antialias/" + name + imageFile)

	except Exception:
			errorFile.write(imageFile + "\n")
