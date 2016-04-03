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

    def createTokens(self, stoplist=[]):
        self.tokens= self._tokenizeDocument()
        self.removeStopwords(stoplist)
        self.includeEntities()

    def lemmatizeTokens(self):
        wordnet = WordNetLemmatizer()
        lemmatizedTokens = set([wordnet.lemmatize(wordnet.lemmatize(word, 'v')) for word in self.tokens])
        self.tokens = lemmatizedTokens 

    def deleteSpecialCharacterTokens(self):
        self.specialCharacters =  [word for word in self.tokens if re.match(r'.*[~!\^@#%&\".,-?\/\_\(\)\{\}\[\]:;\*\"].*', word)]
        for specialChar in self.specialCharacters:
            self.tokens.remove(specialChar)

    def hasTokenAttribute(self):
        return hasattr(self, 'tokens')
    
    def _tokenizeDocument(self):
        return [word.lower() for word in nltk.word_tokenize(self.text)]

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



