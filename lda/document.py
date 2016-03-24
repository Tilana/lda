from entities import entities
import nltk

class document:
    
    def __init__(self, title=None, text=None):
        self.title = title
        self.text = text 
       
    def getNamedEntities(self):
        self.entities = entities(self.text)

    def createWords(self):
        self.words = set([word.lower() for word in nltk.word_tokenize(self.text)])

    def hasWordsAttribute(self):
        return hasattr(self, 'words')

