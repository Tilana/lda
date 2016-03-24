from entities import entities

class dictionary:
        
    def __init__(self):
        self.words = []
        self.stopwords = []

    def addDocument(self, document):
        if not document.hasWordsAttribute():
            document.createWords()
        self.words = self.words.union(document.word)

    def addCollection(self, collection):
        for document in collection:
            adDocument(self, document)

