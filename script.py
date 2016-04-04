#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lda import documentCollection
from lda import htmlCreator
from lda import TopicModel
from gensim.parsing.preprocessing import STOPWORDS


def script():

    model = TopicModel()
    
    path = 'http://localhost:5984/uwazi/_design/documents/_view/fulltext'
    model.collection = documentCollection(path)
    
    model.collection.documents = model.collection.documents[0:3]
    #TODO: incooporate named entities in words
    model.collection.createEntities()
    
    #TODO: change words from set to a tokenized representation of the documents
    
    #TODO: make sure that every document in the collection has the attribute words before calling createCorpus()
    specialChars = r'.*[©°\"~!\^@#%&.",-?\/\_\(\)\{\}\[\]:;\*].*'
    for document in model.collection.documents:
        document.createTokens()
        document.lemmatizeTokens()
        document.deleteSpecialCharacterTokens(specialChars)

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

