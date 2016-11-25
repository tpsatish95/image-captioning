from bs4 import BeautifulSoup
import pickle
# import sys

# sys.setrecursionlimit(50000)

def save_obj(obj, name ):
    with open( name + '.pkl', 'wb') as f:
        pickle.dump(obj, f,  protocol=2)

attackLinks = dict()

html_doc =  open("PokeMoves.html","r")
# make a soup
soup = BeautifulSoup(html_doc.read(), 'html.parser')
divContent = soup.findAll("div", { "id" : "mw-content-text" })[0]
mainTable = divContent.find_all("table")[0].findAll("table")[0]
# print(mainTable)
for tr in mainTable.find_all('tr')[1:]: # to skip heading
    rowElements = tr.find_all('td')
    attackAnchor = rowElements[1].find_all("a")[0] # to get the attack name and link to explore
    # print (attackAnchor)
    attackName = attackAnchor.contents[0]
    link = "http://bulbapedia.bulbagarden.net" + attackAnchor.get("href")

    attackLinks[attackName] = link
    # print(link)

save_obj(attackLinks,"bulbaAttackLinksDict")
