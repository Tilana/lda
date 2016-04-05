from Topic import Topic
import urllib2
import docLoader
from entities import entities
from dictionary import dictionary
from document import document
from gensim import corpora, models, similarities

class TopicModel:
    
    def __init__(self, numberTopics=None):
        self.collection = [] 
        self.corpus = []
        self.topics = [] 
        self.dictionary = dictionary()
        self.vectorDictionary = corpora.Dictionary()
        self.numberTopics = numberTopics

    def loadCollection(self, path=None):
        if path is not None:
            urllib2.urlopen(urllib2.Request(path)) 
            (titles, texts) = docLoader.loadCouchdb(path)
        else:
            titles = ['']
            texts = ['']
        self.collection = self.createDocumentList(titles, texts)

    
    def createvectorDictionary(self):
        self.vectorDictionary.add_documents([self.dictionary.words])
    
    def createCorpus(self):
        self.corpus = [self.vectorDictionary.doc2bow(document.tokens) for document in self.collection]
        
    def createDictionary(self):
        self.dictionary.addCollection(self.collection)

    def tfidfModel(self):
        self.tfidf = models.TfidfModel(self.corpus, normalize=True)
    
    def computeFrequentWords(self, document, N=10):
        docRepresentation = self.tfidf[document.vectorRepresentation]
        freqWords = sorted(docRepresentation, key=lambda frequency: frequency[1], reverse=True)[0:N]
        setattr(document, 'freqWords', self._decodevectorDictionaryList(freqWords))

    def computeTopicRelatedDocuments(self):
        for num in range(0, self.numberTopics):
            relatedDocs = sorted(enumerate([doc[num][1] for doc in self.corpus]), reverse=True, key=lambda relevance:abs(relevance[1]))
            setattr(self.topics[num], 'relatedDocuments', relatedDocs)

    def _decodevectorDictionaryList(self, l):
        return [(self.vectorDictionary.get(tup[0]).encode('utf8'), tup[1]) for tup in l]


    def createFrequentWords(self, N=10):
        for index, docs in enumerate(self.collection):
            self.setFrequentWordsInDoc(docs, N=N)

    def computeTopicCoverage(self, document):
        lsiCoverage = self.lsi[document.vectorRepresentation]
        setattr(document, 'lsiCoverage', lsiCoverage)

    def applyToAllDocuments(self, f):
        for document in self.collection:
            f(document)

    def computeVectorRepresentation(self, document):
        setattr(document, 'vectorRepresentation', self.vectorDictionary.doc2bow(document.tokens))

    def computeSimilarity(self, document):
        setattr(document, 'lsiSimilarity', self.similarityMatrix[self.lsi[document.vectorRepresentation]])

    def lsiModel(self):
        self.lsi = models.LsiModel(corpus=self.corpus, id2word=self.vectorDictionary, num_topics = self.numberTopics)

    def createTopics(self):
        topicList = []
        for topicTuple in self.lsi.show_topics(formatted=False):
            topic = Topic()
            topic.addTopic(topicTuple)
            topicList.append(topic)
            self.topics = topicList

    def computeSimilarityMatrix(self):
        self.similarityMatrix = similarities.MatrixSimilarity(self.lsi[self.corpus], num_best=7)
    
    
    def prepareDocumentCollection(self, lemmatize=True, createEntities=True, includeEntities=True, removeStopwords=True, stopwords=None, removeSpecialChars=True, specialChars = None):
        for document in self.collection:
            document.prepareDocument(lemmatize, includeEntities, removeStopwords, stopwords, removeSpecialChars, specialChars)
        self.createEntities()


    def createEntities(self):
        [document.createEntities() for document in self.collection if document.entities.isEmpty()]
        self.entities = entities('')
        self._addDocumentEntities()
    
    
    def _addDocumentEntities(self):
        for tag in self.collection[0].entities.__dict__.keys():
            self.entities.addEntities(tag, set().union(*[getattr(document.entities, tag) for document in self.collection]))
            
    
    def createDocumentList(self, titles, texts):
        return [document(title, text) for title, text in zip(titles, texts)]

