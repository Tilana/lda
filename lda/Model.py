from Topic import Topic
from gensim import corpora, models, similarities

class Model:
    def __init__(self, name='LDA', numberTopics=3):
        self.name = name
        self.numberTopics = numberTopics

    def createModel(self, corpus, dictionary):
        if self.name=='LDA':
            self.model = models.LdaModel(corpus, self.numberTopics, dictionary)
        if self.name=='LSI':
            self.model = models.LsiModel(corpus, self.numberTopics, dictionary)
        else:
            print 'Unkown Model type'
            print self.name

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
    
    def computeTopicRelatedDocuments(self, corpus):
        for num in range(0, self.numberTopics):
            relatedDocs = sorted(enumerate([doc[num][1] for doc in corpus]), reverse=True, key=lambda relevance:abs(relevance[1]))
            self.topics[num].setAttribute('relatedDocuments', relatedDocs)
            print relatedDocs

