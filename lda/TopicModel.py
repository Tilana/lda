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
        self.corpus = [self.dictionary.doc2bow(document.text.lower().split()) for document in self.collection.documents]
    
    def tfidfModel(self):
        self.tfidf = models.TfidfModel(self.corpus, normalize=True)
    
    def setFrequentWordsInDoc(self, docNr=0, N=10):
        docRepresentation = self.tfidf[self.corpus[docNr]]
        freqWords = sorted(docRepresentation, key=lambda frequency: frequency[1], reverse=True)[0:N]
        encodedWords = [ (self.dictionary.get(tup[0]).encode('utf8'), tup[1]) for tup in freqWords]
        setattr(self.collection.documents[docNr], 'freqWords', encodedWords)

    def createFrequentWords(self, N=10):
        for index, docs in enumerate(self.collection.documents):
            self.setFrequentWordsInDoc(docNr=index, N=N)

    def setTopicCoverageInDoc(self, docNr=0):
        lsiCoverage = self.lsi[self.collection.documents[docNr].vectorSpace]
        setattr(self.collection.documents[docNr], 'lsiCoverage', lsiCoverage)

    def createTopicCoverage(self):
        for index, docs in enumerate(self.collection.documents):
            self.setTopicCoverageInDoc(index)

    def setVectorSpaceInDoc(self, docNr=0):
        setattr(self.collection.documents[docNr], 'vectorSpace', self.dictionary.doc2bow(self.collection.documents[docNr].tokens))

    def createVectorSpace(self):
        for index, docs in enumerate(self.collection.documents):
            self.setVectorSpaceInDoc(index)

    def setSimilarityInDoc(self, docNr):
        setattr(self.collection.documents[docNr], 'lsiSimilarity', self.similarityMatrix[self.lsi[self.collection.documents[docNr].vectorSpace]])

    def createSimilarity(self):
        for index, docs in enumerate(self.collection.documents):
            self.setSimilarityInDoc(index)

    def createSimilarityMatrix(self):
        setattr(self, 'similarityMatrix', similarities.MatrixSimilarity(self.lsi[self.corpus], num_best=5)) 

    
    def lsiModel(self, numTopics=3):
        self.lsi = models.LsiModel(corpus=self.corpus, id2word=self.dictionary, num_topics = numTopics)



