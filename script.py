#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lda import htmlCreator
from lda import TopicModel
from lda import utils
from gensim.parsing.preprocessing import STOPWORDS


def script():

    #### PARAMETERS ####
    path = 'http://localhost:5984/uwazi/_design/documents/_view/fulltext'
    specialChars = set(u'[,:;\-!`\'©°"~?!\^@#%\$&\.\/_\(\)\{\}\[\]\*]')
    #specialChars = u'''.,:;!?[]()/\$&_@*^©-`'"|°'''
    print specialChars
    numberTopics = 2

    #### MODEL ####
    model = TopicModel(numberTopics, specialChars)
    model.loadCollection(path)
    
    model.collection =  model.collection[0:]
    
    model.prepareDocumentCollection(lemmatize=True, includeEntities=True, removeStopwords=True, stopwords=STOPWORDS, removeSpecialChars=True, specialChars=specialChars, removeShortTokens=True, threshold=1)

#    print model.entities.LOCATION
#    print model.entities.PERSON
    for item in model.collection[0].tokens:
        print item
        print utils.containsAny(item, specialChars)


    model.createDictionary(lemmatize=True, addStopwords=True, stoplist=STOPWORDS, removeSpecialChars=True, specialChars= model.specialChars)
    
#    print model.dictionary.words
#    print model.dictionary.ids.items()
   
    model.createCorpus()
        
    print model.corpus
#    for item in model.corpus[0]:
#        word = model.dictionary.ids.get(item[0])
#        print word
#        print utils.containsAny(word, specialChars)

    print model.collection[0].specialCharacters
    
    model.tfidfModel()
#    print model.tfidf
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

