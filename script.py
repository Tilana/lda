from lda import documentCollection
from lda import htmlCreator

path = 'http://localhost:5984/uwazi/_design/documents/_view/fulltext'
collection = documentCollection(path)

collection.documents[1].getNamedEntities()
collection.documents[1].getWords()

collection.documents = collection.documents[0:2]
collection.getNamedEntities()

#collection.createDictionary()
#collection.namedEntities = entities

html = htmlCreator()
html.htmlDocumentEntities(collection, 0)
#html.compareDictionaries(collection)


