#!/usr/bin/python
#-*- coding: utf-8 -*-
from lda import Collection, Dictionary, Model, Viewer
from gensim.parsing.preprocessing import STOPWORDS
from gensim import models
import os.path

def topicModeling():

    #### PARAMETERS ####

#    path = "Documents/scyfibookspdf"
    path = "Documents/NIPS/Papers.csv"
#    path = "Documents/ICAAD/txt"
    fileType = "folder" # "couchdb" "folder" "csv"
    startDoc = 0
    numberDoc= None

    numberTopics = 20 
    passes = 7
    iterations = 100
    identifier = 'T%dP%dI%d' % (numberTopics, passes, iterations)

    filename = 'dataObjects/NIPS_noEntities'
#    filename = 'dataObjects/scifiBooks50_noEntities'
#    filename = 'dataObjects/ICAAD5000'

    includeEntities = 0
    preprocess = 0
    specialChars = set(u'''=+|[,:;€\!'"`\`\'©°\"~?!\^@#%\$&\.\/_\(\)\{\}\[\]\*]''')

    categories = ['machine', 'neuron', 'graph', 'network', 'analysis', 'kernel', 'computation', 'bayes', 'inference', 'classification', 'text', 'information', 'gauss', 'brain',  'learning', 'algorithm', 'food', 'culture', 'image']
#    categories = ['property', 'kenya', 'freedom', 'equality', 'death', 'indigenous', 'police', 'refugee', 'health', 'women', 'education', 'work', 'children', 'human', 'rights', 'torture', 'africa' ,'law', 'culture', 'journalist', 'corruption', 'politics']


    #### MODEL ####
    collection = Collection()

    if not os.path.exists(filename) or preprocess:
        print 'Load and process Document Collection'
        collection.load(filename)
        collection.prepareDocumentCollection(lemmatize=True, includeEntities=False, stopwords=STOPWORDS, specialChars=specialChars, removeShortTokens=True, threshold=1)
        collection.saveDocumentCollection(filename)

    else:
        print 'Load processed document collection'
        collection.loadCollection(path, fileType, startDoc, numberDoc)

        print 'Prepare Dictionary'
        collection.createDictionary(wordList = dictionaryWords, lemmatize=True, stoplist=STOPWORDS, specialChars= collection.specialChars, removeShortWords=True, threshold=1, addEntities=includeEntities, getOriginalWords=True)

        print 'Create Corpus'
        collection.createCorpus()
        print 'Create Entity Corpus'
        #collection.createEntityCorpus()
        #collection.corpus = utils.joinSublists(collection.corpus, collection.entityCorpus)

        collection.save(filename)

    
    print 'TF-IDF Model'
    collection.tfidfModel()

    for ind, document in enumerate(collection.collection):
        collection.computeVectorRepresentation(document)
        collection.computeFrequentWords(document)

    
    print 'Topic Modeling'
    collection.topicModel('LDA', numberTopics, collection.tfidf[collection.corpus], topicCoverage=True, relatedDocuments=True, word2vec=word2vec, categories=categories)
    collection.topicModel('LSI', numberTopics, collection.tfidf[collection.corpus], topicCoverage=True, relatedDocuments=True, word2vec=word2vec, categories=categories) 

    print 'Similarity Analysis'
    collection.similarityAnalysis('LSI', collection.tfidf[collection.corpus])
    collection.similarityAnalysis('LDA', collection.tfidf[collection.corpus])

    print 'Create HTML Files'
    html = Viewer()
    html.htmlDictionary(collection.dictionary)
    html.printTopics(collection.LSI)
    html.printTopics(collection.LDA)
    html.printDocuments(collection)# , openHtml=True)
    html.printDocsRelatedTopics(collection.LSI, collection.collection, openHtml=False)
    html.printDocsRelatedTopics(collection.LDA, collection.collection, openHtml=False)
   
if __name__ == "__main__":
    topicModeling()

