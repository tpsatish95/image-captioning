from bs4 import BeautifulSoup
import urllib.request

urls = open("urls.txt", 'r+')
names = open("names.txt", 'r')


urlArray = urls.readlines()
nameList = names.readlines()

count = 0

for index in range(len(nameList)):
	nameList[index] = nameList[index].strip()

#For debugging
print (len(nameList[0]))

for url in urlArray:
	#Find pokemon name
	beginning = url.rfind('/')
	beginning = beginning + 3
	endChar = url.find('_')
	if endChar == -1:
		endChar = url.rfind('.')

	pokemonName = url[beginning + 1 : endChar]

	#For pokemon with unstructred names, just replace 'in' with 'not in'
	if pokemonName in nameList:
		if pokemonName != '':
			urllib.request.urlretrieve(url, "pokemon_dataset/" + pokemonName + str(count) + ".png")
			#For debugging
			print (pokemonName + str(count) + ".png")
			#For unique names
			count = count + 1
	