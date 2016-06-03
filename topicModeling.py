#!/usr/bin/python
#-*- coding: utf-8 -*-
from lda import Collection, Dictionary, Model, Info, Viewer
from lda.docLoader import loadCategories
from gensim.parsing.preprocessing import STOPWORDS
from gensim.models import TfidfModel
import os.path

def TM_default():

    #### PARAMETERS ####
    info = Info()
    info.data = 'ICAAD'     # 'ICAAD' 'NIPS' 'scifibooks'
    info.modelType = 'LDA'  # 'LDA' 'LSI'
    
    info.startDoc = 0
    info.numberDoc= None 
    info.specialChars = set(u'''[,\.\'\`=\":\\\/_+]''')
    info.includeEntities = 0
    info.preprocess = 0
    
    info.numberTopics = 75 
    info.passes = 90 
    info.iterations = 2000 
    info.tfidf = 0

    info.analyseDictionary = 0
    info.categories = loadCategories('Documents/categories.txt')[0]     #0 -human rights categories   1 - Scientific Paper categories
    
    info.lowerFilter = 9    # in number of documents
    info.upperFilter = 0.4  # in percent
    
    info.setup()

    #### MODEL ####
    collection = Collection()
    html = Viewer(info.identifier)
    
    if not os.path.exists(info.collectionName) or info.preprocess:
        print 'Load and preprocess Document Collection'
        collection.load(info.path, info.fileType, info.startDoc, info.numberDoc)
        collection.prepareDocumentCollection(lemmatize=True, includeEntities=False, stopwords=STOPWORDS, removeShortTokens=True, specialChars=info.specialChars)
        collection.saveDocumentCollection(info.collectionName)
    else:
        print 'Load Processed Document Collection'
        collection.loadPreprocessedCollection(info.collectionName)

    print 'Create Dictionary'
    dictionary = Dictionary(STOPWORDS)
    dictionary.addCollection(collection.documents)

    if info.analyseDictionary:
        'Analyse Word Frequency'
        dictionary.plotWordDistribution()
        dictionary.plotWordDistribution(1,10)
        dictionary.plotWordDistribution(collection.number/2, collection.number)

        dictionary.invertDFS()
        html.wordFrequency(dictionary, 1, 10)
        html.wordFrequency(dictionary, 10, collection.number/2)
        html.wordFrequency(dictionary, collection.number/2, collection.number) 
    
    print 'Filter extremes'
    dictionary.ids.filter_extremes(info.lowerFilter, info.upperFilter)
    if info.analyseDictionary:
        dictionary.plotWordDistribution()
    
    print 'Create Corpus'
    corpus = collection.createCorpus(dictionary)

    print 'TF_IDF Model'
    tfidf = TfidfModel(corpus, normalize=True)
    if tfidf:
        corpus = tfidf[corpus]

    print 'Topic Modeling - LDA'
    lda = Model(info)
    lda.createModel(corpus, dictionary.ids, info)
    lda.createTopics(info)
    html.printTopics(lda)

    if not os.path.exists(info.processedCollectionName):
        print 'Similarity Analysis'
        lda.computeSimilarityMatrix(corpus, num_best = 7)

        print 'Topic Coverage/Related Documents/SimilarityAnalysis'
        for ind, document in enumerate(collection.documents[0:1]):
            print ind
            print 'Topic Coverage'
            lda.computeTopicCoverage(document)
            print 'Related Docs'
            lda.getTopicRelatedDocuments(corpus)
            print 'Similarity'
            lda.computeSimilarity(document)
            print 'RelevantWords'
            collection.computeRelevantWords(tfidf, dictionary, document)
        collection.saveDocumentCollection(info.processedCollectionName)
    else:
        collection.loadPreprocessedCollection(info.processedCollectionName)

    print 'Create HTML Files'
    html.htmlDictionary(dictionary)
    html.printTopics(lda)
    html.printDocuments(collection.documents, lda)# , openHtml=True)
    html.printDocsRelatedTopics(lda, collection.documents, openHtml=False)
   
if __name__ == "__main__":
    TM_default()

