from bs4 import BeautifulSoup
import urllib.request


page1 = open("initial_bulbapedia_pages/page1ol.html",'r').read()
page2 = open("initial_bulbapedia_pages/page2ol.html", 'r').read()

urls = open("urls.txt", 'w')

soup = BeautifulSoup(page1, 'html.parser')
for listitem in soup.find_all('li'):
	urls.write(listitem.a.get('href') + '\n')

soup = BeautifulSoup(page2, 'html.parser')
for listitem in soup.find_all('li'):
	urls.write(listitem.a.get('href') + '\n')


