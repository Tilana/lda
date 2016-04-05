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
    model = TopicModel()
    model.collection = documentCollection(path)
    
    model.collection.documents = model.collection.documents[0:3]
    
    model.collection.prepareDocumentCollection(lemmatize=True, includeEntities=True, removeStopwords=True, stopwords=STOPWORDS, removeSpecialChars=True, specialChars=specialChars)

    print model.collection.entities.LOCATION
    print model.collection.entities.PERSON

    model.collection.createDictionary()
    model.collection.dictionary.addStopwords(STOPWORDS)
    model.collection.dictionary.findSpecialCharTokens(specialChars, model.collection)
    model.collection.dictionary.removeSpecialChars()
    model.collection.dictionary.lemmatize()
    
    model.createDictionary()
    model.createCorpus()
    
    model.tfidfModel()
    model.applyToAllDocuments(model.computeVectorRepresentation)
    model.applyToAllDocuments(model.computeFrequentWords)

    model.numberTopics = 3

    model.lsiModel()
    topics = model.lsi.show_topics(formatted=False)

    model.createTopics()

    model.applyToAllDocuments(model.computeTopicCoverage)

    model.computeSimilarityMatrix()
    model.applyToAllDocuments(model.computeSimilarity)

    model.computeTopicRelatedDocuments()
    
    html = htmlCreator()
    html.htmlDictionary(model.collection)
    html.printTopics(model)
    html.printDocuments(model)
    html.printDocsRelatedTopics(model, openHtml=False)
    
if __name__ == "__main__":
    script()

