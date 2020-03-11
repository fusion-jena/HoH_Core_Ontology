import requests
import json
import os
from pprint import pprint


#Search parameters and API-key
search_url = "http://data.bioontology.org/search?q="
parameters = "&exact_match=true"
api_key = "&apikey=d3a3cc21-3dc0-435c-85e3-ae56ae245a83"

# Read the term file and write the values to list
path = os.path.join(os.path.dirname(__file__), 'bio_found_terms_with_definitions.txt')
terms_file = open(path, "r")
lines = terms_file.readlines()
terms = [line.rstrip() for line in lines]

# Write the search results to list
search_results = []
for term in terms:
    print(term)
    term = term.replace(" ", "%20")
    r = requests.get(search_url+term+parameters+api_key)
    data = r.json()['collection']
    #data = r.json()
    search_results.append(data)

# And save it to text file
f = open('terms_definitions.txt', 'w')
json.dump(search_results, f)
f.close()
