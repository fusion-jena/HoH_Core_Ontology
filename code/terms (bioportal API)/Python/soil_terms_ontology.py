import requests
import json
import os
from pprint import pprint



search_url = "http://data.bioontology.org/search?q="
parameters = "&exact_match=true"
api_key = "&apikey=d3a3cc21-3dc0-435c-85e3-ae56ae245a83"

path = os.path.join(os.path.dirname(__file__), 'soil_terms.txt')
terms_file = open(path, "r")
lines = terms_file.readlines()
terms = [line.rstrip() for line in lines]
ontologies = []
for term in terms:
    term = term.replace(" ", "%20")
    r = requests.get(search_url+term+parameters+api_key)
    data = r.json()
    iterations = data['totalCount']
    term = term.replace("%20", " ")
    print(term)
    for i in range(iterations):
        try:
            temp = []          
            temp.append(term)
            ontology = data['collection'][i]['links']['ontology']
            temp.append(ontology)
            ontologies.append(temp)
        except Exception:
            pass
        
with open ('soil_terms_and_ontologies.txt', 'w') as fo:
   for d in ontologies:
     fo.write(str(d) + '\n')

