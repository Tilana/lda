import urllib2
import docLoader
import nlpProcessing as nlp

class documentCollection:
    def __init__(self, path):
        try:
            urllib2.urlopen(urllib2.Request(path)) 
            (titles, documents) = docLoader.loadCouchdb(path)
        except:
            titles = []
            documents = []
        self.titles = titles
        self.documents = documents
    
    def createDictionary(self, rmStopwords=True):
        self.dictionary = nlp.tokenizeColl(self.documents)
        if rmStopwords:
            self.dictionary = nlp.removeStopwords(self.dictionary)
		
    def getNamedEntities(self):
        self.namedEntities = nlp.getNamedEntities(self.documents)

