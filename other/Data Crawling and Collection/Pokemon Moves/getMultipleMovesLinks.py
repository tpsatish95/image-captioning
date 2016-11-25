import urllib.request
from bs4 import BeautifulSoup
import pickle
from collections import defaultdict

def save_obj(obj, name ):
    with open( name + '.pkl', 'wb') as f:
        pickle.dump(obj, f,  protocol=2)

def load_obj(name ):
    with open( name + '.pkl', 'rb') as f:
        return pickle.load(f)

attack_base = load_obj("attackImagesLinks")

attackMultiImagesLinks = defaultdict(list)

for move in attack_base.keys():
	links = []
	for j in attack_base[move]:
		if "None" not in j[0]:
			links.append(j)

	for imgItem in links:
		try:
			print(imgItem)

			base_link = imgItem[0]
			base_poke = imgItem[1]

			url = urllib.request.urlopen(base_link)
			html_doc = url.read().decode("utf-8")

			# make a soup
			soup = BeautifulSoup(html_doc, 'html.parser')

			divContent = soup.findAll("div", { "id" : "mw-imagepage-section-filehistory" })[0]

			mainTable = divContent.find_all("table")[0]
			for tr in mainTable.find_all('tr')[1:]: # to skip heading
			    rowElements = tr.find_all('td')
			    attackAnchor = rowElements[1].find_all("a")[0] # to get the attack name and link to explore
			    link = str(attackAnchor.get("href"))

			    attackMultiImagesLinks[move].append((link,str(base_poke)))
			print((link,str(base_poke)))
			print()

			save_obj(attackMultiImagesLinks,"attackMultiImagesLinks")
		except:
			continue
