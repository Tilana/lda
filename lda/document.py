from entities import entities
import nltk

class document:
    
    def __init__(self, title=None, text=None):
        self.title = title
        self.text = text 
       
    def createEntities(self):
        self.entities = entities(self.text)

    def createWords(self):
        self.words = self._tokenizeDocument()

    def hasWordsAttribute(self):
        return hasattr(self, 'words')

    def _tokenizeDocument(self):
        return set([word.lower() for word in nltk.word_tokenize(self.text)])


