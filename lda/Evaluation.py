class Evaluation:

    def __init__(self, targetValues, predictionValues):
        self.target= targetValues
        self.prediction= predictionValues

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

    def getTag(self, tag):
        indices = [ind for ind,value in enumerate(self.tags) if value==tag]
        setattr(self, tag, indices)



        
