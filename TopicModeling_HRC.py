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

    path = "Documents/RightsDoc"

    fileType = "folder" # "couchdb" "folder" "csv"
    specialChars = set(u'''=+|[,:;€\!'"`\`\'©°\"~?!\^@#%\$&\.\/_\(\)\{\}\[\]\*]''')
    numberTopics = 15 
    startDoc = 0
    numberDoc= None 
    dictionaryWords = None

    filename = 'dataObjects/rightsDoc_entitiesInDoc_TM.txt'
#    filename = 'dataObjects/rightsDoc_TM.txt'
    includeEntities = 0
    preprocess = 0

    evaluationFile = 'Documents/HRC_TopicAssignment.xlsx'
    categories = pandas.read_excel(evaluationFile, 'Topics', header=None)
    categories = utils.lowerList(list(categories[0]))
    categories = list(set(utils.flattenList([word.split() for word in categories])))
    categories = [word for word in categories if word not in STOPWORDS] 
    
    assignedCategories = pandas.read_excel(evaluationFile, 'Sheet1')


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

    
    print 'Topic Modeling'
#    ctrl.topicModel('LDA', numberTopics, ctrl.tfidf[ctrl.corpus], topicCoverage=True, relatedDocuments=True, word2vec=word2vec, categories=categories)
    ctrl.topicModel('LSI', numberTopics, ctrl.tfidf[ctrl.corpus], topicCoverage=True, relatedDocuments=True, word2vec=word2vec, categories=categories) 

    print 'Similarity Analysis'
    ctrl.similarityAnalysis('LSI', ctrl.tfidf[ctrl.corpus])
#    ctrl.similarityAnalysis('LDA', ctrl.tfidf[ctrl.corpus])

    for ind, doc in enumerate(ctrl.collection):
        doc.name = doc.title.replace('_', '/')[:-5]

        keywordFrequency = utils.countOccurance(doc.text, categories) 
        doc.entities.addEntities('KEYWORDS', utils.sortTupleList(keywordFrequency))
        doc.mostFrequentEntities = doc.entities.getMostFrequent(5)


        targetCategories = df.getRow(assignedCategories, 'Symbol', doc.name, ['Topic 1', 'Topic2', 'Topic 3'])
        doc.targetCategories = [category for category in targetCategories if not str(category) =='nan']
        

    print 'Create HTML Files'
    html = Viewer()
    html.htmlDictionary(ctrl.dictionary)
    html.printTopics(ctrl.LSI)
#    html.printTopics(ctrl.LDA)
    html.printDocuments(ctrl)
    html.printDocsRelatedTopics(ctrl.LSI, ctrl.collection, openHtml=False)
#    html.printDocsRelatedTopics(ctrl.LDA, ctrl.collection, openHtml=False)
   
if __name__ == "__main__":
    topicModeling_RightsDocs()

