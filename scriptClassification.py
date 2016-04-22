#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas
import random
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier

def scriptClassification():

    path = 'PACI.csv'
    data = pandas.read_csv(path)

    predictColumn = 'Domestic.Violence.Manual'
    predictColumn = 'Rape'

    dropList = ['Strength.of.DV']
    dropList = ['Unnamed: 0']
    
   
    orgIndices = range(0, len(data))

    trueCases = data[data[predictColumn]].index.tolist()
    negativeCases = list(set(orgIndices) - set(trueCases))
    selectedNegativeCases = random.sample(negativeCases, len(trueCases))

    indices = list(set(trueCases + selectedNegativeCases))
    data = data.iloc[trueCases+selectedNegativeCases]

    target = data[predictColumn]
    data = data.drop(predictColumn, axis=1)

    for field in data.columns[data.dtypes==object]:
        data = data.drop(field, axis=1)

    data = data.drop(dropList, axis = 1)


    trainIndices = random.sample(data.index, len(data)/2)
    testIndices = list(set(data.index) - set(trainIndices))

    trainData = data.loc[trainIndices]
    trainTarget = target.loc[trainIndices]

    testData = data.loc[testIndices]
    testTarget = target.loc[testIndices]

    model = DecisionTreeClassifier()
    model.fit(trainData, trainTarget)

    predicted = model.predict(testData)

    print metrics.classification_report(testTarget, predicted)
    print metrics.confusion_matrix(testTarget, predicted)

    print sorted(zip(map(lambda relevance: round(relevance,4), model.feature_importances_), data.columns), reverse=True)

    


   
if __name__ == "__main__":
    scriptClassification()

