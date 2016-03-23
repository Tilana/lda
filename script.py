from lda import documentCollection
from lda import htmlCreator

path = 'http://localhost:5984/uwazi/_design/documents/_view/fulltext'
collection = documentCollection(path)

collection.documents[37].getNamedEntities()
collection.documents = collection.documents[0:2]
collection.getNamedEntities()

#collection.createDictionary()
#collection.namedEntities = entities

html = htmlCreator()
html.htmlDocumentEntities(collection, 37)
#html.compareDictionaries(collection)


