from lda import documentCollection
from lda import nlp
from gensim import corpora
from lda import htmlCreator
from lda import namedEntityRecognition 

path = 'http://localhost:5984/uwazi/_design/documents/_view/fulltext'
collection = documentCollection(path)

collection.createDictionary()
collection.getNamedEntities()

testDoc = collection.documents[0]

ner = namedEntityRecognition(testDoc)
ner.tagNamedEntities()
bioTags = ner.bioTagger()
ner.bio2Tree(bioTags)

namedEntities = collection.namedEntities

html = htmlCreator()
html.namedEntitiesOfDocument(collection, 0)
html.compareDictionaries(collection)

from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize

st = StanfordNERTagger('/home/natalie/Documents/Huridocs/LDA/stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz','/home/natalie/Documents/Huridocs/LDA/stanford-ner-2014-06-16/stanford-ner.jar', encoding='utf-8')

#nlp.htmlOutput(collection[0], 0, namedEntities)
#wordsInDoc = nlp.removeStopwordsDoc(testDoc)
#dict_orig = corpora.Dictionary(wordsInDoc)
#dict_filter = dict_orig
#dict_filter.filter_extremes()
#from textblob import TextBlob
#blob = TextBlob(testDoc)
#nouns = blob.noun_phrases
