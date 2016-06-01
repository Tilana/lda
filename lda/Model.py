from Topic import Topic
from gensim import models, similarities
import utils
import logging
import os.path

class Model:

    def __init__(self, name, numberTopics, categories=None):
        self.name = name
        self.numberTopics = numberTopics
        self.categories = categories


    def createModel(self, corpus, dictionary, numberTopics, passes=3, iterations=10):
        logging.basicConfig(format='%(asctime)s: %(levelname)s : %(message)s', level=logging.INFO)
        path = 'TopicModel/'+self.name+'_T%dP%dI%d' % (numberTopics, passes, iterations)
        if not os.path.exists(path):
            if self.name=='LDA':
#                self.model = models.LdaModel(corpus, num_topics = numberTopics, id2word=dictionary, passes=passes, iterations=iterations , update_every=0)
                self.model = models.LdaMulticore(corpus, num_topics = numberTopics, id2word=dictionary, passes=passes, iterations=iterations , batch=1)

            elif self.name=='LSI':
                self.model = models.LsiModel(corpus, self.numberTopics, dictionary)
                self.info = str(self.model)
            else:
                print 'Unkown Model type'
            print 'save Model'
            self.model.save(path)
        else:
            print 'Load Model'
            self.model = models.LdaModel.load(path)



   



    def load(self, path):
        self.model = models.load(path)


    def createTopics(self, word2vec):
        self.topics = self._tupleToTopicList(self.model.show_topics(num_topics=self.numberTopics, formatted=False))
        meanScore = []
        for topic in self.topics:
            topic.labelTopic(word2vec, self.categories)
            topic.evaluate(word2vec)
            meanScore.append(topic.meanSimilarity)
        self.meanScore = utils.getMean(meanScore)
        print "Mean Similarity ", self.meanScore


    def _tupleToTopicList(self, tupleList):
        topicList = []
        for topicTuple in tupleList:
            topic = Topic()
            topic.addTopic(topicTuple)
            topicList.append(topic)
        return topicList


    def computeTopicCoverage(self, document):
        topicCoverage = self.model[document.vectorRepresentation]
        topicCoverage = utils.sortTupleList(utils.absoluteTupleList(topicCoverage))
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


