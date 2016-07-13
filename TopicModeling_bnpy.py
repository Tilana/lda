#!/usr/bin/python
#-*- coding: utf-8 -*-
from lda import Collection, Info, docLoader
import pandas as pd
import glob
import bnpy_run

def TopicModeling_bnpy():

    info = Info()
    info.data = 'ICAAD'
    info.startDoc = 0
    info.numberDoc = None
    info.modelType = 'LDA'
    info.numberTopics = 10
    info.passes = 10
    info.iterations = 30
    info.tfidf=0
    info.whiteList = []
    info.stoplist = []
    info.includeEntities = 0
    info.specialsChasrs = set()
    info.removeNames = 0

    info.setup()

    titles, text = docLoader.loadEncodedFiles(info.path)
    data = pd.DataFrame([titles[0:500], text[0:500]], index = ['title', 'text'])
    data = data.transpose()

    bnpy_data, vocabulary = bnpy_run.preprocess(data)
    beta, model_score = bnpy_run.learn(bnpy_data, nbatch=4)

    theta = bnpy_run.generate_theta(beta, vocabulary, text[600])
    


    


if __name__ =="__main__":
    TopicModeling_bnpy()
