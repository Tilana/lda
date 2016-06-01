#!/usr/bin/python
#-*- coding: utf-8 -*-
from lda import Viewer
from lda import Model
from lda import Dictionary
from lda import Controller
from lda import Word2Vec
from gensim.parsing.preprocessing import STOPWORDS
from gensim import models
import os.path

def TM_default():

    #### PARAMETERS ####
    path = "Documents/ICAAD/txt"
    fileType = "folder" # "couchdb" "folder" "csv"
    
    startDoc = 0
    numberDoc= None 
    specialChars = set(u'''[,\.\'\`=\":\\\/_+]''')
    includeEntities = 0
    preprocess = 0
    
    numberTopics = 3 
    passes = 2 
    iterations = 10
    identifier = 'T%dP%dI%d' % (numberTopics, passes, iterations)
    
    collectionFilename = 'dataObjects/ICAAD_documents_preprocessingTest.txt'

    analyseDictionary = 0
   
    categories = ['property', 'minority', 'discrimination', 'violence', 'sexual', 'girl', 'religion', 'social', 'health', 'law', 'legal', 'court', 'state', 'freedom', 'equality', 'death', 'indigenous', 'police', 'refugee', 'health', 'technology', 'drugs', 'robbery', 'weapon', 'abuse', 'nation',  'women', 'education', 'work', 'children', 'human', 'rights', 'torture', 'men', 'government' ,'law', 'culture', 'journalist', 'corruption', 'politics', 'accident', 'system', 'finance']

    #### MODEL ####
    ctrl = Controller(numberTopics, specialChars)
    word2vec = Word2Vec()
    html = Viewer()
    
    if not os.path.exists(collectionFilename) or preprocess:
        print 'Load and preprocess Document Collection'
        ctrl.loadCollection(path, fileType, startDoc, numberDoc)
        ctrl.prepareDocumentCollection(lemmatize=True, includeEntities=False, stopwords=STOPWORDS, removeShortTokens=True, specialChars=specialChars)
        ctrl.saveDocumentCollection(collectionFilename)

    print 'Processed Document Collection'
    collection = ctrl.loadPreprocessedCollection(collectionFilename)

    print 'Create Dictionary'
    dictionary = Dictionary()
    dictionary.createDictionaryIds(collection)

    if analyseDictionary:
        'Analyse Word Frequency'
        dictionary.plotWordDistribution()
        dictionary.plotWordDistribution(1,10)
        dictionary.plotWordDistribution(4000,len(collection))

        dictionary.invertDFS()
        html.wordFrequency(dictionary, 1, 10)
        html.wordFrequency(dictionary, 10, 20)
        html.wordFrequency(dictionary, 20, 100)
        html.wordFrequency(dictionary, 100, 2000)
        html.wordFrequency(dictionary, 2000, len(collection)) 
    
    
    print 'Filter extremes'
    dictionary.ids.filter_extremes(no_below=9, no_above=0.6)
    if analyseDictionary:
        dictionary.plotWordDistribution()

    dictionary.setSpecialCharacters(collection)
    dictionary.stopwords = STOPWORDS
   
    html.htmlDictionary(dictionary)
    
    print 'Create Corpus'
    ctrl.collection = collection
    corpus = ctrl.createCorpus(dictionary)

    print 'TF_IDF Model'
    tfidf = models.TfidfModel(corpus, normalize=True)

    print 'Topic Modeling - LDA'
    lda = Model('LDA', numberTopics, categories)
    lda.createModel(corpus, dictionary.ids, numberTopics, passes, iterations)
    lda.createTopics(word2vec)

    print 'Similarity Analysis'
    lda.computeSimilarityMatrix(corpus, num_best = 7)

    print 'Topic Coverage/Related Documents/SimilarityAnalysis'
    for ind, document in enumerate(collection):
        print ind
        print 'Topic Coverage'
        lda.computeTopicCoverage(document)
        print 'Related Docs'
        lda.getTopicRelatedDocuments(corpus)
        print 'Similarity'
        lda.computeSimilarity(document)
        print 'RelevantWords'
        ctrl.computeRelevantWords(tfidf, dictionary, document)
    
    #ctrl.saveDocumentCollection(collectionFilename)

    print 'Create HTML Files'
    html.printTopics(lda)
    html.printDocuments(collection, lda)# , openHtml=True)
    html.printDocsRelatedTopics(lda, collection, openHtml=False)
   
if __name__ == "__main__":
    TM_default()

