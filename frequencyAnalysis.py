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
    specialChars = set(u'''[,:;€\!'"*`\`\'©°\"~?!\^@#%\$&\.\/_\(\)\{\}\[\]\*]''')
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
        ctrl.prepareDocumentCollection(lemmatize=True, includeEntities=True, stopwords=STOPWORDS, specialChars=specialChars, removeShortTokens=True, threshold=1)

        print ctrl.collection[0].entities.LOCATION
        print ctrl.collection[0].entities.ORGANIZATION

        ctrl.save(filename)

        print 'Prepare Dictionary'
        ctrl.createDictionary(wordList = dictionaryWords, lemmatize=True, stoplist=STOPWORDS, specialChars= ctrl.specialChars, removeShortWords=True, threshold=1, addEntities=True, getOriginalWords=True)


        print 'Create Corpus'
        ctrl.createCorpus()
        ctrl.createEntityCorpus()
        ctrl.corpus = utils.joinSublists(ctrl.corpus, ctrl.entityCorpus)
        ctrl.save(filename)

    
    print 'Create HTML Files'
    html = htmlCreator()
    html.htmlDictionary(ctrl.dictionary)
    html.printDocuments(ctrl, topics=0, openHtml=True)
   
if __name__ == "__main__":
    scriptLDA()

