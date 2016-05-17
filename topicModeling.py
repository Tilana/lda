#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lda import Viewer 
from lda import utils
from lda import Controller
from gensim.parsing.preprocessing import STOPWORDS
import os.path

def topicModeling():

    #### PARAMETERS ####
#    path = 'http://localhost:5984/uwazi/_design/documents/_view/fulltext'
#    path = "Documents/scyfibookspdf"
    path = "Documents/NIPS/Papers.csv"

    fileType = "couchdb" # "couchdb" "folder" "csv" 
    specialChars = set(u'''=+|[,:;€\!'"`\`\'©°\"~?!\^@#%\$&\.\/_\(\)\{\}\[\]\*]''')
    numberTopics = 5 
    startDoc =0 
    numberDoc= None 
#    dictionaryWords = set(['united nations', 'right', 'kenya', 'property', 'torture','applicant', 'child', 'help'])
    dictionaryWords = None

#    filename = 'dataObjects/scifiBooks_noEntities.txt'
    filename = 'dataObjects/NIPS_noEntities.txt'
#    filename = 'dataObjects/Uwazi_Dictionary'

    includeEntities = 0

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
        ctrl.prepareDocumentCollection(lemmatize=True, includeEntities=includeEntities, stopwords=STOPWORDS, specialChars=specialChars, removeShortTokens=True, threshold=1)

        ctrl.save(filename)

        print 'Prepare Dictionary'
        ctrl.createDictionary(wordList = dictionaryWords, lemmatize=True, stoplist=STOPWORDS, specialChars= ctrl.specialChars, removeShortWords=True, threshold=1, addEntities=includeEntities, getOriginalWords=True)

        print 'Create Corpus'
        ctrl.createCorpus()
        print 'Create Entity Corpus'
        ctrl.createEntityCorpus()
        ctrl.corpus = utils.joinSublists(ctrl.corpus, ctrl.entityCorpus)

        ctrl.save(filename)

    
    print 'TF-IDF Model'
    ctrl.tfidfModel()

    for ind, document in enumerate(ctrl.collection):
        ctrl.computeVectorRepresentation(document)
        ctrl.computeFrequentWords(document)
    
    print 'Topic Modeling'
    ctrl.topicModel('LDA', numberTopics, ctrl.tfidf[ctrl.corpus], topicCoverage=True, relatedDocuments=True)
    ctrl.topicModel('LSI', numberTopics, ctrl.tfidf[ctrl.corpus], topicCoverage=True, relatedDocuments=True) 

    print 'Similarity Analysis'
    ctrl.similarityAnalysis('LSI', ctrl.tfidf[ctrl.corpus])
    ctrl.similarityAnalysis('LDA', ctrl.tfidf[ctrl.corpus])

    print 'Create HTML Files'
    html = Viewer()
    html.htmlDictionary(ctrl.dictionary)
    html.printTopics(ctrl.LSI)
    html.printTopics(ctrl.LDA)
    html.printDocuments(ctrl)
    html.printDocsRelatedTopics(ctrl.LSI, ctrl.collection, openHtml=False)
    html.printDocsRelatedTopics(ctrl.LDA, ctrl.collection, openHtml=False)
   
if __name__ == "__main__":
    topicModeling()

