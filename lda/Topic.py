from Word2Vec import Word2Vec 
import numpy

class Topic:

    def __init__(self):
        self.number = None
        self.wordDistribution = []
        self.relatedDocuments = []

    def addTopic(self, topicTuple):
        self.number = topicTuple[0]
        self.wordDistribution = topicTuple[1]

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def setAttribute(self, name, value):
        setattr(self, name, value)

    def labelTopic(self, categories):
        word2vec = Word2Vec()
        words = zip(*self.wordDistribution)[0]
        print words
        print word2vec.net.doesnt_match(words)
        meanWords = word2vec.net.most_similar(positive=words, topn=5)
        print meanWords
        rating = [] 
        for category in categories:
            categoryRating = [] 
            print category
            for meanWord in meanWords:
                categoryRating.append(word2vec.net.similarity(meanWord[0], category))
                print meanWord[0], word2vec.net.similarity(meanWord[0], category)
            rating.append(numpy.mean(numpy.asarray(categoryRating)))

        print categories
        print rating
        indices = numpy.argsort(numpy.asarray(rating))[::-1]
        print indices
        result = []
        for ind in indices:
            result.append(categories[ind])
        print result
        return result
        


