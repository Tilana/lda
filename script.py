import documentCollection
import nlpProcessing as nlp
from gensim import corpora

path = 'http://localhost:5984/uwazi/_design/documents/_view/fulltext'
docCollection = docCollection(path)

#filename = 'fulltext.txt'
#docLoader.storeAsTxt(docCollection, filename)
#collection = docLoader.loadTxt(filename)

testDoc = docCollection.docs[0]
words = nlp.tokenize(testDoc)
pos = nlp.posTag(words)

namedEntities = nlp.getNamedEntities(pos)
#nlp.htmlOutput(collection[0], 0, namedEntities)

wordsInDoc = nlp.removeStopwordsDoc(testDoc)

dict_orig = corpora.Dictionary(wordsInDoc)
dict_filter = dict_orig
dict_filter.filter_extremes()

from textblob import TextBlob
blob = TextBlob(testDoc)
nouns = blob.noun_phrases
