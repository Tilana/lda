from lda import documentCollection
from lda import htmlCreator
from gensim.parsing.preprocessing import STOPWORDS

path = 'http://localhost:5984/uwazi/_design/documents/_view/fulltext'
collection = documentCollection(path)

collection.documents = collection.documents[0:3]
collection.getNamedEntities()

collection.createDictionary()
collection.dictionary.addStopwords(STOPWORDS)

html = htmlCreator()
html.htmlDocumentEntities(collection, 0)
html.htmlDictionary(collection)


