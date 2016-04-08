import re
import utils
from nltk.stem import WordNetLemmatizer
from gensim import corpora

class dictionary:
        
    def __init__(self):
        self.words = set([])
        self.stopwords = set([])
        self.specialCharacters = set([])
        self.ids = corpora.Dictionary()
    
    def createDictionaryIds(self):
        self.ids.add_documents([self.words])

    def setDictionary(self, wordList=None):
        self.words = set(self._lowerList(wordList))

    def addDocument(self, document):
        if not document.hasTokenAttribute():
            document.createTokens()
        self.words.update(self._lowerList(document.tokens))
    
    def addCollection(self, collection):
        for document in collection:
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
    
    def findSpecialCharTokens(self, specialCharacters, collection):
        self.specialCharacters =  set([word for word in self.words if utils.containsAny(word, specialCharacters)])
#        [self.specialCharacters.update(document.specialCharacters) for document in collection if document.hasSpecialCharAttribute]

    def getOriginalWords(self, collection):
        [self.original.update(document.original) for document in collection if document.hasOriginalAttribute]
    
    
    def removeSpecialChars(self):
        for specialChar in self.specialCharacters:
            self.words.discard(specialChar)
    
    def lemmatize(self):
        wordnet = WordNetLemmatizer()
        self.original = self.words
        self.words = set([wordnet.lemmatize(wordnet.lemmatize(word, 'v')) for word in self.words])
    
    def removeShortWords(self, threshold=1):
        shortWords = [word for word in self.words if len(word)<=threshold]
        self.words = self.words.difference(shortWords)

