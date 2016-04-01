from lda import documentCollection
from lda import htmlCreator
from lda import TopicModel
from gensim.parsing.preprocessing import STOPWORDS


def script():

    model = TopicModel()
    
    path = 'http://localhost:5984/uwazi/_design/documents/_view/fulltext'
    model.collection = documentCollection(path)
    
    model.collection.documents = model.collection.documents[0:3]
    #TODO: incooporate named entities in words
    model.collection.createEntities()
    
    #TODO: change words from set to a tokenized representation of the documents
    
    #TODO: make sure that every document in the collection has the attribute words before calling createCorpus()
    execute = [document.createTokens() for document in model.collection.documents]
    
    model.collection.createDictionary()
    model.collection.dictionary.addStopwords(STOPWORDS)
    
    model.createDictionary()
    model.createCorpus()
    
    model.tfidfModel()
    model.applyToAllDocuments(model.computeVectorRepresentation)
    model.applyToAllDocuments(model.computeFrequentWords)

    model.lsiModel(10)
    topics = model.lsi.print_topics(num_topics=3)
    print "TEST"
    print topics
    print len(topics)
    print topics[0]

    model.applyToAllDocuments(model.computeTopicCoverage)

    model.computeSimilarityMatrix()
    model.applyToAllDocuments(model.computeSimilarity)
    
    html = htmlCreator()
    html.htmlDocumentEntities(model.collection, 0)
    html.htmlDictionary(model.collection)
    html.printTopics(model)
    html.printDocuments(model)
    html.printDocsRelatedTopics(model, 3)
    
if __name__ == "__main__":
    script()

