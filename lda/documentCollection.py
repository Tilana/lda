import urllib2
import docLoader
import nlpProcessing as nlp
import namedEntityRecognition as ner

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
        self.dictionary = nlp.tokenizeCollection(self.documents)
        if rmStopwords:
            self.dictionary = nlp.removeStopwords(self.dictionary)
		
    def getNamedEntities(self):
        self.namedEntities = [ner.getNamedEntities(document) for document in self.documents]

    def addEntitiesToDict(self):
        print "Not yet implemented"


