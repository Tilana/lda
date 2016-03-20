from documentCollection import documentCollection
import nlpProcessing as nlp
from gensim import corpora
from htmlCreator import htmlCreator

path = 'http://localhost:5984/uwazi/_design/documents/_view/fulltext'
collection = documentCollection(path)

collection.createDictionary()
collection.getNamedEntities()

testDoc = collection.documents[0]
namedEntities = collection.namedEntities

html = htmlCreator()
html.namedEntitiesOfDocument(collection, 0)
html.compareDictionaries(collection)


#nlp.htmlOutput(collection[0], 0, namedEntities)
#wordsInDoc = nlp.removeStopwordsDoc(testDoc)
#dict_orig = corpora.Dictionary(wordsInDoc)
#dict_filter = dict_orig
#dict_filter.filter_extremes()
#from textblob import TextBlob
#blob = TextBlob(testDoc)
#nouns = blob.noun_phrases
