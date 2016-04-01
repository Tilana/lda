from documentCollection import documentCollection
from gensim import corpora, models, similarities

class TopicModel:
    
    def __init__(self, path=None):
        self.collection = documentCollection(path)
        self.corpus = []
        self.topics = []
        self.dictionary = corpora.Dictionary()
    
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

    def lsiModel(self, numTopics=3):
        self.lsi = models.LsiModel(corpus=self.corpus, id2word=self.dictionary, num_topics = numTopics)

    def computeSimilarityMatrix(self):
        self.similarityMatrix = similarities.MatrixSimilarity(self.lsi[self.corpus], num_best=7)



