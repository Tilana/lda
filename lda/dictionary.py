class dictionary:
        
    def __init__(self):
        self.words = set([])
        self.stopwords = set([])
    
    def addDocument(self, document):
        if not document.hasWordsAttribute():
            document.createWords()
        self.words = self.words.union(document.words)
    
    def addCollection(self, collection):
        for document in collection.documents:
            self.addDocument(document)

