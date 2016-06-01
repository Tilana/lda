#!/usr/bin/python
#-*- coding: utf-8 -*-
from lda import Viewer
from lda import utils
from lda import Controller
from lda import Word2Vec
from gensim.parsing.preprocessing import STOPWORDS
from gensim import corpora
import os.path
import itertools

def combinedTM():

    #### PARAMETERS ####

    numberTopics = 20
    specialChars = None

    filename1 = 'dataObjects/ICAAD2000_1_default.txt'
    filename2 = 'dataObjects/ICAAD2000_2_default.txt'

    categories = ['property', 'minority', 'discrimination', 'violence', 'sexual', 'girl', 'religion', 'social', 'health', 'law', 'legal', 'court', 'state', 'freedom', 'equality', 'death', 'indigenous', 'police', 'refugee', 'health', 'technology', 'drugs', 'robbery', 'weapon', 'abuse', 'nation',  'women', 'education', 'work', 'children', 'human', 'rights', 'torture', 'men', 'government' ,'law', 'culture', 'journalist', 'corruption', 'politics']


    #### MODEL ####
    word2vec = Word2Vec()
    mainCtrl = Controller(numberTopics, specialChars)

    ctrl1 = Controller(numberTopics, specialChars)
    ctrl2 = Controller(numberTopics, specialChars)

    print 'Load preprocessed document collection'
    ctrl1.load(filename1)
    ctrl2.load(filename2)

    mainCtrl.dictionary.createDictionaryIds(ctrl1.collection)
    
    print len(ctrl1.dictionary.ids)
    transformation  = ctrl1.dictionary.ids.merge_with(ctrl2.dictionary.ids)
    print len(ctrl1.dictionary.ids)

    print 'filter extremes!!!'
    merged_corpus = itertools.chain(ctrl1.corpus, transformation[ctrl2.corpus])
    corpus = corpora.MmCorpus.serialize("mergedCorpus.mm", merged_corpus)

        print 'Create Corpus'
        ctrl.createCorpus()
        print 'Create Entity Corpus'
        #ctrl.createEntityCorpus()
        #ctrl.corpus = utils.joinSublists(ctrl.corpus, ctrl.entityCorpus)

        ctrl.save(filename)

    
    print 'TF-IDF Model'
    ctrl.tfidfModel()

    for ind, document in enumerate(ctrl.collection):
        ctrl.computeVectorRepresentation(document)
        ctrl.computeFrequentWords(document)

    
    print 'Topic Modeling'
    ctrl.topicModel('LDA', numberTopics, ctrl.corpus, topicCoverage=False, relatedDocuments=False, word2vec=word2vec, categories=categories)

    print 'Similarity Analysis'
#    ctrl.similarityAnalysis('LDA', ctrl.tfidf[ctrl.corpus])

    print 'Create HTML Files'
    html = Viewer()
    html.htmlDictionary(ctrl.dictionary)
    html.printTopics(ctrl.LDA)
#    html.printDocuments(ctrl)# , openHtml=True)
#    html.printDocsRelatedTopics(ctrl.LDA, ctrl.collection, openHtml=False)
   
if __name__ == "__main__":
    combinedTM()

