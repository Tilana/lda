import pandas as pd
import random
from lda import dataframeUtils as df
from lda import Evaluation
from sklearn import metrics

class ClassificationModel:

    def __init__(self, path=None, target=None, droplist=None):
        if path != None:
            self.orgData = pd.read_csv(path)
        self.data = self.orgData
        self.targetFeature = target 
        self.droplist = droplist

    
    def splitDataset(self, num):
        self._generateRandomIndices(num)
        self.trainData = self.data.loc[self.trainIndices]
        self.trainTarget = self.target.loc[self.trainIndices]
        self.testData = self.data.loc[self.testIndices]
        self.testTarget = self.target.loc[self.testIndices]

    def _generateRandomIndices(self, num):
        self.trainIndices = random.sample(self.data.index, num)
        self.testIndices = list(set(self.data.index) - set(self.trainIndices))
    
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

    def evaluate(self):
        self.evaluation = Evaluation(self.testTarget, self.predicted)
        self.evaluation.setAllTags()

        self.evaluation.accuracy()
        self.evaluation.recall()
        self.evaluation.precision()

    def featureImportance(self):
        featureImportance = sorted(zip(map(lambda relevance: round(relevance,4), self.classifier.feature_importances_), self.data.columns), reverse=True)
        self.featureImportance = [(elem[1], elem[0]) for elem in featureImportance if elem[0]>0.0]

    def confusionMatrix(self):
        matrix = metrics.confusion_matrix(self.testTarget, self.predicted)
        self.confusionMatrix = pd.DataFrame(matrix)

    def dropNANRows(self):
        self.data = self.data.dropna()

    def mergeDataset(self, dataset2):
        self.data = pd.merge(dataset2, self.data, on=['id'])


    def getTaggedData(self, tag):
        indices = getattr(self.evaluation, tag)
        tagIndices = [self.testIndices[position] for position in indices]
        return self.orgData.loc[tagIndices, ['File', 'Unnamed: 0']].apply(tuple, axis=1).tolist()

    def getTaggedDocs(self):
        tags = ['TP', 'FP', 'TN', 'FN']
        for tag in tags:
            setattr(self, tag+'_docs', self.getTaggedData(tag))


