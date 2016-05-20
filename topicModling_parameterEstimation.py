#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lda import Viewer 
from lda import utils
from lda import Controller
from lda import Word2Vec
from lda import dataframeUtils as df
import csv
import pandas
from gensim.parsing.preprocessing import STOPWORDS
import os.path

def topicModeling_RightsDocs():

    #### PARAMETERS ####

    path = "Documents/NIPS/Papers.csv"

    fileType = "csv" # "couchdb" "folder" "csv"
    specialChars = set(u'''=+|[,:;€\!'"`\`\'©°\"~?!\^@#%\$&\.\/_\(\)\{\}\[\]\*]''')
    numberTopics = 10 
    startDoc = 0
    numberDoc= None 
    dictionaryWords = None

    filename = 'dataObjects/NIPS_noEntities.txt'
    includeEntities = 0
    preprocess = 0

    categories = ['inference', 'theory', 'uncertainty', 'neural', 'robust', 'stochastic', 'monte', 'learning', 'complexity', 'problem', 'computation', 'deep', 'graph', 'network', 'image', 'text', 'recognition', 'classification', 'rgeression', 'algorithm', 'probabilistic', 'bayes', 'gradient', 'training', 'sampling', 'kernel', 'result', 'feature', 'evaluation', 'convoluation', 'speed', 'brain', 'model', 'prediction', 'data', 'performance', 'decoding', 'encoding', 'generative', 'discriminative', 'game', 'recurrent', 'languague'] 

    

    alpha = [0.05, 0.1, 0.25, 0.5]
    eta = [0.05, 0.1, 0.25, 0.5]



    #### MODEL ####
    ctrl = Controller(numberTopics, specialChars)
    word2vec = Word2Vec()
    categories = word2vec.filterList(categories)

    if os.path.exists(filename) and not preprocess:
        print 'Load preprocessed document collection'
        ctrl.load(filename)
        ctrl.numberTopics = numberTopics

    else:
        print 'Load unprocessed document collection'
        ctrl.loadCollection(path, fileType, startDoc, numberDoc)

        print 'Prepare document collection'
        ctrl.prepareDocumentCollection(lemmatize=True, includeEntities=1, stopwords=STOPWORDS, specialChars=specialChars, removeShortTokens=True, threshold=1)

        ctrl.save(filename)

        print 'Prepare Dictionary'
        ctrl.createDictionary(wordList = dictionaryWords, lemmatize=True, stoplist=STOPWORDS, specialChars= ctrl.specialChars, removeShortWords=True, threshold=1, addEntities=includeEntities, getOriginalWords=True)

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

    for alphaValue in alpha:
        for etaValue in eta:
            print 'Topic Modeling'
            print 'alpha = ', alphaValue
            print 'eta = ', etaValue

            ctrl.topicModel('LDA', numberTopics, ctrl.tfidf[ctrl.corpus], topicCoverage=True, relatedDocuments=True, word2vec=word2vec, categories=categories, alpha=alphaValue, eta=etaValue)

            html = Viewer()
            html.printTopics(ctrl.LDA)
   
if __name__ == "__main__":
    topicModeling_RightsDocs()

