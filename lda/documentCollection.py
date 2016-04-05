import urllib2
import docLoader
from document import document
from entities import entities
from dictionary import dictionary

class documentCollection:
    def __init__(self, path=None):
        if path is not None:
            urllib2.urlopen(urllib2.Request(path)) 
            (titles, texts) = docLoader.loadCouchdb(path)
        else:
            titles = ['']
            texts = ['']
        self.documents = self._createDocumentList(titles, texts)
#        self.dictionary = dictionary()

#    def createDictionary(self):
#        self.dictionary.addCollection(self)

#    def prepareDocumentCollection(self, lemmatize=True, createEntities=True, includeEntities=True, removeStopwords=True, stopwords=None, removeSpecialChars=True, specialChars = None):
#        for document in self.documents:
#            document.prepareDocument(lemmatize, includeEntities, removeStopwords, stopwords, removeSpecialChars, specialChars)
#        self.createEntities()

    
#    def createEntities(self):
#        [document.createEntities for document in self.documents if document.entities.isEmpty()]
#        self.entities = entities('')
#        self._addDocumentEntities()
            
    def _createDocumentList(self, titles, texts):
        return [document(title, text) for title, text in zip(titles, texts)]

#    def _addDocumentEntities(self):
#        for tag in self.documents[0].entities.__dict__.keys():
#            self.entities.addEntities(tag, set().union(*[getattr(document.entities, tag) for document in self.documents]))
#
