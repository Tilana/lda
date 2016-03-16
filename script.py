import docLoader 
import nlpProcessing as nlp
from gensim import corpora

path = 'http://localhost:5984/uwazi/_design/documents/_view/fulltext'
collection = docLoader.loadCouchdb(path)

#filename = 'fulltext.txt'
#docLoader.storeAsTxt(docCollection, filename)
#collection = docLoader.loadTxt(filename)

testDoc = collection[10][1]
titles, docs = zip(*collection)
titles = list(titles)
docs = list(docs)

words = nlp.tokenize(testDoc)
pos = nlp.posTag(words)

namedEntities = nlp.getNamedEntities(pos)
#nlp.htmlOutput(collection[0], 0, namedEntities)

wordsInDoc = nlp.removeStopwordsDoc(collection[0][1])

dict_orig = corpora.Dictionary(wordsInDoc)
dict_filter = dict_orig
dict_filter.filter_extremes()

from textblob import TextBlob
blob = TextBlob(testDoc)
nouns = blob.noun_phrases
