from Entities import Entities
import utils
import nltk
from nltk.stem import WordNetLemmatizer

class Document:
    
    def __init__(self, title=None, text=None):
        self.title = title
        self.text = text 
        self.entities = Entities()
       
    def createEntities(self, frequency=1):
        self.entities = Entities(self.text)

    def createTokens(self):
        self.tokens= self._tokenizeDocument()

    def prepareDocument(self, lemmatize=True, includeEntities=True, stopwords=None, specialChars=None, removeShortTokens=True, threshold=2, whiteList = None):
        self.text = self.text.decode('utf8', 'ignore')
        self.tokens = self._tokenizeDocument()
        self.original = self.tokens
        if stopwords is None:
            stopwords = []
        if specialChars is None:
            specialChars = []
        if whiteList is None:
            whiteList = list(set(self.tokens) - set(stopwords))

        if lemmatize:
            self.lemmatizeTokens()
        self.tokens = [token for token in self.tokens if (token not in stopwords) and (token in whiteList)]

        self.tokens = [token for token in self.tokens if not utils.containsAny(token, specialChars) and len(token) > threshold]
        if includeEntities:
            if self.entities.isEmpty():
                self.createEntities()
            self.appendEntities()

    def lemmatizeTokens(self):
        wordnet = WordNetLemmatizer()
        self.original = self.tokens
        self.tokens = [wordnet.lemmatize(wordnet.lemmatize(word, 'v')) for word in self.tokens]

    def findSpecialCharacterTokens(self, specialCharacters):
        self.specialCharacters =  [word for word in self.tokens if utils.containsAny(word, specialCharacters)]

    def removeSpecialCharacters(self):
        for specialChar in self.specialCharacters:
            self.tokens.remove(specialChar)

    def hasTokenAttribute(self):
        return hasattr(self, 'tokens')

    def hasOriginalAttribute(self):
        return hasattr(self, 'original')
    
    def hasSpecialCharAttribute(self):
        return hasattr(self, 'specialCharacters')

    def setTopicCoverage(self, coverage, name):
        sortedCoverage = utils.sortTupleList(coverage)
        self.setAttribute(('%sCoverage' % name), sortedCoverage)
   
    def _tokenizeDocument(self):
        return [word.lower() for word in nltk.word_tokenize(self.text)]

    def removeShortTokens(self, threshold=1):
        shortWords = [word for word in self.tokens if len(word)<=threshold]
        self.tokens = [word for word in self.tokens if word not in shortWords]


    def removeStopwords(self, stoplist):
        self.tokens = [word for word in self.tokens if word not in stoplist]

    def appendEntities(self):
        entityList = self.entities.getEntities()
        for entity in entityList:
            for frequency in range(0, entity[1]):
                self.tokens.append(entity[0].encode('utf8'))
                self.correctTokenOccurance(entity[0])

    def correctTokenOccurance(self, entity):
        [self.tokens.remove(word) for word in entity.split() if word in self.tokens]

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def setAttribute(self, name, value):
        setattr(self, name, value)


