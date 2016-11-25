import urllib.request
from bs4 import BeautifulSoup
import pickle

def save_obj(obj, name ):
    with open( name + '.pkl', 'wb') as f:
        pickle.dump(obj, f,  protocol=2)

def load_obj(name ):
    with open( name + '.pkl', 'rb') as f:
        return pickle.load(f)

attack_base = load_obj("bulbaAttackLinksDict")

try:
	attackImagesLinks = load_obj("attackImagesLinks")
	none = load_obj("noImagesAttacks")
except:
	attackImagesLinks = dict()
	none = []

# get undone moves
attacks = list((set(attack_base.keys()) - set(attackImagesLinks.keys())) - set(none))

print(len(attacks))

for move in attacks:
	print(move)
	base_link = attack_base[move]
	print(base_link)

	limit = 3
	j = 0
	while j < limit:
		try:
			with urllib.request.urlopen(base_link) as url:
				html_doc = url.read().decode("utf-8")

				# make a soup
				soup = BeautifulSoup(html_doc, 'html.parser')
				result = soup.findAll("span", { "id" : "In_the_anime" })

				if len(result) == 0:
					print("retrying")
					j += 1
					if j == 3:
						none.append(str(move))
					continue
				else:
					j = limit+1

				h2 = result[0].parent
				test = h2.findNextSibling(text=None)

				# print(test)

				if test.name == "table" :
					for tr in test.find_all('tr')[:1]: # first row links
						rowElements = tr.find_all('td')
						links = []
						for attackAnchor in rowElements:
							link = "http://bulbapedia.bulbagarden.net" + str(attackAnchor.find_all("a")[0].get("href"))

							links.append(link)
						# print(links)
					for tr in test.find_all('tr')[1:2]: # second row pokemon name
						rowElements = tr.find_all('td')
						pokeNames = []
						for attackAnchor in rowElements:
							text = attackAnchor.b.text.lower()
							pokeNames.append(str(text))

					print("Table")
					attackImagesLinks[move] = list(zip(links,pokeNames))
					print(attackImagesLinks[move])
					print()
				else:
					links = []
					pokeNames = []
					try:
						for i in ["In_the_main_series","In_Pok.C3.A9mon_Origins"]:

							h3 = soup.findAll("span", { "id" : i })[0].parent
							table = h3.findNextSibling(text=None)

							for tr in table.find_all('tr')[:1]: # first row links
								rowElements = tr.find_all('td')
								for attackAnchor in rowElements:
									link = "http://bulbapedia.bulbagarden.net" + str(attackAnchor.find_all("a")[0].get("href"))

									links.append(link)
								# print(links)
							for tr in table.find_all('tr')[1:2]: # second row pokemon name
								rowElements = tr.find_all('td')
								for attackAnchor in rowElements:
									text = attackAnchor.b.text.lower()
									pokeNames.append(str(text))

						attackImagesLinks[move] = list(zip(links,pokeNames))
						print("No Table")
						print(attackImagesLinks[move])
						print()
					except:
						none.append(str(move))

			save_obj(none,"noImagesAttacks")
			save_obj(attackImagesLinks,"attackImagesLinks")
		except:
			none.append(move)
			save_obj(none,"noImagesAttacks")
