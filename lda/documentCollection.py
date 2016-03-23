import urllib2
import docLoader
from document import document
import nlpProcessing as nlp
import namedEntityRecognition as ner
from entities import entities

class documentCollection:
    def __init__(self, path):
        try:
            urllib2.urlopen(urllib2.Request(path)) 
            (titles, texts) = docLoader.loadCouchdb(path)
        except:
            titles = ['']
            texts = ['']
        self.documents = [document(title, text) for title, text in zip(titles, texts)]
            
    def createDictionary(self, rmStopwords=True):
        self.dictionary = nlp.tokenizeCollection(self.documents)
        if rmStopwords:
            self.dictionary = nlp.removeStopwords(self.dictionary)
    
    def getNamedEntities(self):
        for document in self.documents:
            document.getNamedEntities()
        self.entities = entities('')
        for tag in self.documents[0].entities.__dict__.keys():
            self.entities.addEntities(tag, set().union(*[getattr(document.entities, tag) for document in self.documents]))
    
    def addEntitiesToDict(self):
        print "Not yet implemented"


