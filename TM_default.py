#!/usr/bin/python
#-*- coding: utf-8 -*-
from lda import Collection, Dictionary, Model, Viewer
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
    preprocess = 1
    
    numberTopics = 50
    passes = 70 
    iterations = 1000
    identifier = 'T%dP%dI%d' % (numberTopics, passes, iterations)
    
    collectionFilename = 'dataObjects/ICAAD_documents_preprocessingTest.txt'

    analyseDictionary = 0
   
    categories = ['property', 'minority', 'discrimination', 'violence', 'sexual', 'girl', 'religion', 'social', 'health', 'law', 'legal', 'court', 'state', 'freedom', 'equality', 'death', 'indigenous', 'police', 'refugee', 'health', 'technology', 'drugs', 'robbery', 'weapon', 'abuse', 'nation',  'women', 'education', 'work', 'children', 'human', 'rights', 'torture', 'men', 'government' ,'law', 'culture', 'journalist', 'corruption', 'politics', 'accident', 'system', 'finance']

    #### MODEL ####
    collection = Collection()
    html = Viewer()
    
    if not os.path.exists(collectionFilename) or preprocess:
        print 'Load and preprocess Document Collection'
        collection.load(path, fileType, startDoc, numberDoc)
        collection.prepareDocumentCollection(lemmatize=True, includeEntities=False, stopwords=STOPWORDS, removeShortTokens=True, specialChars=specialChars)
        collection.saveDocumentCollection(collectionFilename)
    else:
        print 'Processed Document Collection'
        collection.loadPreprocessedCollection(collectionFilename)

    print 'Create Dictionary'
    dictionary = Dictionary(STOPWORDS)
    dictionary.addDocuments(collection.documents)

    if analyseDictionary:
        'Analyse Word Frequency'
        dictionary.plotWordDistribution()
        dictionary.plotWordDistribution(1,10)
        dictionary.plotWordDistribution(4000, collection.amount)

        dictionary.invertDFS()
        html.wordFrequency(dictionary, 1, 10)
        html.wordFrequency(dictionary, 10, 20)
        html.wordFrequency(dictionary, 20, 100)
        html.wordFrequency(dictionary, 100, 2000)
        html.wordFrequency(dictionary, 2000, collection.amount) 
    
    print 'Filter extremes'
    dictionary.ids.filter_extremes(no_below=9, no_above=0.45)
    if analyseDictionary:
        dictionary.plotWordDistribution()
    html.htmlDictionary(dictionary)
    
    print 'Create Corpus'
    corpus = collection.createCorpus(dictionary)

    print 'TF_IDF Model'
    tfidf = models.TfidfModel(corpus, normalize=True)

    print 'Topic Modeling - LDA'
    lda = Model('LDA', numberTopics, categories)
    lda.createModel(corpus, dictionary.ids, numberTopics, passes, iterations)
    lda.createTopics()

    print 'Similarity Analysis'
    lda.computeSimilarityMatrix(corpus, num_best = 7)

    print 'Topic Coverage/Related Documents/SimilarityAnalysis'
    for ind, document in enumerate(collection.documents):
        print ind
        print 'Topic Coverage'
        lda.computeTopicCoverage(document)
        print 'Related Docs'
#        lda.getTopicRelatedDocuments(corpus)
        print 'Similarity'
        lda.computeSimilarity(document)
        print 'RelevantWords'
        collection.computeRelevantWords(tfidf, dictionary, document)
    
    #collection.saveDocumentCollection(collectionFilename)

    print 'Create HTML Files'
    html.printTopics(lda)
    html.printDocuments(collection.documents, lda)# , openHtml=True)
    html.printDocsRelatedTopics(lda, collection.documents, openHtml=False)
   
if __name__ == "__main__":
    TM_default()

