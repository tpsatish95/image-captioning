import urllib.request
import simplejson
import time
import pickle
import os

def save_obj(obj, name ):
    with open( name + ".pkl" , 'wb') as f:
        pickle.dump(obj, f,  protocol=2)

fetcher = urllib.request.build_opener()


YOUR_API_KEY = "AIzaSyDhMnNNzDLVRBKEgoCwsKcRzcYMcq4rZaQ"
CX = "006884488164293224233:lblrjk65gqe"
NUM = 10 # 10 results per request
# 100 calls per day free (top 100 images are only accessible)

searchTerms = [i.strip() for i in open("Kanto.txt").readlines()]
numberOfImages = 10

urls = []
for searchTerm in searchTerms:
	sT = searchTerm.lower()
	os.makedirs("./Images/" + sT.lower())
	searchTerm = urllib.request.quote(searchTerm.lower())  # for non-ascii encoding of search term
	count = 0
	for startIndex in range(1, numberOfImages, NUM):
		while True:
			searchUrl = "https://www.googleapis.com/customsearch/v1?q=" + searchTerm + "&cx=" + CX + "&num=" + str(NUM) + "&start=" + str(startIndex) + "&key=" + YOUR_API_KEY+ "&alt=json&searchType=image"
			print(searchUrl)
			# searchUrl = "https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + searchTerm + "&start=" + str(startIndex) + "&userip=192.168.1.2"
			f = fetcher.open(searchUrl)
			deserialized_output = simplejson.load(f)
			# print(deserialized_output)
			# break
			if None == deserialized_output["items"]:
			    print("Retrying " + str(startIndex))

			    # Sleep for two second to prevent IP blocking from Google
			    time.sleep(3)

			    continue

			else:
			    for temp in deserialized_output["items"]:

			        urls.append(temp["link"])
			        u = temp["link"]
			        try:
			            image = urllib.request.urlopen(u.strip()).read()
			            print(u)
			            f = open("./Images/" + sT + "/" + str(count) + "." + u.split(".")[len(u.split("."))-1].split("?")[0].split("/")[0],'wb')
			            f.write(image)
			            f.close()
			        except Exception as e:
			            print("Failed !")
			            print(e)
			            continue

			        count += 1
			        save_obj(urls,"./Images/urls")

			        # Sleep for two second to prevent IP blocking from Google
			        time.sleep(3)

			    print(startIndex)
			    break
