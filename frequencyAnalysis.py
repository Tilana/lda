#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lda import Viewer 
from lda import Controller
from lda import Entities
from lda import utils
from gensim.parsing.preprocessing import STOPWORDS

def scriptLDA():

    #### PARAMETERS ####
    path = "Documents/RightsDoc"
    couchdb = 1
    specialChars = set(u'''[,:;€\!'"*`\`\'©°\"~?!\^@#%\$&\.\/_\(\)\{\}\[\]\*]''')
    startDoc = 2
    docNumber = None 
    
    topics = ['armed conflict', 'environment', 'military', 'attack', 'justice', 'freedom', 'family', 'migrant', 'health', 'child', 'racism', 'corruption', 'culture', 'climate', 'discrimination', 'economy', 'internet', 'journalist', 'peace', 'poverty', 'privacy', 'religion', 'slavery', 'self determination', 'sexual violence', 'women', 'torture', 'violence', 'water', 'trafficking', 'terrorism', 'education', 'indigenous people']

    filename = 'dataObjects/rightsDoc.txt'

    #### MODEL ####
    ctrl = Controller(specialChars=specialChars)

    print 'Load document collection'
    ctrl.loadCollection(path, couchdb, startDoc, docNumber)

    print 'Prepare document collection'
    ctrl.prepareDocumentCollection(lemmatize=True, includeEntities=True, stopwords=STOPWORDS, specialChars=specialChars, removeShortTokens=True, threshold=1)

    ctrl.topics = Entities()
    ctrl.topics.addEntities('predefined', topics)
    for document in ctrl.collection:
        topicFrequency = ctrl.topics.countOccurence(document.text, 'predefined')
        document.entities.addEntities('TOPICS', utils.sortTupleList(topicFrequency))
#        mostFrequent = document.entities.getMostFrequentEntities()

    ctrl.save(filename)

    html = Viewer()
    html.printDocuments(ctrl, topics=0, openHtml=True)

      
if __name__ == "__main__":
    scriptLDA()

