from entities import entities
import nltk

class document:
    def __init__(self, title=None, text=None):
        if title is None:
            title = []
        if text is None:
            text = []
        self.title = title
        self.text = text
        
    def getNamedEntities(self):
        self.entities = entities(self.text)

    def getWords(self):
        self.words = set([word.lower() for word in nltk.word_tokenize(self.text)])

