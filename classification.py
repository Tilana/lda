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
    predictColumn = 'Sexual.Assault'

    dropList = ['Strength.of.SA', 'Sexual.Assault.Manual', 'Unnamed: 0']


    ### PREPROCESSING ###
    # TODO: Consider symmetrie in age values
    data = df.createNumericFeature(data, 'Age')
    
    data = df.createNumericFeature(data, 'Court')
    data.loc[data['Reconciliation_freq']=='False', 'Reconciliation_freq' ] = '0'
    data = df.toNumeric(data, 'Reconciliation_freq')
   

    data = df.cleanDataset(data)

    ### SELECT TEST AND TRAINING DATA ###
    data = df.balanceDataset(data, predictColumn)

    target = data[predictColumn]
    data = data.drop(dropList + [predictColumn], axis=1)

    dataset = df.splitDataset(data, target, len(data)/2)


    ### CLASSIFICATION ###
    model = DecisionTreeClassifier()
    model.fit(dataset['trainData'], dataset['trainTarget'])

    predicted = model.predict(dataset['testData'])

    ### EVALUATION ###
    print metrics.classification_report(dataset['testTarget'], predicted)
    print metrics.confusion_matrix(dataset['testTarget'], predicted)

    print sorted(zip(map(lambda relevance: round(relevance,4), model.feature_importances_), data.columns), reverse=True)


   
if __name__ == "__main__":
    classification()

