from Word2Vec import Word2Vec 
import utils

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
        return zip(*self.wordDistribution)[0]

    def labelTopic(self, categories):
        word2vec = Word2Vec()
        similarWords = word2vec.getSimilarWords(self.getTopicWords())
        meanSimilarity = word2vec.getMeanSimilarity(categories, similarWords)
        self.keywords = word2vec.sortCategories(meanSimilarity, categories)
        


