import pandas as pd
import random

def getRow(df, colname, value, columns):
    return list(df.loc[df[colname]==value, columns].values[0])

def filterData(df, colname):
    return df[df[colname]]

def getIndex(df):
    return df.index.tolist()

def splitDataset(data, target, num):
    (trainIndices, testIndices) = generateRandomIndices(data, num)
    return {'trainData': data.loc[trainIndices],
            'trainTarget': target.loc[trainIndices],
            'testData': data.loc[testIndices],
            'testTarget': target.loc[testIndices]}

def generateRandomIndices(data, num):
    trainIndices = random.sample(data.index, num)
    testIndices = list(set(data.index) - set(trainIndices))
    return (trainIndices, testIndices)


def balanceDataset(data, colname):
    trueCases = getIndex(filterData(data, colname))
    negativeCases = list(set(getIndex(data)) - set(trueCases))
    selectedNegativeCases = random.sample(negativeCases, len(trueCases))
    return data.iloc[trueCases+selectedNegativeCases]

def cleanDataset(data):
    for field in data.columns[data.dtypes==object]:
        data = data.drop(field, axis=1)
    return data





        

