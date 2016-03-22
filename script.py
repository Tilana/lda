from lda import documentCollection
from lda import htmlCreator

path = 'http://localhost:5984/uwazi/_design/documents/_view/fulltext'
collection = documentCollection(path)
collection.documents = collection.documents[0:2]
collection.createDictionary()
collection.getNamedEntities()
#collection.namedEntities = entities

html = htmlCreator()
html.htmlDocumentEntities2(collection, 0)
#html.compareDictionaries(collection)


