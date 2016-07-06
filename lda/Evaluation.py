from __future__ import division

class Evaluation:

    def __init__(self, target, prediction):
        self.target= target
        self.prediction= prediction
        self.checkLength()
        self.n = len(self.target)

    def accuracy(self):
        self.accuracy = (len(self.TP) + len(self.TN))/self.n
                                                                    
    def recall(self):
        self.recall = len(self.TP)/(len(self.TP) + len(self.FN))
                                                                    
    def precision(self):
        self.precision = len(self.TP)/(len(self.TP) + len(self.FP))

    def checkLength(self):
        if len(self.target) != len(self.prediction):
            print 'WARNING: Evaluation - length of target and prediction list is unequal'

    def createTags(self):
        self.tags = []
        for predValue, targetValue in zip(self.prediction, self.target):
            if predValue == True:
                if predValue == targetValue:
                    self.tags.append('TP')
                else:
                    self.tags.append('FP')
            else:
                if predValue == targetValue:
                    self.tags.append('TN')
                else:
                    self.tags.append('FN')

    def setTag(self, tag):
        indices = [ind for ind,value in enumerate(self.tags) if value==tag]
        setattr(self, tag, indices)


    def setAllTags(self):
        self.createTags()
        categories = ['TP', 'FP', 'TN', 'FN']
        for tag in categories:
            self.setTag(tag)

    
    

    
    

    
    





        
