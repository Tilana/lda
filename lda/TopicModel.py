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
