#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas
import random
from lda import dataframeUtils as df
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier

def classification():

    ##### PARAMETERS #####
    path = 'Documents/PACI.csv'
    data = pandas.read_csv(path)

    predictColumn = 'Domestic.Violence.Manual'
    predictColumn = 'Rape'

    dropList = ['Strength.of.DV']
    dropList = ['Unnamed: 0'] 

    ##### CLASSIFICATION #####

    data = df.cleanDataset(data)
    data = df.balanceDataset(data, predictColumn)

    target = data[predictColumn]
    data = data.drop(dropList + [predictColumn], axis=1)

    dataset = df.splitDataset(data, target, len(data)/2)

    model = DecisionTreeClassifier()
    model.fit(dataset['trainData'], dataset['trainTarget'])

    predicted = model.predict(dataset['testData'])

    print metrics.classification_report(dataset['testTarget'], predicted)
    print metrics.confusion_matrix(dataset['testTarget'], predicted)

    print sorted(zip(map(lambda relevance: round(relevance,4), model.feature_importances_), data.columns), reverse=True)


   
if __name__ == "__main__":
    classification()

