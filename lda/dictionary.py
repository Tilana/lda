class dictionary:
        
    def __init__(self):
        self.words = set([])
        self.stopwords = set([])
    
    def addDocument(self, document):
        if not document.hasWordsAttribute():
            document.createTokens()
        self.words.update(self._lowerList(document.tokens))
    
    def addCollection(self, collection):
        for document in collection.documents:
            self.addDocument(document)

    def addStopwords(self, listStopwords):
        self.stopwords.update(self._lowerList(listStopwords))
        self.removeStopwords()

    def removeStopwords(self):
        [self.words.discard(stopword) for stopword in self.stopwords]

    def addWords(self, wordList):
        [self.words.add(word) for word in self._lowerList(wordList) if word not in self.stopwords]


    def _lowerList(self, wordList):
        return [word.lower() for word in wordList]



