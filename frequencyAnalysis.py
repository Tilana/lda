#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lda import Viewer 
from lda import Controller
from lda import Entities
from lda import utils
import csv
import pandas
from gensim.parsing.preprocessing import STOPWORDS

def frequencyAnalysis():

    #### PARAMETERS ####
    evaluationDoc = 'Documents/HRC_TopicAssignment.xlsx'
    keywords = pandas.read_excel(evaluationDoc, 'Topics', header=None)
    keywords = utils.lowerList(list(keywords[0]))

    originalAssignment = pandas.read_excel(evaluationDoc, 'Sheet1')

    path = "Documents/RightsDoc"
    filetype = "folder" 
    specialChars = set(u'''[,:;€\!'"*`\`\'©°\"~?!\^@#%\$&\.\/_\(\)\{\}\[\]\*]''')
    startDoc = 0
    docNumber = None 
   
    filename = 'dataObjects/rightsDoc.txt'

    
    #### MODEL ####
    ctrl = Controller(specialChars=specialChars)
    ctrl.loadCollection(path, filetype, startDoc, docNumber)

    ctrl.prepareDocumentCollection(lemmatize=True, includeEntities=False, stopwords=STOPWORDS, specialChars=specialChars, removeShortTokens=True, threshold=1)

    ctrl.topics = Entities()
    ctrl.topics.addEntities('predefined', keywords)
    for document in ctrl.collection:
        topicFrequency = ctrl.topics.countOccurence(document.text, 'predefined')
        document.entities.addEntities('PREDEFINED KEYWORDS', utils.sortTupleList(topicFrequency))

    fileNames = [doc.title.replace('_', '/')[:-5] for doc in ctrl.collection]

    for ind, doc in enumerate(ctrl.collection):
        doc.title = fileNames[ind]
        doc.mostFrequent = doc.entities.getMostFrequent(5)
        manualTopics = list((originalAssignment.loc[originalAssignment['Symbol']==doc.title, ['Topic 1', 'Topic 2', 'Topic 3']]).values[0])
        mostFrequent = zip(*doc.mostFrequent)[0]
        doc.manualTopics = [(topic.lower(), topic.lower() in mostFrequent) for topic in manualTopics if not str(topic)=='nan']


    ctrl.save(filename)

    html = Viewer()
    html.freqAnalysis(ctrl.collection, openHtml=True)

    with open('freqAnalysisOutput.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for document in ctrl.collection:
            writer.writerow([document.title] + document.entities.getMostFrequent())


      
if __name__ == "__main__":
    frequencyAnalysis()

