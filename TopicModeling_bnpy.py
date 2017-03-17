#!/usr/bin/python
#-*- coding: utf-8 -*-
from lda import Collection, Info, docLoader
import pandas as pd
import numpy as np
import glob
import bnpy_run

def TopicModeling_bnpy():

    info = Info()
    info.data = 'Aleph'
    N = 100

    info.setPath()

    titles, text = docLoader.loadEncodedFiles(info.path)
    data = pd.DataFrame([titles[0:N], text[0:N]], index = ['title', 'text'])
    data = data.transpose()

    bnpy_data, vocabulary, word_count = bnpy_run.preprocess(data)
    
    tokenPerDocument = bnpy_data.getSparseDocTypeCountMatrix().toarray()
    data['token'] = tokenPerDocument.tolist()

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

    modelInfo = model[1]
    topicCoverage = model[1]['LP']['theta']
    topicCoverage2 = model[1]['LP']['DocTopicCount']

    def normalizeMatrix(matrix):
        sumRows = matrix.sum(axis=1)
        return matrix/sumRows[:, np.newaxis]

    data['topicCoverage'] = normalizeMatrix(topicCoverage).tolist()
    

if __name__ =="__main__":
    TopicModeling_bnpy()
