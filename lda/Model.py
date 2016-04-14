from Topic import Topic
from gensim import corpora, models, similarities
import utils

class Model:

    def __init__(self, name, numberTopics):
        self.name = name
        self.numberTopics = numberTopics


    def createModel(self, corpus, dictionary):
        if self.name=='LDA':
            self.model = models.LdaModel(corpus, self.numberTopics, dictionary)
            self.info = str(self.model)
        elif self.name=='LSI':
            self.model = models.LsiModel(corpus, self.numberTopics, dictionary)
            self.info = str(self.model)
        else:
            print 'Unkown Model type'


    def createTopics(self):
        self.topics = self._tupleToTopicList(self.model.show_topics(formatted=False))


    def _tupleToTopicList(self, tupleList):
        topicList = []
        for topicTuple in tupleList:
            topic = Topic()
            topic.addTopic(topicTuple)
            topicList.append(topic)
        return topicList


    def computeTopicCoverage(self, document):
        topicCoverage = self.model[document.vectorRepresentation]
        document.setAttribute(('%sCoverage' % self.name), topicCoverage)
        
    
    def computeSimilarity(self, document):
        document.setAttribute(('%sSimilarity' % self.name), self.similarityMatrix[self.model[document.vectorRepresentation]])
       

    def computeSimilarityMatrix(self, corpus, num_best=7):
        self.similarityMatrix = similarities.MatrixSimilarity(self.model[corpus], num_best)


    def getTopicRelatedDocuments(self, corpus):
        topicCoverage = self.model[corpus]
        for ind, topic in enumerate(self.topics):
            topicCoveragePerTopic = utils.absoluteTupleList(self.zipTopicCoverageList(topicCoverage, ind))
            setattr(topic, 'relatedDocuments', sorted(topicCoveragePerTopic, reverse=True))


#    def getTopicCoverageInCollection(self, collection):
#        coverageList = []
#        for document in collection:
#            topicCoverage = getattr(document, ('%sCoverage' % self.name))
#            coverageList.append(topicCoverage)
#        return coverageList
#

    def zipTopicCoverageList(self, coverageList, value):
        valueList = []
        for index, documents in enumerate(coverageList):
            for tupleElement in documents:
                if tupleElement[0]==value:
                    valueList.append((tupleElement[1], index))
        return valueList


