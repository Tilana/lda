#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lda import htmlCreator
from lda import TopicModel
from lda import utils
from gensim.parsing.preprocessing import STOPWORDS
from gensim import similarities
import os.path

def scriptLDA():

    #### PARAMETERS ####
    path = 'http://localhost:5984/uwazi/_design/documents/_view/fulltext'
    specialChars = set(u'[,:;\-!`\'©°"~?!\^@#%\$&\.\/_\(\)\{\}\[\]\*]')
    numberTopics = 15
    dictionaryWords = set(['united nations', 'property', 'torture','applicant', 'child', 'help'])
    dictionaryWords = None

    filename = 'dataObjects/TM1.txt'

    #### MODEL ####
    model = TopicModel(numberTopics, specialChars)

    if os.path.exists(filename):
        print "LOAD existing Topic Model"
        model.load(filename)
        model.numberTopics = numberTopics

    else:
        model.loadCollection(path)
        
        model.collection =  model.collection[0:]
        
        model.prepareDocumentCollection(lemmatize=True, includeEntities=True, stopwords=STOPWORDS, specialChars=specialChars, removeShortTokens=True, threshold=1)
    
        model.createDictionary(wordList = dictionaryWords, lemmatize=True, stoplist=STOPWORDS, specialChars= model.specialChars, removeShortWords=True, threshold=1)
        
        model.dictionary.getOriginalWords(model.collection)
    
        model.createCorpus()
            
        print model.corpus
    #    for item in model.corpus[0]:
    #        word = model.dictionary.ids.get(item[0])
    #        print word
    #        print utils.containsAny(word, specialChars)
    
    #    print model.collection[0].specialCharacters
        
        model.save(filename)

    print "LSI Model"
        
    model.tfidfModel()

    for ind, document in enumerate(model.collection):
        model.computeVectorRepresentation(document)
        model.computeFrequentWords(document)

    model.lsiModel()
    model.createTopics()
    model.computeSimilarityMatrix()
 
    print model.topics
    #print model.lsi

    for document in model.collection:
        model.computeTopicCoverage(document)
        model.computeSimilarity(document)

    model.computeTopicRelatedDocuments()
    
    html = htmlCreator()
    html.htmlDictionary(model.dictionary)
    html.printTopics(model)
    html.printDocuments(model)
    html.printDocsRelatedTopics(model, openHtml=False)
    
if __name__ == "__main__":
    scriptLDA()

