#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lda import Viewer 
from lda import Controller
from lda import Entities
from lda import utils
from gensim.parsing.preprocessing import STOPWORDS

def frequencyAnalysis():

    #### PARAMETERS ####
    path = "Documents/RightsDoc"
    filetype = "folder" 
    specialChars = set(u'''[,:;€\!'"*`\`\'©°\"~?!\^@#%\$&\.\/_\(\)\{\}\[\]\*]''')
    startDoc = 0
    docNumber = 5 
   
    filename = 'dataObjects/rightsDoc.txt'

    topics = ['armed conflict', 'albinism', 'arms', 'attack',
            'birth', 'child', 'corruption',
            'civil', 'culture', 'climate', 'commemoration',
            'death penalty', 'detention', 'democracy', 'drones', 
            'discrimination','debt','development','disability',
            'disappearance', 'determination', 
            'environment', 'economy', 'education', 'employment',
            'execution', 'expression',
            'freedom', 'family', 'food',
            'genocide', 'globalization', 'goverance', 'gender', 
            'health', 'hiv', 'housing',
            'internet', 'international cooperations','information', 
            'indigenous people',
            'justice', 'journalist', 'law',
            'military', 'migrant', 'older persons',
            'nationality', 'natural disaster'
            'peace', 'poverty', 'privacy', 'protest', 'politic',
            'prison', 'prevention', 'peasant', 
            'racism', 'religion',
            'slavery', 'self determination', 'sexual violence',
            'solidarity', 'sexual orientation', 'sport', 'social',
            'torture', 'trafficking', 'terrorism', 'tradition', 
            'truth', 
            'violence', 'war', 'water', 'women']

    
    #### MODEL ####
    ctrl = Controller(specialChars=specialChars)

    print 'Load document collection'
    ctrl.loadCollection(path, filetype, startDoc, docNumber)

    print 'Prepare document collection'
    ctrl.prepareDocumentCollection(lemmatize=True, includeEntities=True, stopwords=STOPWORDS, specialChars=specialChars, removeShortTokens=True, threshold=1)

    ctrl.topics = Entities()
    ctrl.topics.addEntities('predefined', topics)
    for document in ctrl.collection:
        topicFrequency = ctrl.topics.countOccurence(document.text, 'predefined')
        document.entities.addEntities('TOPICS', utils.sortTupleList(topicFrequency))

    ctrl.save(filename)

    html = Viewer()
    html.printDocuments(ctrl, topics=0, openHtml=True)

      
if __name__ == "__main__":
    frequencyAnalysis()

