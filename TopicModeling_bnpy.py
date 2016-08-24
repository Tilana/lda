#!/usr/bin/python
#-*- coding: utf-8 -*-
from lda import Collection, Info, docLoader
import pandas as pd
import numpy as np
import glob
import bnpy_run

def TopicModeling_bnpy():

    info = Info()
    info.data = 'CRC'

    info.setPath()

    titles, text = docLoader.loadEncodedFiles(info.path)
    data = pd.DataFrame([titles[0:], text[0:]], index = ['title', 'text'])
    data = data.transpose()

    bnpy_data, vocabulary = bnpy_run.preprocess(data)
    beta, model_score, model = bnpy_run.learn(bnpy_data, nbatch=1)

    #theta = bnpy_run.generate_theta(beta, vocabulary, text[600])

    topics = []
    for topicNr in range(beta.shape[0]):
        currTopic = beta[topicNr]
        sortedIndices = np.argsort(currTopic)
        top10 = sortedIndices[-20:]
        topic = [vocabulary[ind] for ind in top10]
        topics.append(topic)
    
    print len(topics)

    for topic in topics:
        print topic
    

if __name__ =="__main__":
    TopicModeling_bnpy()
