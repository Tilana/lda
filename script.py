#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lda import documentCollection
from lda import htmlCreator
from lda import TopicModel
from gensim.parsing.preprocessing import STOPWORDS


def script():

    #### PARAMETERS ####
    path = 'http://localhost:5984/uwazi/_design/documents/_view/fulltext'
    specialChars = r'.*[©°\"~!\^@#%&.",-?\/\_\(\)\{\}\[\]:;\*].*'
    numberTopics = 3

    #### MODEL ####
    model = TopicModel(numberTopics)
    model.loadCollection(path)
    
    model.collection =  model.collection[0:3]
    
    model.prepareDocumentCollection(lemmatize=True, includeEntities=True, removeStopwords=True, stopwords=STOPWORDS, removeSpecialChars=True, specialChars=specialChars)

    print model.entities.LOCATION
    print model.entities.PERSON

    model.createDictionary()
    model.dictionary.addStopwords(STOPWORDS)
    model.dictionary.findSpecialCharTokens(specialChars, model.collection)
    model.dictionary.removeSpecialChars()
    model.dictionary.lemmatize()

    print model.dictionary.words
    
    model.createvectorDictionary()

    model.createDictionary()
    model.createCorpus()

        
    print model.corpus
    print model.vectorDictionary.items()
    
    model.tfidfModel()
    model.applyToAllDocuments(model.computeVectorRepresentation)
    model.applyToAllDocuments(model.computeFrequentWords)

    print model.tfidf    

    model.lsiModel()
    topics = model.lsi.show_topics(formatted=False)

    model.createTopics()
    print model.topics
    print model.lsi

    model.applyToAllDocuments(model.computeTopicCoverage)

    model.computeSimilarityMatrix()
    model.applyToAllDocuments(model.computeSimilarity)

    model.computeTopicRelatedDocuments()
    
    html = htmlCreator()
    html.htmlDictionary(model.dictionary)
    html.printTopics(model)
    html.printDocuments(model)
    html.printDocsRelatedTopics(model, openHtml=False)
    
if __name__ == "__main__":
    script()

