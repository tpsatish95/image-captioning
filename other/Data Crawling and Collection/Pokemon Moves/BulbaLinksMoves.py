from bs4 import BeautifulSoup
import pickle

def save_obj(obj, name ):
    with open( name + '.pkl', 'wb') as f:
        pickle.dump(obj, f)

attackLinks = dict()

html_doc =  open("PokeMoves.html","r")
# make a soup
soup = BeautifulSoup(html_doc.read(), 'html.parser')
divContent = soup.findAll("div", { "id" : "mw-content-text" })[0]
mainTable = divContent.find_all("table")[0].findAll("table")[0]
for tr in mainTable.find_all('tr')[1:]: # to skip heading
    rowElements = tr.find_all('td')
    attackAnchor = rowElements[1].find_all("a")[0] # to get the attack name and link to explore
    attackName = str(attackAnchor.contents[0])
    link = "http://bulbapedia.bulbagarden.net" + str(attackAnchor.get("href"))

    attackLinks[attackName] = link

print(attackLinks)


save_obj(attackLinks,"bulbaAttackLinksDict")
