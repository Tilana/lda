from Topic import Topic
import urllib2
import docLoader
from entities import entities
from dictionary import dictionary
from document import document
from gensim import corpora, models, similarities
import cPickle

class TopicModel:
    
    def __init__(self, numberTopics=None, specialChars=None):
        self.collection = [] 
        self.corpus = []
        self.topics = [] 
        self.dictionary = dictionary()
        self.numberTopics = numberTopics
        self.specialChars = specialChars

    def loadCollection(self, path=None):
        if path is not None:
            urllib2.urlopen(urllib2.Request(path)) 
            (titles, texts) = docLoader.loadCouchdb(path)
        else:
            titles = ['']
            texts = ['']
        self.collection = self.createDocumentList(titles, texts)
    
    def createCorpus(self):
        self.corpus = [self.dictionary.ids.doc2bow(document.tokens) for document in self.collection]
        
    def createDictionary(self, wordList=None, lemmatize=True, stoplist=None, specialChars=None, removeShortWords=True, threshold=1):
        if wordList is None:
            self.dictionary.addCollection(self.collection)
        else:
            self.dictionary.setDictionary(wordList)
        self.dictionary.createDictionaryIds()
        if lemmatize:
            self.dictionary.lemmatize()
        if stoplist is not None:
            self.dictionary.addStopwords(stoplist)
        if specialChars is not None:
            self.dictionary.findSpecialCharTokens(specialChars, self.collection)
            self.dictionary.removeSpecialChars()
        if removeShortWords:
            self.dictionary.removeShortWords(threshold)


    def tfidfModel(self):
        self.tfidf = models.TfidfModel(self.corpus, normalize=True)
    
    def computeFrequentWords(self, document, N=10):
        docRepresentation = self.tfidf[document.vectorRepresentation]
        freqWords = sorted(docRepresentation, key=lambda frequency: frequency[1], reverse=True)[0:N]
        setattr(document, 'freqWords', self._decodeDictionaryIds(freqWords))

    def computeTopicRelatedDocuments(self):
        for num in range(0, self.numberTopics):
            relatedDocs = sorted(enumerate([doc[num][1] for doc in self.corpus]), reverse=True, key=lambda relevance:abs(relevance[1]))
            setattr(self.lsiTopics[num], 'relatedDocuments', relatedDocs)

    def _decodeDictionaryIds(self, l):
        return [(self.dictionary.ids.get(tup[0]).encode('utf8'), tup[1]) for tup in l]


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
        setattr(document, 'vectorRepresentation', self.dictionary.ids.doc2bow(document.tokens))

    def computeTFIDF(self, document, ind):
        setattr(document, 'tfidf', self.tfidf[self.corpus[ind]])

    def computeSimilarity(self, document):
        setattr(document, 'lsiSimilarity', self.similarityMatrix[self.lsi[document.vectorRepresentation]])

    def lsiModel(self):
        self.lsi = models.LsiModel(corpus=self.tfidf[self.corpus], id2word=self.dictionary.ids, num_topics = self.numberTopics)

    def ldaModel(self):
        self.lda = models.LdaModel(corpus=self.tfidf[self.corpus], id2word=self.dictionary.ids, num_topics = self.numberTopics)

    def createTopics(self):
        topicList = []
        for topicTuple in self.lsi.show_topics(formatted=False):
            topic = Topic()
            topic.addTopic(topicTuple)
            topicList.append(topic)
            self.lsiTopics = topicList
        ldaTopics = [] 
        for topicTuple in self.lda.show_topics(formatted=False):
            topic = Topic()
            topic.addTopic(topicTuple)
            ldaTopics.append(topic)
            self.ldaTopics = ldaTopics 

    def computeSimilarityMatrix(self):
        self.similarityMatrix = similarities.MatrixSimilarity(self.lsi[self.corpus], num_best=7)
    
    
    def prepareDocumentCollection(self, lemmatize=True, createEntities=True, includeEntities=True, stopwords=None, specialChars = None, removeShortTokens=True, threshold=1):
        for document in self.collection:
            document.prepareDocument(lemmatize, includeEntities, stopwords, specialChars, removeShortTokens=True, threshold=threshold)
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

    def save(self, path):
        f = file(path, 'wb')
        f.write(cPickle.dumps(self.__dict__))
        f.close()

    def load(self, path):
        f= open(path, 'rb')
        data = f.read()
        f.close()
        self.__dict__ = cPickle.loads(data)

