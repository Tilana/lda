from entities import entities
import utils
import re
import nltk
from nltk.stem import WordNetLemmatizer

class document:
    
    def __init__(self, title=None, text=None):
        self.title = title
        self.text = text 
        self.entities = entities()
       
    def createEntities(self):
        self.entities = entities(self.text)

    def createTokens(self):
        self.tokens= self._tokenizeDocument()

    def prepareDocument(self, lemmatize=True, includeEntities=True, stopwords=None, specialChars=None, removeShortTokens=True, threshold=1):
        self.tokens = self._tokenizeDocument()
        self.original = self.tokens
        if lemmatize:
            self.lemmatizeTokens()
        if includeEntities:
            if self.entities.isEmpty():
                self.createEntities()
            self.includeEntities()
        if stopwords is not None:
            self.removeStopwords(stopwords)
        if specialChars is not None:
            if not self.hasSpecialCharAttribute():
                self.findSpecialCharacterTokens(specialChars)
            self.removeSpecialCharacters()
        if removeShortTokens:
            self.removeShortTokens(threshold)

    def lemmatizeTokens(self):
        wordnet = WordNetLemmatizer()
        self.original = self.tokens
        self.tokens = [wordnet.lemmatize(wordnet.lemmatize(word, 'v')) for word in self.tokens]

    def findSpecialCharacterTokens(self, specialCharacters):
        self.specialCharacters =  set([word for word in self.tokens if utils.containsAny(word, specialCharacters)])

    def removeSpecialCharacters(self):
        for specialChar in self.specialCharacters:
            self.tokens.remove(specialChar)

    def hasTokenAttribute(self):
        return hasattr(self, 'tokens')

    def hasOriginalAttribute(self):
        return hasattr(self, 'original')
    
    def hasSpecialCharAttribute(self):
        return hasattr(self, 'specialCharacters')
   
    def _tokenizeDocument(self):
        self.text = u'self.text'
        return [word.lower() for word in nltk.word_tokenize(self.text)]

    def removeShortTokens(self, threshold=1):
        shortWords = [word for word in self.tokens if len(word)<=threshold]
        self.tokens = [word for word in self.tokens if word not in shortWords]


    def removeStopwords(self, stoplist):
        self.tokens = [word for word in self.tokens if word not in stoplist]

    def includeEntities(self):
        entityList = self.entities.getEntities()
        for entity in entityList:
            ent = entity.lower().split()
            lengthEntity = len(ent)
            if lengthEntity>1:
                wordInd = []
                for pos in range(lengthEntity):
                   indices = [index for index, word in enumerate(self.tokens) if word == ent[pos]]
                   wordInd = wordInd + indices
                distList = utils.listDifference(sorted(wordInd))
                count = 1
                for elem in distList:
                    if elem[0]==1:
                        count+=1
                        if count==lengthEntity:
                            self.tokens[elem[1]+1] = ' '.join(self.tokens[elem[1]+2-lengthEntity:elem[1]+2])
                            del self.tokens[elem[1]+2-count:elem[1]+1]

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def setAttribute(self, name, value):
        setattr(self, name, value)



