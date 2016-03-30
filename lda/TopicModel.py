from documentCollection import documentCollection
from gensim import corpora, models

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
    
    def getFrequentWordsInDoc(self, docNr=0, N=10):
        docRepresentation = self.tfidf[self.corpus[docNr]]
        return sorted(docRepresentation, key=lambda frequency: frequency[1], reverse=True)[0:N]
    
    def lsiModel(self, numTopics=3):
        self.lsi = models.LsiModel(corpus=self.corpus, id2word=self.dictionary, num_topic = numTopics)



