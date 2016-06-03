import urllib2
import docLoader
from Dictionary import Dictionary
from Document import Document
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


    def createEntityCorpus(self, dictionary):
        self.entityCorpus = [sorted([(dictionary.getDictionaryId(entry[0]), entry[1]) for entry in document.entities.getEntities()]) for document in self.documents]



    def computeRelevantWords(self, tfidf, dictionary, document, N=10):
        docRepresentation = tfidf[document.vectorRepresentation]
        freqWords = sorted(docRepresentation, key=lambda frequency: frequency[1], reverse=True)[0:N]
        freqWords = [(dictionary.getWord(item[0]), item[1]) for item in freqWords]
        document.setAttribute('freqWords', freqWords)


    def createFrequentWords(self, N=10):
        for index, docs in enumerate(self.documents):
            self.setFrequentWordsInDoc(docs, N=N)


    def applyToAllDocuments(self, f):
        for document in self.documents:
            f(document)


    def computeVectorRepresentation(self, document):
        document.setAttribute('vectorRepresentation', self.dictionary.ids.doc2bow(document.tokens))


    def prepareDocumentCollection(self, lemmatize=True, createEntities=True, includeEntities=True, stopwords=None, specialChars = None, removeShortTokens=True, threshold=1):
        for index, document in enumerate(self.documents):
            print index, document.title
            document.prepareDocument(lemmatize, includeEntities, stopwords, specialChars, removeShortTokens=True, threshold=threshold)

    
    def createDocumentList(self, titles, texts):
        return [Document(title, text) for title, text in zip(titles, texts)]

    def saveDocumentCollection(self, path):
        sPickle.s_dump(self.documents, open(path, 'w'))


