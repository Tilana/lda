import urllib2
import docLoader
from Dictionary import Dictionary
from Document import Document
#from Model import Model
#from gensim import models 
import cPickle
import sPickle

class Collection:
    
    def __init__(self):
        self.documents = [] 

    def load(self, path=None, fileType=0, startDoc="couchdb", numberDocs=None):
        if path is not None and fileType=="couchdb":
            urllib2.urlopen(urllib2.Request(path)) 
            (titles, texts) = docLoader.loadCouchdb(path)
        elif path is not None and fileType == "folder":
            (titles, texts) = docLoader.loadTxtFiles(path)
        elif path is not None and fileType == "csv":
            (titles, texts) = docLoader.loadCsvFile(path)
        else:
            titles = ['']
            texts = ['']
        if numberDocs is None:
            numberDocs = len(titles)
        self.documents = self.createDocumentList(titles[startDoc:startDoc + numberDocs], texts[startDoc:startDoc + numberDocs])
        self.number = len(self.documents)
    
    def createCorpus(self, dictionary):
        corpus = []
        for document in self.documents:
            vectorRepresentation = dictionary.ids.doc2bow(document.tokens)
            corpus.append(vectorRepresentation)
            document.setAttribute('vectorRepresentation', vectorRepresentation)
        return corpus


    def loadPreprocessedCollection(self, filename):
        collection = []
        for doc in sPickle.s_load(open(filename)):
            collection.append(doc)
        self.documents = collection
        self.number = len(self.documents)



    def createEntityCorpus(self):
        self.entityCorpus = [sorted([(self.dictionary.getDictionaryId(entry[0]), entry[1]) for entry in document.entities.getEntities()]) for document in self.documents]


    def createDictionary(self, wordList=None, lemmatize=True, stoplist=None, specialChars=None, removeShortWords=True, threshold=1, addEntities=True, getOriginalWords=True):
        if wordList is None:
            print '   - Add tokens to Wordlist'
            self.dictionary.addCollection(self.documents)
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
            self.dictionary.findSpecialCharTokens(specialChars, self.documents)
            self.dictionary.removeSpecialChars()
        if removeShortWords:
            print '   - Remove short tokens'
            self.dictionary.removeShortWords(threshold)
        if addEntities:
            print '   - Find Named Entities'
            self.dictionary.createEntities(self.documents)
        if getOriginalWords:
            print '   - Store original Dictionary'
            self.dictionary.getOriginalWords(self.documents)
        self.dictionary.createDictionaryIds(self.documents)
        print self.dictionary.ids


#    def tfidfModel(self):
#        self.tfidf = models.TfidfModel(self.corpus, normalize=True)


    def computeRelevantWords(self, tfidf, dictionary, document, N=10):
        docRepresentation = tfidf[document.vectorRepresentation]
        freqWords = sorted(docRepresentation, key=lambda frequency: frequency[1], reverse=True)[0:N]
        freqWords = [(dictionary.getWord(item[0]), item[1]) for item in freqWords]
#        document.setAttribute('freqWords', self._decodeDictionaryIds(dictionary, freqWords))
        document.setAttribute('freqWords', freqWords)

#    def _decodeDictionaryIds(self, dictionary, l):
#        return [(dictionary.ids.get(tup[0]).encode('utf8'), tup[1]) for tup in l]


    def createFrequentWords(self, N=10):
        for index, docs in enumerate(self.documents):
            self.setFrequentWordsInDoc(docs, N=N)


#    def getModelType(self, name):
#        return getattr(self, name)
    
    
#    def topicModel(self, name, numTopics, corpus, topicCoverage=True, relatedDocuments=True, word2vec=None, categories=None, passes=3, iterations=10):
#        model = Model(name, numTopics, categories)
#        model.createModel(corpus, self.dictionary.ids, numTopics, passes, iterations)
#        setattr(self, name, model) 
#        modelType = self.getModelType(name)
#        print ' create Topics'
#        modelType.createTopics(word2vec)
#        if topicCoverage:
#            print ' Topic Coverage'
#            for document in self.documents:
#                modelType.computeTopicCoverage(document)
#        if relatedDocuments:
#            print ' Related Documents'
#            modelType.getTopicRelatedDocuments(self.corpus)
        


#    def similarityAnalysis(self, name='LDA', corpus=None):
#        modelType = self.getModelType(name)
#        modelType.computeSimilarityMatrix(corpus)
#        for document in self.documents:
#            modelType.computeSimilarity(document)


    def applyToAllDocuments(self, f):
        for document in self.documents:
            f(document)


    def computeVectorRepresentation(self, document):
        document.setAttribute('vectorRepresentation', self.dictionary.ids.doc2bow(document.tokens))


#    def computeTFIDF(self, document, ind):
#        document.setAttribute('tfidf', self.tfidf[self.corpus[ind]])

    
    def prepareDocumentCollection(self, lemmatize=True, createEntities=True, includeEntities=True, stopwords=None, specialChars = None, removeShortTokens=True, threshold=1):
        for index, document in enumerate(self.documents):
            print index, document.title
            document.prepareDocument(lemmatize, includeEntities, stopwords, specialChars, removeShortTokens=True, threshold=threshold)

    
    def createDocumentList(self, titles, texts):
        return [Document(title, text) for title, text in zip(titles, texts)]

    def saveDocumentCollection(self, path):
        sPickle.s_dump(self.documents, open(path, 'w'))

#    def loadDocumentCollection(self, path):
#        collection = []
#        for document in sPickle.s_load(open(path)):
#            collection.append(document)
#        self.documents = collection

#    def save(self, path):
#        f = file(path, 'wb')
#        f.write(cPickle.dumps(self.__dict__))
#        f.close()
#
#    def load(self, path):
#        f= open(path, 'rb')
#        data = f.read()
#        f.close()
#        self.__dict__ = cPickle.loads(data)

