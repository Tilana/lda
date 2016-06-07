#!/usr/bin/python
#-*- coding: utf-8 -*-
from lda import Collection, Dictionary, Model, Info, Viewer
from lda.docLoader import loadCategories
from gensim.parsing.preprocessing import STOPWORDS
from gensim.models import TfidfModel
import os.path
from lda import ImagePlotter
from lda import Word2Vec

def TM_default():

    #### PARAMETERS ####
    info = Info()
    info.data = 'ICAAD'     # 'ICAAD' 'NIPS' 'scifibooks'
    info.modelType = 'LDA'  # 'LDA' 'LSI'
    
    info.startDoc = 0 
    info.numberDoc= 100 
    info.specialChars = set(u'''[,\.\'\`=\":\\\/_+]''')
    info.includeEntities = 0
    info.preprocess = 0

    info.numberTopics = 21 
    info.passes = 204 
    info.iterations = 1500 
    info.online = 1 
    info.chunksize = 4100 
    info.multicore = 1
    info.tfidf = 0
    
    info.whiteList = ['sexual', 'rape', 'assault', 'penetration', 'women', 'vagina', 'child', 'subdue', 'harassment', 'forced', 'abuse', 'sexually', 'exploitation', 'prostitution', 'strip', 'nude', 'sex', 'trafficking', 'incest', 'aggression', 'offender', 'genital', 'family', 'parent', 'sibling', 'intimate', 'marriage', 'gay', 'lesbian', 'boy', 'girl', 'porn', 'pornography', 'victim', 'violation', 'touch', 'body', 'penis', 'stalking', 'bank', 'banking', 'bond', 'comission', 'credit','debit', 'debt', 'deposit', 'money', 'interest', 'rate', 'mortgage', 'savings', 'vault', 'withdrawal', 'account', 'payment', 'bancrupt', 'finance', 'beneficiary', 'cash', 'cost', 'currency', 'default', 'fund', 'bill', 'sale', 'selling', 'solvent', 'solvency', 'tax', 'payer', 'taxes', 'fraud', 'loan', 'bribery', 'evasion', 'laundring', 'money', 'theft', 'forgery', 'charge']
    word2vec = Word2Vec()
    info.whiteList= word2vec.net.vocab.keys()
    
    info.analyseDictionary = 1
    info.categories = loadCategories('Documents/categories.txt')[0]     #0 -human rights categories   1 - Scientific Paper categories
    
    info.lowerFilter = 5    # in number of documents
    info.upperFilter = 0.55  # in percent
    
    info.setup()

    #### MODEL ####
    collection = Collection()
    html = Viewer(info)
        
    if not os.path.exists(info.collectionName) or info.preprocess:
        print 'Load and preprocess Document Collection'
        collection.load(info.path, info.fileType, info.startDoc, info.numberDoc)
        collection.prepareDocumentCollection(lemmatize=True, includeEntities=False, stopwords=STOPWORDS, removeShortTokens=True, specialChars=info.specialChars, whiteList=info.whiteList)
        collection.saveDocumentCollection(info.collectionName)
    else:
        print 'Load Processed Document Collection'
        collection.loadPreprocessedCollection(info.collectionName)

    print 'Create Dictionary'
    dictionary = Dictionary(STOPWORDS)
    dictionary.addCollection(collection.documents)

    if info.analyseDictionary:
        'Analyse Word Frequency'
        dictionary.plotWordDistribution(info)
        dictionary.plotWordDistribution(info, 1,10)
        dictionary.plotWordDistribution(info, collection.number/2, collection.number)

        dictionary.invertDFS()
        html.wordFrequency(dictionary, 1, 10)
        html.wordFrequency(dictionary, 10, collection.number/2)
        html.wordFrequency(dictionary, collection.number/2, collection.number) 
    
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
    

    print 'Get Documents related to Topics'
    lda.getTopicRelatedDocuments(corpus, info)

    print 'Similarity Analysis'
    lda.computeSimilarityMatrix(corpus, numFeatures=info.numberTopics, num_best = 7)

    maxTopicCoverage = []
    for ind, document in enumerate(collection.documents):
        lda.computeTopicCoverage(document)
        lda.computeSimilarity(document)
        collection.computeRelevantWords(tfidf, dictionary, document)
        maxTopicCoverage.append(document.LDACoverage[0][1])

    ImagePlotter.plotHistogram(maxTopicCoverage, 'Maximal Topic Coverage', 'html/' + info.data+'_'+info.identifier+'/Images/maxTopicCoverage.jpg', 'Maximal LDA Coverage', 'Number of Docs', log=1)

    print 'Create HTML Files'
    info.saveToFile()
    html.printTopics(lda)
    html.htmlDictionary(dictionary)
    html.printTopics(lda)
    html.printDocuments(collection.documents, lda)# , openHtml=True)
    html.printDocsRelatedTopics(lda, collection.documents, openHtml=False)
    html.documentOverview(collection.documents)
   
if __name__ == "__main__":
    TM_default()

