#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lda import htmlCreator
from lda import TopicModel
from gensim.parsing.preprocessing import STOPWORDS


def script():

    #### PARAMETERS ####
    path = 'http://localhost:5984/uwazi/_design/documents/_view/fulltext'
    specialChars = r'.*[©°\"~!\^@#%&.",-?\/\_\(\)\{\}\[\]:;\*].*'
    numberTopics = 3

    #### MODEL ####
    model = TopicModel(numberTopics, specialChars)
    model.loadCollection(path)
    
    model.collection =  model.collection[0:10]
    
    model.prepareDocumentCollection(lemmatize=True, includeEntities=True, removeStopwords=True, stopwords=STOPWORDS, removeSpecialChars=True, specialChars=specialChars)

#    print model.entities.LOCATION
#    print model.entities.PERSON

    model.createDictionary(lemmatize=True, addStopwords=True, stoplist=STOPWORDS, removeSpecialChars=True, specialChars= model.specialChars)
    
#    print model.dictionary.words
#    print model.dictionary.ids.items()
   
    model.createCorpus()
        
    print model.corpus
    
    model.tfidfModel()
    print model.tfidf
    for document in model.collection:
        model.computeVectorRepresentation(document)
        model.computeFrequentWords(document)

    model.lsiModel()
    model.createTopics()
    model.computeSimilarityMatrix()
 
    print model.topics
    #print model.lsi

    for document in model.collection:
        model.computeTopicCoverage(document)
        model.computeSimilarity(document)

    model.computeTopicRelatedDocuments()
    
    html = htmlCreator()
    html.htmlDictionary(model.dictionary)
    html.printTopics(model)
    html.printDocuments(model)
    html.printDocsRelatedTopics(model, openHtml=False)
    
if __name__ == "__main__":
    script()

