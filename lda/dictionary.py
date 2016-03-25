class dictionary:
        
    def __init__(self):
        self.words = set([])
        self.stopwords = set([])
    
    def addDocument(self, document):
        if not document.hasWordsAttribute():
            document.createWords()
        self.words.update(self._lowerList(document.words))
    
    def addCollection(self, collection):
        for document in collection.documents:
            self.addDocument(document)

    def addStopwords(self, listStopwords):
        self.stopwords.update(self._lowerList(listStopwords))
        self.removeStopwords()

    def removeStopwords(self):
        [self.words.discard(stopword) for stopword in self.stopwords]


    def _lowerList(self, wordList):
        return [word.lower() for word in wordList]


