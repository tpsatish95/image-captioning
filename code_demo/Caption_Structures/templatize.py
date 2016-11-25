from collections import defaultdict
import pickle

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, protocol = 2)

lines = open("templates.txt","r").readlines()

pA = "$pokemonA"
pB = "$pokemonB"

template = defaultdict(set)

for line in lines:
	if pA in line and pB in line:
		template["two"].add(line.strip().replace(pA,"$PA").replace(pB,"$PB").replace("$attackC","$A"))
	elif pA in line or pB in line:
		template["one"].add(line.strip().replace(pA,"$PA").replace("$attackB","$A"))

print(list(template["two"])[0])
save_obj(template,"random_templates_generator")
