import utils
import numpy

class Topic:

    def __init__(self):
        self.number = None
        self.wordDistribution = []
        self.relatedDocuments = []

    def addTopic(self, topicTuple):
        self.number = topicTuple[0]
        self.wordDistribution = topicTuple[1]

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def setAttribute(self, name, value):
        setattr(self, name, value)

    def getTopicWords(self):
        return zip(*self.wordDistribution)[0][0:7]

    def labelTopic(self, word2vec, categories):
        topicWords = word2vec.filterList(self.getTopicWords()) 
        similarWords = word2vec.getSimilarWords(topicWords)
        meanSimilarity = word2vec.getMeanSimilarity(categories, similarWords)
        self.keywords = word2vec.sortCategories(meanSimilarity, categories)

    def evaluate(self, word2vec):
        topicWords = word2vec.filterList(self.getTopicWords())
        if not topicWords:
            self.intruder = 'default'
        else:
            self.intruder = word2vec.net.doesnt_match(topicWords)
        similarityMatrix = [word2vec.wordToListSimilarity(word, topicWords) for word in topicWords]

        self.pairwiseSimilarity = utils.getUpperSymmetrixMatrix(similarityMatrix)
        self.meanSimilarity = utils.getMean(self.pairwiseSimilarity)


