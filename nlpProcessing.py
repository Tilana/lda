import nltk
from gensim.parsing.preprocessing import STOPWORDS
import pickle
from collections import defaultdict
import webbrowser
from textblob import TextBlob as tb
from nltk.stem import WordNetLemmatizer
import utils

# tokenize collection of document to word level
def tokenizeColl(coll):
	return set(utils.flattenList([nltk.word_tokenize(doc) for doc in coll]))

# tokenize a document on sentence and word level
def tokenize(doc):
	sentences = nltk.sent_tokenize(doc)
	words = [nltk.word_tokenize(sent) for sent in sentences]
	return words

# tag parts of speech and chunk named entities 
def posTag(doc):
	pos = [nltk.pos_tag(words) for words in doc]
	return [nltk.ne_chunk(tag, binary=True) for tag in pos]

# traverse through syntax tree
def traverse(tree):
	namedEntities = []
	
	if hasattr(tree, 'label') and tree.label:
		if tree.label() == 'NE':
			namedEntities.append(' '.join([child[0] for child in tree]))
		else:
			for child in tree:
				namedEntities.extend(traverse(child))
	return namedEntities


# Named-entity recognition
def namedEntityRecognizer(pos):
	namedEntities = []
	for tag in pos:
		namedEntities.extend(traverse(tag))
	return set(namedEntities)

# get named Enities
def getNamedEntities(coll):
	wordTokens = [tokenize(doc) for doc in coll]
	pos = [posTag(tokens) for tokens in wordTokens]
	return [namedEntityRecognizer(p) for p in pos]


# remove stopwords from dictionary
def removeStopwords(doc):
	return set([word.lower() for word in doc if word.lower() not in STOPWORDS])

# remove stopwords from dictionary
def removeStopwordsDoc(doc):
	return [word for word in doc.lower().split() if word not in STOPWORDS and word.isalnum()] 

# save preprocessed data to file
def saveProcessedDocs(dat, name):
	with open(name, 'wb') as f:
		pickle.dump(dat, f)

# remove all occurences of words in l1 one which are part of l2
def removeWords(dic, namedEntities):
	namedEntityList = splitNamedEntities(namedEntities)
	intersect = [word for word in dic if word not in namedEntityList]
	delWord = [word for word in dic if word in namedEntityList]
	return namedEntities.union(set(intersect)), set(delWord)

# transform namedEntities to list of splitted characters
def splitNamedEntities(namedEntity):
	splittedList = [ent[1].lower().split() for ent in enumerate(namedEntity)]
	return [item for sublist in splittedList for item in sublist]

# get word frequency in document
def wordFreqInDoc(word, doc):
	return tb(doc.lower()).words.count(word.lower()) 

# get number of documents containing a word
def wordFreqInColl(word, docList):
	return sum(1 for doc in docList if word.lower() in doc.lower())

# filter words based on Frequency
def filterDict(docs, words, minDocFreq=2, minCollFreq=2, minWordLength=1):
	lemmatizer = WordNetLemmatizer()
	return [lemmatizer.lemmatize(word) for word in words if wordFreqInColl(word, docs)>minCollFreq and len(word)>minWordLength]


