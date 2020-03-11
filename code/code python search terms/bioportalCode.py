import urllib.request, urllib.error, urllib.parse
import json
#import os
from pprint import pprint

REST_URL = "http://data.bioontology.org"
API_KEY = "2b521c96-6fe2-43c2-8dfc-ae98d4eae0fa"

PATH2 = "additionalFilesForCode/search_results.txt"
PATH3="additionalFilesForCode/search_results_filtered.txt"
PATH4="additionalFilesForCode/import_filtered_results.txt"

def get_json(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [("Authorization", "apikey token=" + API_KEY)]
    return json.loads(opener.open(url).read())

## Get list of search terms
#terms = []
#def getListOfSearchTerms(terms):
    #path = os.path.join(os.path.dirname(__file__), "classes_search_terms.txt")
    #terms_file = open(path, "r")
    #for line in terms_file:
    #    terms.append(line)

# Do a search for every term
def searchForTerm(search_results, term):
    #for term in terms:
    #    search_results.append(get_json(REST_URL + "/search?q=" + term)["collection"])
    search_results.append(get_json(REST_URL + "/search?q=" + term)["collection"])

# Print the results
def saveResults(search_results):
    search_file = open(PATH2, "w")
    for result in search_results:
        try:
            pprint(result, search_file)
        except UnicodeEncodeError:
            continue
    search_file.close()
    
#extracting what I need
def extractNeededInfo():
    search_file = open(PATH2, "r")
    filtered_file = open(PATH3, "w")
    for line in search_file:
        if "{\'@context\': {\'@vocab\':" in line:
            filtered_file.write("==========NEXT============\n")
        elif "\'@id\':" in line:
            filtered_file.write(line.lstrip().replace("\'", "").replace(",",""))
        elif "\'prefLabel\':" in line:
            if "http://" not in line:
                filtered_file.write(line.lstrip().replace("\'", "").replace(",",""))
        elif "\'definition\':" in line:
            definition_line = ""
            if "http://" not in line:
                if "\']," not in line:
                    copy_line = line.lstrip().replace("\'", "").replace(",","").replace("\n","").replace("[","").replace("]","").replace(";","")
                    while "]," not in definition_line:    
                        definition_line = search_file.readline()        
                        copy_line = copy_line + definition_line.lstrip().replace("\'", "").replace(",","").replace("\n","").replace("[","").replace("]","").replace(";","")
                    filtered_file.write(copy_line + "\n")
                else:
                    filtered_file.write(line.lstrip().replace("\'", "").replace(",","").replace("[","").replace("]","").replace(";",""))
    #            filtered_file.write(line.lstrip().replace("\'", "").replace(",",""))
        elif "\'ontology\':" in line:
            if "http://data.bioontology.org/metadata/Ontology" not in line:
                filtered_file.write(line.lstrip().replace("\'", "").replace(",",""))
        elif "}," in line:
            filtered_file.write("\n")
    search_file.close()
    filtered_file.close()


def createImportableFile():
    filtered_file = open(PATH3, "r")
    import_file = open(PATH4,"w")
    
    import_file.write("term~uid~label~definition~ontology")
    insert_line=["","","","","",""]
    #next einbauen, damit pro next in einem list element
    for line in filtered_file:
        if "==========NEXT============" in line:
            strInsert = str(insert_line).replace(", ","~").replace("\'","").replace("[","").replace("]","")
            import_file.write(strInsert + "\n")
            insert_line=["","","","","",""]
        if "@id: " in line:
            insert_line[1] = line.replace("@id: ","").replace("\n","")# + ";"
        elif "ontology: " in line:
            insert_line[4] = line.replace("ontology: ","").replace("\n","")# + ";"
        elif "prefLabel: " in line:
            insert_line[2] = line.replace("prefLabel: ","").replace("\n","")# + ";"
        elif "definition: " in line:
            insert_line[3] = line.replace("definition: ","").replace("\n","")# + ";"
    strInsert = str(insert_line).replace(", ","~").replace("\'","").replace("[","").replace("]","")
    import_file.write(strInsert + "\n")
    filtered_file.close()
    import_file.close()

#main
search_results = []
searchForTerm(search_results, "biodiversity")
print("1 fertig")
saveResults(search_results)
print("2 fertig")
extractNeededInfo()
print("3 fertig")
createImportableFile()
print("4 fertig")