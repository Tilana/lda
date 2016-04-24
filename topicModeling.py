#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lda import htmlCreator
from lda import Controller
from lda import utils
from gensim.parsing.preprocessing import STOPWORDS
from gensim import similarities
import os.path

def topicModeling():

    #### PARAMETERS ####
#    path = 'http://localhost:5984/uwazi/_design/documents/_view/fulltext'
#    path = "//home/natalie/Documents/Huridocs/LDA/Documents/scyfibookspdf"
    path = "//home/natalie/Documents/Huridocs/LDA/Documents/NIPS/Papers.csv"
    fileType = 2
    specialChars = set(u'''=+|[,:;€\!'"`\`\'©°\"~?!\^@#%\$&\.\/_\(\)\{\}\[\]\*]''')
    numberTopics = 20
    startDoc =0 
    numberDoc= None 
#    dictionaryWords = set(['united nations', 'property', 'torture','applicant', 'child', 'help'])
    dictionaryWords = None

    filename = 'dataObjects/NIPSAbstracts_all.txt'

    preprocess = 0

    #### MODEL ####
    ctrl = Controller(numberTopics, specialChars)

    if os.path.exists(filename) and not preprocess:
        print 'Load preprocessed document collection'
        ctrl.load(filename)
        ctrl.numberTopics = numberTopics

    else:
        print 'Load unprocessed document collection'
        ctrl.loadCollection(path, fileType, startDoc, numberDoc)

        print 'Prepare document collection'
        ctrl.prepareDocumentCollection(lemmatize=True, includeEntities=True, stopwords=STOPWORDS, specialChars=specialChars, removeShortTokens=True, threshold=1)

        ctrl.save(filename)

        print 'Prepare Dictionary'
        ctrl.createDictionary(wordList = dictionaryWords, lemmatize=True, stoplist=STOPWORDS, specialChars= ctrl.specialChars, removeShortWords=True, threshold=1, addEntities=True, getOriginalWords=True)

        print 'Create Corpus'
        ctrl.createCorpus()
        print 'Create Entity Corpus'
#        ctrl.createEntityCorpus()
#        ctrl.corpus = utils.joinSublists(ctrl.corpus, ctrl.entityCorpus)

        ctrl.save(filename)

    
    print 'TF-IDF Model'
    ctrl.tfidfModel()

    for ind, document in enumerate(ctrl.collection):
        ctrl.computeVectorRepresentation(document)
        ctrl.computeFrequentWords(document)
    
    print 'Topic Modeling'
#    ctrl.topicModel('LSI', numberTopics, ctrl.corpus, topicCoverage=True, relatedDocuments=True)
#    ctrl.topicModel('LDA', numberTopics, ctrl.corpus, topicCoverage=True, relatedDocuments=True)
    ctrl.topicModel('LDA', numberTopics, ctrl.tfidf[ctrl.corpus], topicCoverage=True, relatedDocuments=True)
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
    topicModeling()

