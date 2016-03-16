import json
import urllib
import pickle

# load couchdb data from URL
def loadCouchdb(path):
    dat = json.load(urllib.urlopen(path))
    rows = dat['rows']
    docs = list(map((lambda doc: doc['value']['Text']),rows))
    titles = list(map((lambda doc: doc['value']['Title']),rows))
    return zip(titles, docs)

# store data as txt file
def storeAsTxt(dat):
    with open('fullTextDocs.txt', 'wb') as f:
        pickle.dump(docs, f)

# Load documents from path to list
def loadTxt(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

