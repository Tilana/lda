#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lda import htmlCreator
import nltk
from lda import Controller
from lda import entities
from lda import utils
from gensim.parsing.preprocessing import STOPWORDS
from gensim import similarities
import os.path

def scriptLDA():

    #### PARAMETERS ####
    path = "//home/natalie/Documents/Huridocs/LDA/Documents/RightsDoc"
    couchdb = 0
    specialChars = set(u'''[,:;€\!'"*`\`\'©°\"~?!\^@#%\$&\.\/_\(\)\{\}\[\]\*]''')
    startDoc = 2
    docNumber = None 
    
    topics = ['armed conflict', 'environment', 'justice', 'freedom', 'family', 'migrants', 'health', 'child', 'racism', 'corruption', 'culture', 'climate', 'discrimination', 'economy', 'internet', 'journalists', 'peace', 'poverty', 'privacy', 'religion', 'slavery', 'self determination', 'sexual violence', 'women', 'torture', 'violence', 'water', 'trafficking', 'terrorism', 'education', 'indigenous people']

    filename = 'dataObjects/rightsDoc.txt'

    #### MODEL ####
    ctrl = Controller(specialChars=specialChars)

    print 'Load document collection'
    ctrl.loadCollection(path, couchdb, startDoc, docNumber)

    print 'Prepare document collection'
    ctrl.prepareDocumentCollection(lemmatize=True, includeEntities=True, stopwords=STOPWORDS, specialChars=specialChars, removeShortTokens=True, threshold=1)

    ctrl.topics = entities()
    ctrl.topics.addEntities('predefined', topics)
    for document in ctrl.collection:
        topicFrequency = ctrl.topics.countOccurence(document.text, 'predefined')
        document.entities.addEntities('TOPICS', utils.sortTupleList(topicFrequency))

    ctrl.save(filename)

    html = htmlCreator()
    html.printDocuments(ctrl, topics=0, openHtml=True)

      
if __name__ == "__main__":
    scriptLDA()

