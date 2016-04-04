from Topic import Topic
from documentCollection import documentCollection
from gensim import corpora, models, similarities

class TopicModel:
    
    def __init__(self, path=None, numberTopics=None):
        self.collection = documentCollection(path)
        self.corpus = []
        self.topics = [] 
        self.dictionary = corpora.Dictionary()
        self.numberTopics = numberTopics
    
    def createDictionary(self):
        self.dictionary.add_documents([self.collection.dictionary.words])
    
    def createCorpus(self):
        self.corpus = [self.dictionary.doc2bow(document.tokens) for document in self.collection.documents]
    
    def tfidfModel(self):
        self.tfidf = models.TfidfModel(self.corpus, normalize=True)
    
    def computeFrequentWords(self, document, N=10):
        docRepresentation = self.tfidf[document.vectorRepresentation]
        freqWords = sorted(docRepresentation, key=lambda frequency: frequency[1], reverse=True)[0:N]
        setattr(document, 'freqWords', self._decodeDictionaryList(freqWords))

    def computeTopicRelatedDocuments(self):
        for num in range(0, self.numberTopics):
            relatedDocs = sorted(enumerate([doc[num][1] for doc in self.corpus]), reverse=True, key=lambda relevance:abs(relevance[1]))
            setattr(self.topics[num], 'relatedDocuments', relatedDocs)

    def _decodeDictionaryList(self, l):
        return [(self.dictionary.get(tup[0]).encode('utf8'), tup[1]) for tup in l]


    def createFrequentWords(self, N=10):
        for index, docs in enumerate(self.collection.documents):
            self.setFrequentWordsInDoc(docs, N=N)

    def computeTopicCoverage(self, document):
        lsiCoverage = self.lsi[document.vectorRepresentation]
        setattr(document, 'lsiCoverage', lsiCoverage)

    def applyToAllDocuments(self, f):
        for document in self.collection.documents:
            f(document)

    def computeVectorRepresentation(self, document):
        setattr(document, 'vectorRepresentation', self.dictionary.doc2bow(document.tokens))

    def computeSimilarity(self, document):
        setattr(document, 'lsiSimilarity', self.similarityMatrix[self.lsi[document.vectorRepresentation]])

    def lsiModel(self):
        self.lsi = models.LsiModel(corpus=self.corpus, id2word=self.dictionary, num_topics = self.numberTopics)

    def createTopics(self):
        topicList = []
        for topicTuple in self.lsi.show_topics(formatted=False):
            topic = Topic()
            topic.addTopic(topicTuple)
            topicList.append(topic)
            self.topics = topicList

    def computeSimilarityMatrix(self):
        self.similarityMatrix = similarities.MatrixSimilarity(self.lsi[self.corpus], num_best=7)



