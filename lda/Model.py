from Topic import Topic
from Word2Vec import Word2Vec
from gensim import models, similarities
import utils
import pickle
import logging
import os.path

class Model:

    def __init__(self, info):
        self.name = info.modelType
        self.categories = info.categories
        self.numberTopics = info.numberTopics

    def createModel(self, corpus, dictionary, info):
        logging.basicConfig(format='%(asctime)s: %(levelname)s : %(message)s', level=logging.INFO)
        path = 'TopicModel/'+info.data+'_'+info.identifier
        if not os.path.exists(path):
            if self.name=='LDA':
                if info.multicore:
                    self.model = models.LdaMulticore(corpus, num_topics = info.numberTopics, id2word=dictionary, passes=info.passes, iterations=info.iterations , batch=0)
                else:
                    self.model = models.LdaModel(corpus, num_topics = info.numberTopics, id2word=dictionary, passes=info.passes, iterations=info.iterations , update_every=info.online, chunksize=info.chunksize)
            elif self.name=='LSI':
                self.model = models.LsiModel(corpus, info.numberTopics, dictionary)
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


    def createTopics(self, info):
        word2vec = Word2Vec()
        self.topics = self._tupleToTopicList(self.model.show_topics(num_topics=info.numberTopics, formatted=False))
        meanScore = []
        for topic in self.topics:
            topic.labelTopic(word2vec, info.categories)
            topic.findIntruder(word2vec)
            topic.computeSimilarityScore(word2vec)
            meanScore.append(topic.medianSimilarity)
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
       

    def computeSimilarityMatrix(self, corpus, numFeatures, num_best=7):
        self.similarityMatrix = similarities.MatrixSimilarity(self.model[corpus], num_features = numFeatures, num_best=num_best)


    def getTopicRelatedDocuments(self, corpus, info):
        topicCoverage = self.model[corpus]
        for ind, topic in enumerate(self.topics):
            print 'Topic ', ind
            topicCoveragePerTopic = utils.absoluteTupleList(self.zipTopicCoverageList(topicCoverage, ind))
            setattr(topic, 'relatedDocuments', sorted(topicCoveragePerTopic, reverse=True))
            topic.getRelevanceHistogram(info)


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

    def saveModel(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    def loadModel(self, path):
        with open(path, 'rb') as f:
            self = pickle.load(f)

    



