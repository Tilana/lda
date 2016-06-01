#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Entities import Entities
import utils
from nltk.stem import WordNetLemmatizer
from gensim import corpora
import matplotlib.pyplot as plt

class Dictionary:
        
    def __init__(self):
        self.words = set([])
        self.stopwords = set([])
        self.specialCharacters = set([])
        self.ids = corpora.Dictionary()
    
    def createDictionaryIds(self, collection):
        for doc in collection:
            if not doc.hasTokenAttribute():
                doc.createTokens()
            self.ids.add_documents([doc.tokens])
    
    def setSpecialCharacters(self, collection):
        [self.specialCharacters.update(doc.specialCharacters) for doc in collection]

    def setDictionary(self, wordList=None):
        self.words = set(utils.lowerList(wordList))

    def addDocument(self, document):
        if not document.hasTokenAttribute():
            document.createTokens()
        self.words.update(utils.lowerList(document.tokens))
    
    def addCollection(self, collection):
        for document in collection:
            self.addDocument(document)

    def addStopwords(self, listStopwords):
        self.stopwords.update(utils.lowerList(listStopwords))
        self.removeStopwords()

    def removeStopwords(self):
        [self.words.discard(stopword) for stopword in self.stopwords]

    def addWords(self, wordList):
        [self.words.add(word) for word in utils.lowerList(wordList) if word not in self.stopwords]

    def getDictionaryId(self, word):
        return self.ids.keys()[self.ids.values().index(word)]


    def getWord(self, index):
        return self.ids.get(index)

    
    def plotWordDistribution(self, start=None, end=None):
        if start != None:
            distribution = [freq+1 for freq in self.ids.dfs.values() if freq>=start and freq <= end]
            plt.hist(distribution, log=True)
            plt.title('Word-Document Histogram  %d -  %d documents' % (start, end))
        else:
            distribution = [freq+1 for freq in self.ids.dfs.values()]
            plt.hist(distribution, bins=20, log=True)
            plt.title('Word-Document Histogram')
        
        plt.xlabel('Number of Documents')
        plt.ylabel('Frequency of Words')
        plt.show()

        
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
       # self.words = set([wordnet.lemmatize(wordnet.lemmatize(word.decode('utf8'), 'v')) for word in self.words])
        self.words = set([wordnet.lemmatize(wordnet.lemmatize(word, 'v')) for word in self.words])
   

    def removeShortWords(self, threshold=1):
        shortWords = [word for word in self.words if len(word)<=threshold]
        self.words = self.words.difference(shortWords)

    
    def createEntities(self, collection):
        [document.createEntities() for document in collection if document.entities.isEmpty()]
        self.entities = Entities('')
        self._addDocumentEntities(collection)
    
    def encodeWord(self, word):
        return self.ids.get(word)

    def invertDFS(self):
        self.inverseDFS = {}
        for key, value in self.ids.dfs.items():
            if value not in self.inverseDFS:
                self.inverseDFS[value] = []
            self.inverseDFS[value].append(self.ids.get(key))
    
    
    def _addDocumentEntities(self, collection):
        for tag in collection[0].entities.__dict__.keys():
            self.entities.addEntities(tag, set().union(*[getattr(document.entities, tag) for document in collection]))
        for entity in self.entities.getEntities():
            self.words.add(entity[0].lower())

 
