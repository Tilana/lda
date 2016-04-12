import urllib2
import docLoader
from entities import entities
from Dictionary import Dictionary
from document import document
from Model import Model
from gensim import models 
import cPickle

class TopicModel:
    
    def __init__(self, numberTopics=None, specialChars=None):
        self.collection = [] 
        self.corpus = []
        self.topics = [] 
        self.dictionary = Dictionary()
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
        
    def createDictionary(self, wordList=None, lemmatize=True, stoplist=None, specialChars=None, removeShortWords=True, threshold=1, addEntities=True):
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
        if addEntities:
            self.dictionary.createEntities(self.collection)


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
    
    
    def createModel(self, name='LDA', numTopics=3):
        model = Model(name, numTopics)
        model.createModel(self.corpus, self.dictionary.ids)
        setattr(self, name, model) 


    def applyToAllDocuments(self, f):
        for document in self.collection:
            f(document)


    def computeVectorRepresentation(self, document):
        document.setAttribute('vectorRepresentation', self.dictionary.ids.doc2bow(document.tokens))


    def computeTFIDF(self, document, ind):
        document.setAttribute('tfidf', self.tfidf[self.corpus[ind]])

    
    def prepareDocumentCollection(self, lemmatize=True, createEntities=True, includeEntities=True, stopwords=None, specialChars = None, removeShortTokens=True, threshold=1):
        for document in self.collection:
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

