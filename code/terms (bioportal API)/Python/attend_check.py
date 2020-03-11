import requests
import json
import os
from pprint import pprint


#Search parameters and API-key
search_url = "http://data.bioontology.org/search?q="
parameters = "&exact_match=true"
api_key = "&apikey=d3a3cc21-3dc0-435c-85e3-ae56ae245a83"

# Read the term file and write the values to list
path = os.path.join(os.path.dirname(__file__), 'classes_search_terms.txt')
terms_file = open(path, "r")
lines = terms_file.readlines()
terms = [line.rstrip() for line in lines]

# Write the search results to list
search_results = []
for term in terms:
    term = term.replace(" ", "%20")
    r = requests.get(search_url+term+parameters+api_key)
    data = r.json()['collection']
    #data = r.json()
    if (len(data) != 0):
        term = term.replace("%20", " ")
        print(term)
        search_results.append(term)

# And save it to text file
f = open('output.txt', 'w')
json.dump(search_results, f)
f.close()
