import urllib2
import docLoader
from entities import entities
from Dictionary import Dictionary
from document import document
from Model import Model
from gensim import models 
import cPickle

class Controller:
    
    def __init__(self, numberTopics=None, specialChars=None):
        self.collection = [] 
        self.corpus = []
        self.topics = [] 
        self.dictionary = Dictionary()
        self.numberTopics = numberTopics
        self.specialChars = specialChars

    def loadCollection(self, path=None, fileType=0, startDoc=0, numberDocs=None):
        if path is not None and fileType==0:
            urllib2.urlopen(urllib2.Request(path)) 
            (titles, texts) = docLoader.loadCouchdb(path)
        elif path is not None and fileType == 1:
            (titles, texts) = docLoader.loadTxtFiles(path)
        elif path is not None and fileType ==2:
            (titles, texts) = docLoader.loadCsvFile(path)
        else:
            titles = ['']
            texts = ['']
        if numberDocs is None:
            numberDocs = len(titles)
        self.collection = self.createDocumentList(titles[startDoc:startDoc + numberDocs], texts[startDoc:startDoc + numberDocs])
    
    def createCorpus(self):
        self.corpus = [self.dictionary.ids.doc2bow(document.tokens) for document in self.collection]


    def createEntityCorpus(self):
        self.entityCorpus = [sorted([(self.dictionary.getDictionaryId(entry[0]), entry[1]) for entry in document.entities.getEntities()]) for document in self.collection]


    def createDictionary(self, wordList=None, lemmatize=True, stoplist=None, specialChars=None, removeShortWords=True, threshold=1, addEntities=True, getOriginalWords=True):
        if wordList is None:
            print '   - Add tokens to Wordlist'
            self.dictionary.addCollection(self.collection)
        else:
            self.dictionary.setDictionary(wordList)
        if lemmatize:
            print '   - Lemmatize Dictionary'
            self.dictionary.lemmatize()
        if stoplist is not None:
            print '   - Remove Stopwords'
            self.dictionary.addStopwords(stoplist)
        if specialChars is not None:
            print '   - Remove special Characters'
            self.dictionary.findSpecialCharTokens(specialChars, self.collection)
            self.dictionary.removeSpecialChars()
        if removeShortWords:
            print '   - Remove short tokens'
            self.dictionary.removeShortWords(threshold)
        if addEntities:
            print '   - Find Named Entities'
            self.dictionary.createEntities(self.collection)
        if getOriginalWords:
            print '   - Store original Dictionary'
            self.dictionary.getOriginalWords(self.collection)
        self.dictionary.createDictionaryIds()

    def tfidfModel(self):
        self.tfidf = models.TfidfModel(self.corpus, normalize=True)


    def computeFrequentWords(self, document, N=10):
        docRepresentation = self.tfidf[document.vectorRepresentation]
        freqWords = sorted(docRepresentation, key=lambda frequency: frequency[1], reverse=True)[0:N]
        document.setAttribute('freqWords', self._decodeDictionaryIds(freqWords))


    def _decodeDictionaryIds(self, l):
        return [(self.dictionary.ids.get(tup[0]).encode('utf8'), tup[1]) for tup in l]


    def createFrequentWords(self, N=10):
        for index, docs in enumerate(self.collection):
            self.setFrequentWordsInDoc(docs, N=N)


    def getModelType(self, name):
        return getattr(self, name)
    
    
    def topicModel(self, name, numTopics, corpus, topicCoverage=True, relatedDocuments=True):
        model = Model(name, numTopics)
        model.createModel(corpus, self.dictionary.ids)
        setattr(self, name, model) 
        modelType = self.getModelType(name)
        modelType.createTopics()
        if topicCoverage:
            for document in self.collection:
                modelType.computeTopicCoverage(document)
        if relatedDocuments:
            modelType.getTopicRelatedDocuments(self.corpus)


    def similarityAnalysis(self, name='LDA', corpus=None):
        modelType = self.getModelType(name)
        modelType.computeSimilarityMatrix(corpus)
        for document in self.collection:
            modelType.computeSimilarity(document)


    def applyToAllDocuments(self, f):
        for document in self.collection:
            f(document)


    def computeVectorRepresentation(self, document):
        document.setAttribute('vectorRepresentation', self.dictionary.ids.doc2bow(document.tokens))


    def computeTFIDF(self, document, ind):
        document.setAttribute('tfidf', self.tfidf[self.corpus[ind]])

    
    def prepareDocumentCollection(self, lemmatize=True, createEntities=True, includeEntities=True, stopwords=None, specialChars = None, removeShortTokens=True, threshold=1):
        for index, document in enumerate(self.collection):
            print index, document.title
            document.prepareDocument(lemmatize, includeEntities, stopwords, specialChars, removeShortTokens=True, threshold=threshold)

    
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

