from PIL import Image
import networkx as nx

im = Image.open("test.png") 
pix = im.load()

G = nx.Graph()

for i in range(im.size[0]):
	for j in range(im.size[1]):
		
		print (str(i) + "," + str(j))

		currentPixel = pix[i,j]

		print (currentPixel)

		if(currentPixel[3] != 0):
			
			currentPixel = currentPixel[:3]

			print(currentPixel)
			
			print(G.nodes())
			print(G.edges())

			if(currentPixel not in G.nodes()): #TODO: check if you can use a hash instead of not in
				G.add_node(currentPixel, count=1)
				#print(G.node[currentPixel])
			else:
				#print(G[currentPixel])
				G.node[currentPixel]['count'] += 1

			for a in range(i-1, i+2):
				for b in range(j-1, j+2):
					

					if((a in range(im.size[0])) and (b in range(im.size[1]))):
						
						neighborPixel = pix[a,b]
						
						if(not(a==i and b==j) and neighborPixel[3]!= 0):
							
							neighborPixel = neighborPixel[:3]

							if(neighborPixel not in G.nodes()):
								G.add_node(neighborPixel, count=0)

							if(((currentPixel, neighborPixel) not in G.edges()) and ((neighborPixel, currentPixel) not in G.edges()) and currentPixel != neighborPixel):
								G.add_edge(currentPixel, neighborPixel, weight=1) 
							elif(currentPixel != neighborPixel):
								G[currentPixel][neighborPixel]['weight'] += 1

							

print (G.nodes())

for node in G.nodes():
	print (G.node[node])

#print (G.edges())
print (list(G.edges_iter(data=True)))


