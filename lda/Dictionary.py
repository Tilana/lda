#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Entities import Entities
import utils
from nltk.stem import WordNetLemmatizer
from gensim import corpora
import matplotlib.pyplot as plt

class Dictionary:
        
    def __init__(self, stopwords=None):
        self.words = set([])
        self.ids = corpora.Dictionary()
        self.specialCharacters = set([]) 
        self.stopwords = set([]) if stopwords is None else stopwords           

    def addCollection(self, collection):
        for document in collection:
            self.addDocument(document)

    def addDocument(self, document):
        if document.hasTokenAttribute():
            self.ids.add_documents([document.tokens])
        if document.hasSpecialCharAttribute():
            self.specialCharacters.update(document.specialCharacters)

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

 
