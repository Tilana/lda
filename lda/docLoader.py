import json
import urllib
import pickle
import os
import pandas


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


def loadCsvFile(path):
    data = pandas.read_csv(path) #, encoding='utf8')
    titles = list(data['Title'])
    docs = list(data['Abstract'])
    titles = [removeSpecialChars(title) for title in titles]
    docs = [removeSpecialChars(text) for text in docs]
    return (titles, docs)


def removeSpecialChars(text, verbosity=0):
    encodedText = []
    for word in text.split():
        try:
            encodedWord = word.encode('utf8')
            encodedText.append(encodedWord)
        except:
            if verbosity:
                print "Failed Encoding: ", word
            pass
    return " ".join(encodedText)




def storeAsTxt(dat, path):
    with open(path, 'wb') as f:
        pickle.dump(dat, f)


def loadTxt(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

