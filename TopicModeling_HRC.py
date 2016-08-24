#!/usr/bin/python
#-*- coding: utf-8 -*-
from lda import Collection, Dictionary, Model, Info, Viewer, utils, ImagePlotter, Word2Vec
from lda.docLoader import loadCategories
from gensim.parsing.preprocessing import STOPWORDS
from nltk.corpus import names
from gensim.models import TfidfModel
import os.path
from lda import dataframeUtils as df
import pandas

def topicModeling_HRC():

    #### PARAMETERS ####
    info = Info()
    word2vec = Word2Vec()
    info.data = 'HRC'     # 'ICAAD' 'NIPS' 'scifibooks' 'HRC'

    # Preprocessing # 
    info.preprocess = 0
    info.startDoc = 0 
    info.numberDoc= None 
    info.specialChars = set(u'''[,\.\'\`=\":\\\/_+]''')
    info.includeEntities = 0

    info.whiteList= word2vec.net.vocab.keys()
    info.stoplist = list(STOPWORDS) + utils.lowerList(names.words())

    info.removeNames = 1
    info.bigrams = 1

    # Dictionary #
    info.analyseDictionary = 1
                                                              
    info.lowerFilter = 5     # in number of documents
    info.upperFilter = 0.75   # in percent

    # LDA #
    info.modelType = 'LDA'  # 'LDA' 'LSI'
    info.numberTopics = 15 
    info.tfidf = 0
    info.passes = 985 
    info.iterations = 1200 
    info.online = 1 
    info.chunksize = 4100                                        
    info.multicore = 1

    # Evaluation #
#    filename = 'dataObjects/rightsDoc_entitiesInDoc_TM.txt'
#    filename = 'dataObjects/rightsDoc_TM.txt'
    evaluationFile = 'Documents/HRC/HRC_TopicAssignment.xlsx'
    categories = pandas.read_excel(evaluationFile, 'Topics', header=None)
    categories = utils.lowerList(list(categories[0]))
    categories = list(set(utils.flattenList([word.split() for word in categories])))
    categories = [word for word in categories if word not in STOPWORDS] 
    info.categories = word2vec.filterList(categories)
    
    assignedCategories = pandas.read_excel('Documents/HRC/hrc_topics.xlsx', 'Sheet1')
    assignedCategories = assignedCategories.fillna('xx')  
    
    info.setup()

    #### MODEL ####
    collection = Collection()
    html = Viewer(info) 

#    ctrl = Controller(numberTopics, specialChars)
    
    if not os.path.exists(info.collectionName) or info.preprocess:
        print 'Load and preprocess Document Collection'
        collection.load(info.path, info.fileType, info.startDoc, info.numberDoc)
        collection.setDocNumber()
        collection.prepareDocumentCollection(lemmatize=True, includeEntities=info.includeEntities, stopwords=info.stoplist, removeShortTokens=True, threshold=2, specialChars=info.specialChars, whiteList=info.whiteList, bigrams=info.bigrams)

    else:
        print 'Load Processed Document Collection'
        collection.loadPreprocessedCollection(info.collectionName)

    print 'Create Dictionary'
    dictionary = Dictionary(info.stoplist)
    dictionary.addCollection(collection.documents)

    print 'Create category dictionary'
    categoryList = df.toListMultiColumns(assignedCategories, ['Topic 1', 'Topic 2', 'Topic 3'])
    categoryDictionary = dict([(word, index) for index, word in enumerate(categoryList)])

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
    for document in collection.documents:
        print ind
        document.setTopicCoverage(topicCoverage[document.nr], lda.name)
        lda.computeSimilarity(document)
        collection.computeRelevantWords(tfidf, dictionary, document)
        maxTopicCoverage.append(document.LDACoverage[0][1])
        keywordFrequency = utils.countOccurance(document.text, categories) 
        document.entities.addEntities('KEYWORDS', utils.sortTupleList(keywordFrequency))
        document.mostFrequentEntities = document.entities.getMostFrequent(5)
        targetCategories = df.getRow(assignedCategories, 'identifier', document.title, ['Topic 1', 'Topic 2', 'Topic 3'])
        document.targetCategories = [(category, categoryDictionary.get(category, -1)) for category in targetCategories]

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
    topicModeling_HRC()

