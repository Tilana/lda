#!/usr/bin/python
#-*- coding: utf-8 -*-
from lda import Viewer
from lda import utils
from lda import Controller
from lda import Word2Vec
from gensim.parsing.preprocessing import STOPWORDS
from gensim import corpora, models
import sPickle
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
    
    numberTopics = 45 
    passes = 50 
    iterations = 1000
    identifier = 'T%dP%dI%d' % (numberTopics, passes, iterations)
    
    collectionFilename = 'dataObjects/ICAAD_documents_preprocessingTest.txt'
   
    categories = ['property', 'minority', 'discrimination', 'violence', 'sexual', 'girl', 'religion', 'social', 'health', 'law', 'legal', 'court', 'state', 'freedom', 'equality', 'death', 'indigenous', 'police', 'refugee', 'health', 'technology', 'drugs', 'robbery', 'weapon', 'abuse', 'nation',  'women', 'education', 'work', 'children', 'human', 'rights', 'torture', 'men', 'government' ,'law', 'culture', 'journalist', 'corruption', 'politics', 'accident', 'system', 'finance']

    #### MODEL ####
    ctrl = Controller(numberTopics, specialChars)
    word2vec = Word2Vec()
    
    if not os.path.exists(collectionFilename) or preprocess:
        print 'Preprocessing'
        ctrl.loadCollection(path, fileType, startDoc, numberDoc)
        ctrl.prepareDocumentCollection(lemmatize=True, includeEntities=False, stopwords=STOPWORDS, removeShortTokens=True, specialChars=specialChars)
        ctrl.saveDocumentCollection(collectionFilename)

    
    print 'Create Dictionary'
    dictionary = corpora.Dictionary()
    collection = []
    for document in sPickle.s_load(open(collectionFilename)):
        collection.append(document)
        dictionary.add_documents([document.tokens])
    
    print 'Filter extremes'
    orgDfs = dictionary.dfs
    orgValues = dictionary.values()
    orgIndex = dictionary.values().index
    orgKeys = dictionary.keys()

    ctrl.dictionary.ids = dictionary
    ctrl.dictionary.plotWordDistribution()
    ctrl.dictionary.plotWordDistribution(10)



    dictionary.filter_extremes(no_below=4, no_above=0.85)
    filteredDictValues = dictionary.values()
    removedValues = list(set(orgValues) - set(filteredDictValues))
    ctrl.collection = collection
    ctrl.dictionary.ids = dictionary

    print 'Get Frequency of removed words'
    print len(orgValues)
    print len(removedValues)
    ctrl.dictionary.FreqRm = [(word, orgDfs[orgKeys[orgIndex(word)]]) for word in removedValues[0:100]]
    

    print 'Get removed special character words'
    ctrl.dictionary.specialCharacters = set()  
    [ctrl.dictionary.specialCharacters.update(doc.specialCharacters) for doc in ctrl.collection] 

    ctrl.dictionary.stopwords = STOPWORDS
   
    html = Viewer()
    html.htmlDictionary(ctrl.dictionary)

    print 'Create Corpus'
    ctrl.corpus = [dictionary.doc2bow(document.tokens) for document in collection] 

    print 'TF_IDF Model'
    ctrl.tfidfModel()

    for document in ctrl.collection:
        ctrl.computeVectorRepresentation(document)
        ctrl.computeFrequentWords(document)
    
    print 'Topic Modeling - LDA'
    ctrl.topicModel('LDA', numberTopics, ctrl.corpus, topicCoverage=False, relatedDocuments=False, word2vec=word2vec, categories=categories, passes=passes, iterations=iterations)
    html.printTopics(ctrl.LDA)

    import sys
    sys.exit()

    print 'Similarity Analysis'
    ctrl.similarityAnalysis('LDA', ctrl.corpus)

    #ctrl.saveDocumentCollection(collectionFilename)

    print 'Create HTML Files'
    html.printDocuments(ctrl)# , openHtml=True)
    html.printDocsRelatedTopics(ctrl.LDA, ctrl.collection, openHtml=False)
   
if __name__ == "__main__":
    TM_default()

