class Topic:

    def __init__(self):
        self.number = None
        self.wordDistribution = []
        self.relatedDocuments = []

    def addTopic(self, topicTuple):
        self.number = topicTuple[0]
        self.wordDistribution = topicTuple[1]

    def createTopicList(self, topics):
        return [self.addTopic(topic) for topic in topics]
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

