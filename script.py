from documentCollection import documentCollection
import nlpProcessing as nlp
from gensim import corpora
import dictHtmlOutput as html

path = 'http://localhost:5984/uwazi/_design/documents/_view/fulltext'
collection = documentCollection(path)

collection.createDict()
collection.getNamedEntities()


#html.htmlOutput(testDoc, 0, namedEntities)
#html.createDictHtml(testDoc, namedEntities, collection.dict, collection.dict)

#nlp.htmlOutput(collection[0], 0, namedEntities)
#wordsInDoc = nlp.removeStopwordsDoc(testDoc)
#dict_orig = corpora.Dictionary(wordsInDoc)
#dict_filter = dict_orig
#dict_filter.filter_extremes()
#from textblob import TextBlob
#blob = TextBlob(testDoc)
#nouns = blob.noun_phrases
