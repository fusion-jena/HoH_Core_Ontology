import requests
import json
import os
from pprint import pprint



search_url = "http://data.bioontology.org/search?q="
parameters = "&exact_match=true"
api_key = "&apikey=d3a3cc21-3dc0-435c-85e3-ae56ae245a83"

path = os.path.join(os.path.dirname(__file__), 'bio_found_terms_with_definitions.txt')
terms_file = open(path, "r")
lines = terms_file.readlines()
terms = [line.rstrip() for line in lines]
definitions = []
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
            definition = data['collection'][i]['definition']
            temp.append(definition)
            definitions.append(temp)
        except Exception:
            pass
        
with open ('term_and_definition.txt', 'w') as fo:
   for d in definitions:
     fo.write(str(d) + '\n')

