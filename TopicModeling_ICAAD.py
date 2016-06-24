#!/usr/bin/python
#-*- coding: utf-8 -*-
from lda import Collection, Dictionary, Model, Info, Viewer, utils
from lda.docLoader import loadCategories
from gensim.parsing.preprocessing import STOPWORDS
from nltk.corpus import names
from gensim.models import TfidfModel
import os.path
from lda import ImagePlotter
from lda import Word2Vec
from lda import dataframeUtils as df
import csv
import pandas

def topicModeling_ICAAD():

    #### PARAMETERS ####
    info = Info()
    word2vec = Word2Vec()
    info.data = 'ICAAD'     # 'ICAAD' 'NIPS' 'scifibooks' 'HRC'

    # Preprocessing # 
    info.preprocess = 0
    info.startDoc = 0 
    info.numberDoc= None 
    info.specialChars = set(u'''[,\.\'\`=\":\\\/_+]''')
    info.includeEntities = 0

    info.whiteList= word2vec.net.vocab.keys()
    info.stoplist = list(STOPWORDS) + utils.lowerList(names.words())

    info.removeNames = 1

    # Dictionary #
    info.analyseDictionary = 1
                                                              
    info.lowerFilter = 10     # in number of documents
    info.upperFilter = 0.3   # in percent

    # LDA #
    info.modelType = 'LDA'  # 'LDA' 'LSI'
    info.numberTopics = 18 
    info.tfidf = 0
    info.passes = 371 
    info.iterations = 1500 
    info.online = 1 
    info.chunksize = 4100                                        
    info.multicore = 1

    # Categories and Keywords
    info.categories = loadCategories('Documents/categories.txt')[0]     #0 -human rights categories   1 - Scientific Paper categories
    keywordFile = 'Documents/ICAAD/CategoryLists.csv'
    keywords = pandas.read_csv(keywordFile).astype(str)
    #info.keywords = word2vec.filterList(keywords)
    
    info.setup()

    #### MODEL ####
    collection = Collection()
    html = Viewer(info) 

    if not os.path.exists(info.collectionName) or info.preprocess:
        print 'Load and preprocess Document Collection'
        collection.load(info.path, info.fileType, info.startDoc, info.numberDoc)
        collection.prepareDocumentCollection(lemmatize=True, includeEntities=False, stopwords=info.stoplist, removeShortTokens=True, threshold=2, specialChars=info.specialChars, whiteList=info.whiteList)

    else:
        print 'Load Processed Document Collection'
        collection.loadPreprocessedCollection(info.collectionName)

    print 'Create Dictionary'
    dictionary = Dictionary(info.stoplist)
    dictionary.addCollection(collection.documents)

    print 'Create category dictionary'
#    categoryList = df.toListMultiColumns(assignedCategories, ['Topic 1', 'Topic 2', 'Topic 3'])
#    categoryDictionary = dict([(word, index) for index, word in enumerate(categoryList)])

    if info.analyseDictionary:
        'Analyse Word Frequency'
        collectionLength = collection.number
        dictionary.analyseWordFrequencies(info, html, collectionLength)
    
    print 'Filter extremes'
    dictionary.ids.filter_extremes(info.lowerFilter, info.upperFilter)

    if info.analyseDictionary:
        dictionary.plotWordDistribution(info)
    
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

    print 'Topic Coverage'
    topicCoverage = lda.model[corpus]
    
    print 'Get Documents related to Topics'
    lda.getTopicRelatedDocuments(topicCoverage, info)
    
    print 'Similarity Analysis'
    lda.computeSimilarityMatrix(corpus, numFeatures=info.numberTopics, num_best = 7)

    maxTopicCoverage = []
    for ind, document in enumerate(collection.documents):
        document.setTopicCoverage(topicCoverage[ind], lda.name)
        lda.computeSimilarity(document)
        collection.computeRelevantWords(tfidf, dictionary, document)
        maxTopicCoverage.append(document.LDACoverage[0][1])
        for category in keywords.columns.tolist():
            wordsInCategory = list(keywords[category].unique())
            wordsInCategory = [word for word in wordsInCategory if word != 'nan']
            keywordFrequency = utils.countOccurance(document.text, wordsInCategory)
            document.entities.addEntities(category, utils.sortTupleList(keywordFrequency))
        document.mostFrequentEntities = document.entities.getMostFrequent(5)

    ImagePlotter.plotHistogram(maxTopicCoverage, 'Maximal Topic Coverage', 'html/' + info.data+'_'+info.identifier+'/Images/maxTopicCoverage.jpg', 'Maximal LDA Coverage', 'Number of Docs', log=1)

    print 'Create HTML Files'
    html.htmlDictionary(dictionary)
    html.printTopics(lda)
    html.printDocuments(collection.documents, lda)
    html.printDocsRelatedTopics(lda, collection.documents, openHtml=False)
    html.documentOverview(collection.documents)

    info.selectedTopics = input('Select Topics: ')
    collection.writeDocumentFeatureFile(info, info.selectedTopics)

                                                                   
    info.saveToFile()
   
if __name__ == "__main__":
    topicModeling_ICAAD()

