# -*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup
import pickle
from collections import defaultdict

searchTerms = [i.strip() for i in open("Kanto.txt").readlines()]

def save_obj(obj, name ):
    with open( name + '.pkl', 'wb') as f:
        pickle.dump(obj, f,  protocol=2)

def load_obj(name ):
    with open( name + '.pkl', 'rb') as f:
        return pickle.load(f)


pokemon_attack_map = defaultdict(set)
notD = []

# searchTerms = ['Metapod', 'Butterfree', 'Pikachu', 'Nidoran%E2%99%80', 'Nidorina', 'Nidoqueen', 'Nidorino', 'Nidoking', 'Venonat', 'Venomoth', 'Mankey', 'Primeape', 'Kadabra', 'Alakazam', 'Cubone', 'Marowak', 'Chansey', 'Tangela', 'Mr._Mime', 'Scyther', 'Pinsir', 'Gyarados', 'Eevee', 'Vaporeon', 'Jolteon', 'Flareon']
# pokemon_attack_map = load_obj("pokemon_attack_map")

for poke in searchTerms:
	link = "http://bulbapedia.bulbagarden.net/wiki/"+poke+"_(Pok%C3%A9mon)/Generation_I_learnset"
	print(link)
	try:
		# base_link = "http://bulbapedia.bulbagarden.net/wiki/Bulbasaur_(Pok%C3%A9mon)/Generation_I_learnset" # test link
		url = urllib.request.urlopen(link)
		html_doc = url.read().decode("utf-8")

		# make a soup
		soup = BeautifulSoup(html_doc, 'html.parser')

		mainTable = soup.findAll("table", { "class" : "sortable" })[0]

		print(poke)
		# print(mainTable)
		for tr in mainTable.find_all('tr')[1:]: # to skip heading
			rowElements = tr.find_all('td')
			try:
				attackAnchor = rowElements[1].find_all("a")[0] # to get the attack name and link to explore
				# print (attackAnchor)
				move = str(attackAnchor.span.text.lower())

				pokemon_attack_map[poke].add(move)
			except:
				attackAnchor = rowElements[2].find_all("a")[0] # to get the attack name and link to explore
				# print (attackAnchor)
				move = str(attackAnchor.span.text.lower())

				pokemon_attack_map[poke].add(move)
		print(pokemon_attack_map[poke])
		print()
		# break

		save_obj(pokemon_attack_map,"pokemon_attack_map")
	except Exception as e:
		print(e)
		notD.append(poke)
		continue

print(notD)
