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
    
    numberTopics = 40 
    passes = 50 
    identifier = 'T%dP%d' % (numberTopics, passes)
    
    collectionFilename = 'dataObjects/ICAAD_documents_noEntities.txt'
   
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
#    dictionary.filter_extremes(no_below=7, no_above=0.7)
    print 'Filter extremes'
    dictionary.filter_extremes()

    ctrl.collection = collection
    ctrl.dictionary.ids = dictionary

    print 'Create Corpus'
    ctrl.corpus = [dictionary.doc2bow(document.tokens) for document in collection] 

    print 'TF_IDF Model'
    ctrl.tfidfModel()

    for document in ctrl.collection:
        ctrl.computeVectorRepresentation(document)
        ctrl.computeFrequentWords(document)

    lda = models.LdaModel(ctrl.corpus, num_topics=numberTopics, id2word=dictionary, passes=passes)
    lda.save('dataObjects/LDA_TM_%s' %identifier)

    pagename='html/ldaTopics%s.html' % identifier
    lda.print_topics()

    Viewer()
    Viewer.LDATopics(pagename, lda, numberTopics)

    
    print 'Topic Modeling'
    ctrl.topicModel('LDA', numberTopics, ctrl.tfidf[ctrl.corpus], topicCoverage=True, relatedDocuments=True, word2vec=word2vec, categories=categories, passes=passes)

    print 'Similarity Analysis'
    ctrl.similarityAnalysis('LDA', ctrl.tfidf[ctrl.corpus])

    ctrl.saveDocumentCollection(collectionFilename)

    print 'Create HTML Files'
    html = Viewer()
    html.htmlDictionary(ctrl.dictionary)
    html.printTopics(ctrl.LDA)
    html.printDocuments(ctrl)# , openHtml=True)
    html.printDocsRelatedTopics(ctrl.LDA, ctrl.collection, openHtml=False)
   
if __name__ == "__main__":
    TM_default()

