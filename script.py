from lda import documentCollection
from lda import htmlCreator

path = 'http://localhost:5984/uwazi/_design/documents/_view/fulltext'
collection = documentCollection(path)
#collection.createDictionary()
collection.getNamedEntities()


html = htmlCreator()
html.namedEntitiesOfDocument(collection, 0)
html.compareDictionaries(collection)


