import pandas as pd
import random
from lda import dataframeUtils as df
from sklearn import metrics

class ClassificationModel:

    def __init__(self, path=None, target=None, droplist=None):
        if path != None:
            self.data = pd.read_csv(path)
        self.targetFeature = target 
        self.droplist = droplist

    
    def splitDataset(self, num):
        (trainIndices, testIndices) = self._generateRandomIndices(num)
        self.trainData = self.data.loc[trainIndices]
        self.trainTarget = self.target.loc[trainIndices]
        self.testData = self.data.loc[testIndices]
        self.testTarget = self.target.loc[testIndices]

    
    def _generateRandomIndices(self, num):
        trainIndices = random.sample(self.data.index, num)
        testIndices = list(set(self.data.index) - set(trainIndices))
        return (trainIndices, testIndices)
    
    
    def balanceDataset(self, factor=1):
        trueCases = df.getIndex(df.filterData(self.data, self.targetFeature))
        negativeCases = list(set(df.getIndex(self.data)) - set(trueCases))
        numberSamples = factor * len(trueCases)
        selectedNegativeCases = self.getRandomSample(negativeCases, numberSamples)
        self.data = self.data.loc[trueCases+selectedNegativeCases, :]

    def getRandomSample(self, data, n):
        return random.sample(data, n)

    
    def cleanDataset(self):
        for field in self.data.columns[self.data.dtypes==object]:
            self.data = self.data.drop(field, axis=1)
    
    def createNumericFeature(self, column):
        category = 0
        for value in self.data[column].unique():
            self.data.loc[self.data[column]==value, column] = category
            category += 1
        self.toNumeric(column)

    def createTarget(self):
        self.target = self.data[self.targetFeature]
        self.droplist = self.droplist + [self.targetFeature]
    
    def toNumeric(self, column):
        self.data[column] = self.data[column].astype(int)

    def toBoolean(self, column):
        self.data[column] = self.data[column].astype(bool)

    def dropFeatures(self):
        self.data = self.data.drop(self.droplist, axis=1)

    def trainClassifier(self, classifier):
        classifier.fit(self.trainData, self.trainTarget)
        self.classifier = classifier

    def predict(self, classifier):
        self.predicted = classifier.predict(self.testData)

    def evaluate(self, binary=1):
        self.accuracy = metrics.accuracy_score(self.testTarget, self.predicted)
        if binary:
            self.precision = metrics.precision_score(self.testTarget, self.predicted)
            self.recall = metrics.recall_score(self.testTarget, self.predicted)
        else:
            self.precision = 0
            self.recall = 0

    def featureImportance(self):
        featureImportance = sorted(zip(map(lambda relevance: round(relevance,4), self.classifier.feature_importances_), self.data.columns), reverse=True)
        self.featureImportance = [(elem[1], elem[0]) for elem in featureImportance]

    def confusionMatrix(self):
        matrix = metrics.confusion_matrix(self.testTarget, self.predicted)
        self.confusionMatrix = pd.DataFrame(matrix)

    def dropNANRows(self):
        self.data = self.data.dropna()




