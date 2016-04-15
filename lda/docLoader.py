import json
import urllib
import pickle
import os


def loadCouchdb(path):
    dat = json.load(urllib.urlopen(path))
    rows = dat['rows']
    docs = list(map((lambda doc: doc['value']['Text']),rows))
    titles = list(map((lambda doc: doc['value']['Title']),rows))
    return (titles, docs)


def loadTxtFiles(path):
    titles = [txtfile for txtfile in os.listdir(path)]
    docs = [open(path+'/'+txtfile).read().decode('utf8') for txtfile in os.listdir(path)]
    return (titles, docs)


# store data as txt file
def storeAsTxt(dat, path):
    with open(path, 'wb') as f:
        pickle.dump(dat, f)

# Load documents from path to list
def loadTxt(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

