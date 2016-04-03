import re
from nltk.stem import WordNetLemmatizer

class dictionary:
        
    def __init__(self):
        self.words = set([])
        self.stopwords = set([])
        self.specialCharacters = set([])
    
    def addDocument(self, document):
        if not document.hasTokenAttribute():
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
    
    def deleteSpecialCharacterTokens(self):
        self.specialCharacters =  set([word for word in self.words if re.match(r'.*[~!\^@#%&\".,-?\/\_\(\)\{\}\[\]:;\*\"].*', word)])
        for specialChar in self.specialCharacters:
            self.words.remove(specialChar)
    
    def lemmatize(self):
        wordnet = WordNetLemmatizer()
        lemmatizedTokens = set([wordnet.lemmatize(wordnet.lemmatize(word, 'v')) for word in self.words])
        self.lemmaDict = lemmatizedTokens 


