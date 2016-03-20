import docLoader
import nlpProcessing as nlp

class documentCollection:
    def __init__(self, path):
        (titles, docs) = docLoader.loadCouchdb(path)
        self.titles = titles
        self.docs = docs
    
    def createDict(self, rmStopwords=True):
        self.dict = nlp.tokenizeColl(self.docs)
        if rmStopwords:
            self.dict = nlp.removeStopwords(self.dict)
		
    def getNamedEntities(self):
        self.namedEntities = nlp.getNamedEntities(self.docs)

