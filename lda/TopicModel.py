from documentCollection import documentCollection
from gensim import corpora

class TopicModel:

    def __init__(self):
        self.collection = documentCollection(' ')
        self.corpus = []
        self.topics = []
        self.dictionary = corpora.Dictionary()

    def createDictionary(self):
        self.dictionary.add_documents([self.collection.dictionary.words]) 

    def createCorpus(self):
        self.corpus = [self.dictionary.doc2bow(document.words) for document in self.collection.documents]



