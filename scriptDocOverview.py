#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lda import htmlCreator
import nltk
from lda import Controller
from lda import utils
from gensim.parsing.preprocessing import STOPWORDS
from gensim import similarities
import os.path

def scriptLDA():

    #### PARAMETERS ####
    path = "//home/natalie/Documents/Huridocs/LDA/Documents/RightsDoc"
    couchdb = 0
    specialChars = set(u'''[,:;€\-!'"`\`\'©°\"~?!\^@#%\$&\.\/_\(\)\{\}\[\]\*]''')
    numberTopics = 3
    startDoc = 0
    docNumber = 5 
    dictionaryWords = set(['united nations', 'property', 'torture','applicant', 'child', 'help'])
    dictionaryWords = None

    filename = 'dataObjects/rightsDoc.txt'
    preprocess = 1

    #### MODEL ####
    ctrl = Controller(numberTopics, specialChars)

    if os.path.exists(filename) and not preprocess:
        print 'Load preprocessed document collection'
        ctrl.load(filename)
        ctrl.numberTopics = numberTopics

    else:
        print 'Load unprocessed document collection'
        ctrl.loadCollection(path, couchdb, startDoc, docNumber)

        print 'Prepare document collection'
        ctrl.prepareDocumentCollection(lemmatize=True, includeEntities=False, stopwords=STOPWORDS, specialChars=specialChars, removeShortTokens=True, threshold=1)

        ctrl.save(filename)

        print 'Prepare Dictionary'
        ctrl.createDictionary(wordList = dictionaryWords, lemmatize=True, stoplist=STOPWORDS, specialChars= ctrl.specialChars, removeShortWords=True, threshold=1, addEntities=True, getOriginalWords=True)

#        print ctrl.dictionary.words
#
#        print ctrl.dictionary.entities.LOCATION

#        print ctrl.collection[0].text.lower()
#        print 'HUMAN RIGHTS WATCH ID'


        print 'Create Corpus'
        ctrl.createCorpus()
        ctrl.createEntityCorpus()
        ctrl.corpus = utils.joinSublists(ctrl.corpus, ctrl.entityCorpus)
        print 'LOCATION'
        print ctrl.dictionary.entities.LOCATION

        corp = ctrl.entityCorpus[0][500:2100]
        print 'ENTITITY CORPUS'
        print ctrl.entityCorpus
        for elem in corp:
            print ctrl.dictionary.ids.get(elem[0]), elem[1]
#        print ctrl.dictionary.getDictionaryId('human rights watch')
#        print ctrl.corpus

        ctrl.save(filename)

    
    print 'TF-IDF Model'
    ctrl.tfidfModel()

    for ind, document in enumerate(ctrl.collection):
        ctrl.computeVectorRepresentation(document)
        ctrl.computeFrequentWords(document)
    
    print 'Topic Modeling'
#    ctrl.topicModel('LSI', numberTopics, ctrl.corpus, topicCoverage=True, relatedDocuments=True)
    ctrl.topicModel('LDA', numberTopics, ctrl.corpus, topicCoverage=True, relatedDocuments=True)
    ctrl.topicModel('LSI', numberTopics, ctrl.tfidf[ctrl.corpus], topicCoverage=True, relatedDocuments=True) 

    print 'Similarity Analysis'
    ctrl.similarityAnalysis('LSI', ctrl.tfidf[ctrl.corpus])
    ctrl.similarityAnalysis('LDA', ctrl.corpus)

    print 'Create HTML Files'
    html = htmlCreator()
    html.htmlDictionary(ctrl.dictionary)
    html.printTopics(ctrl.LSI)
    html.printTopics(ctrl.LDA)
    html.printDocuments(ctrl)
    html.printDocsRelatedTopics(ctrl.LSI, ctrl.collection, openHtml=False)
    html.printDocsRelatedTopics(ctrl.LDA, ctrl.collection, openHtml=False)
   
if __name__ == "__main__":
    scriptLDA()

