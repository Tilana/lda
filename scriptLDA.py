#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lda import htmlCreator
from lda import TopicModel
from lda import utils
from gensim.parsing.preprocessing import STOPWORDS
from gensim import similarities
import os.path

def scriptLDA():

    #### PARAMETERS ####
    path = 'http://localhost:5984/uwazi/_design/documents/_view/fulltext'
    specialChars = set(u'[,:;\-!`\'©°"~?!\^@#%\$&\.\/_\(\)\{\}\[\]\*]')
    numberTopics = 3
    dictionaryWords = set(['united nations', 'property', 'torture','applicant', 'child', 'help'])
    dictionaryWords = None

    filename = 'dataObjects/TM3docs.txt'
    preprocess = 0

    #### MODEL ####
    model = TopicModel(numberTopics, specialChars)

    if os.path.exists(filename) and not preprocess:
        print "LOAD existing Topic Model"
        model.load(filename)
        model.numberTopics = numberTopics

    else:
        model.loadCollection(path)
        
        model.collection =  model.collection[0:3]
        
        model.prepareDocumentCollection(lemmatize=True, includeEntities=True, stopwords=STOPWORDS, specialChars=specialChars, removeShortTokens=True, threshold=1)
    
        model.createDictionary(wordList = dictionaryWords, lemmatize=True, stoplist=STOPWORDS, specialChars= model.specialChars, removeShortWords=True, threshold=1, addEntities=True)
        
        model.dictionary.getOriginalWords(model.collection)
    
        model.createCorpus()
            
        print model.corpus
    #    for item in model.corpus[0]:
    #        word = model.dictionary.ids.get(item[0])
    #        print word
    #        print utils.containsAny(word, specialChars)
    
    #    print model.collection[0].specialCharacters
        
        model.save(filename)

    print "LSI Model"
        
    model.tfidfModel()

    for ind, document in enumerate(model.collection):
        model.computeVectorRepresentation(document)
        print dir(document) 
        model.computeFrequentWords(document)
    model.createModel('LSI', 3)
    model.createModel('LDA', 3)

#    model.lsiModel()
#    model.ldaModel()
    model.LSI.createTopics()
    model.LDA.createTopics()

    model.LSI.computeSimilarityMatrix(model.corpus)
    model.LDA.computeSimilarityMatrix(model.corpus)

    print model.LSI.topics
    print model.LDA.topics
   #print model.lsi

    for document in model.collection:
        model.LSI.computeTopicCoverage(document)
        print type(document.LSICoverage)
        print document.LSICoverage
        model.LSI.computeSimilarity(document)
        model.LDA.computeTopicCoverage(document)
        model.LDA.computeSimilarity(document)

    model.LSI.computeTopicRelatedDocuments(model.corpus)
    print 'Related Dcouments'
    print model.LSI.topics[0].relatedDocuments
    model.LDA.computeTopicRelatedDocuments(model.corpus)
   
    html = htmlCreator()
    html.htmlDictionary(model.dictionary)
    html.printTopics(model.LSI)
    html.printTopics(model.LDA)
    html.printDocuments(model)
    html.printDocsRelatedTopics(model, topicType='LSI', openHtml=False)
    html.printDocsRelatedTopics(model, topicType='LDA', openHtml=False)
   
if __name__ == "__main__":
    scriptLDA()

