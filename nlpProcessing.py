import nltk
from gensim.parsing.preprocessing import STOPWORDS
import pickle
from collections import defaultdict
import webbrowser
from textblob import TextBlob as tb

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
def getNamedEntities(pos):
	namedEntities = []
	for tag in pos:
		namedEntities.extend(traverse(tag))
	return set(namedEntities)

# remove stopwords from dictionary
def removeStopwords(doc):
	return[[word for word in doc.lower().split() if word not in STOPWORDS and word.isalnum()] for doc in documents]

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
    return [word for word in words if wordFreqInColl(word, docs)>minCollFreq and len(word)>minWordLength]

# create html overview file for a document
def htmlOutput(doc, ind, namedEntities):	
	name = 'html/nlpDoc%02d.html' % ind
	f = open(name, 'w')
	f.write("<html><head><h1>Doc %02d - %s </h1></head>" % (ind, doc[0]))
	f.write("""<body><div style="width:100%;"><div style="float:right; width:40%;">""")
	f.write("""<h3>Named Entities: \n</h3><table>""")
	f.write("""<col style="width:40%"> <col style="width:50%">""")
	for ent in namedEntities:
		f.write("""<tr><td>%s</td> </tr>""" % ent)
	f.write("""</table></div>""")
	f.write("""<div style="float:left; width:55%%;"><p>%s</p></div></div></body></html>""" % doc[1].encode('utf8'))
	f.close()
	webbrowser.open_new_tab('html/nlpDoc%02d.html' % ind)

# print unprocessed and processed dictionary
def createDictHtml(doc, namedEntities):
	name = 'html/dictionary.html'
	f = open(name, 'w')
	f.write("<html><head><h1> Dictionary </h1></head>")
	f.write("""<body><div style="width:100%;"><div style="float:left; width:20%;">""")
	f.write("""<h3> Un-Processed \n</h3><table>""")
	for words in set(removeStopwordsDoc(doc)):
		f.write("""<tr><td>%s</td> </tr>""" % words.encode('utf8'))
	f.write("""</table></div>""")
	f.write("""<div style="float:left; width:20%%;">""")
	f.write("""<h3> Processed \n</h3><table>""")
	orig = removeStopwordsDoc(doc)
	new = removeWords(orig, namedEntities)	
	for words in new[0]:
		f.write("""<tr><td>%s</td> </tr>""" % words.encode('utf8'))
	f.write("""</table></div>""")
	f.write("""<div style="float:left; width:50%%;">""")
	f.write("""<h3> Removed Words \n</h3><table>""")
	for words in new[1]:
		f.write("""<tr><td>%s</td> </tr>""" % words.encode('utf8'))
	f.write("""</table></div>""")
	f.write("""</div></body></html>""")
	f.close()
	webbrowser.open_new_tab('html/dictionary.html')


