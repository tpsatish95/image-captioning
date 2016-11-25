from PIL import Image
from os import listdir
import os

desDirectory = "pokemon_blended_cards/32x32/antialias/"

countFile = open("counts.txt",'w')

backgroundImageDirectory = "background_data/resized_bg/32x32/antialias/"
overlayImageDirectory = "resized_datasets/32x32/antialias/"

backgroundImageList = listdir(backgroundImageDirectory)
overLayImageList = listdir(overlayImageDirectory)

count = 0

for background in backgroundImageList:
	for overlay in overLayImageList:

		backgroundImage = Image.open(backgroundImageDirectory + background)
		overlayImage = Image.open(overlayImageDirectory + overlay)

		backgroundImage = backgroundImage.convert("RGBA")
		overlayImage = overlayImage.convert("RGBA")

		backgroundImage.paste(overlayImage, (0,0), overlayImage)
		name = ''.join([i for i in overlay if not i.isdigit()])
		name = name[0:-4]

		print("Name is: " + name)

		if not os.path.exists(desDirectory + name):
			os.makedirs(desDirectory + name)
			countFile.write(name + " " + str(count) + "\n")


		backgroundImage.save(desDirectory + name + "/" + str(count) + ".png","PNG")
		count = count + 1
