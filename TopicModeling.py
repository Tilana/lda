from gensim import corpora, models, similarities
import pickle

#### UTILITIES ####
# print list of tuples
def printTupleList(list):
    print "\n".join("(%s,%s)" % tup for tup in list)

#### LOAD DATA ####
# get full text documents
with open('fullTextDocs.txt', 'rb') as f:
    documents = pickle.load(f)

# get preprocessed documents
with open('preprocessedfullTexts.txt', 'rb') as f:
    processed_texts = pickle.load(f)

#### build DICTIONARY and CORPUS ####
# create dictionary - a mapping between words and index
dictionary = corpora.Dictionary(processed_texts)
# print(dictionary.token2id)

# convert to bag-of-words vectors (document-term-matrix)
corpus = [dictionary.doc2bow(text) for text in processed_texts]
# print(corpus)

#### TF-IDF ####
# compute document frequency -- term frequency-inverse document frequency
tfidf = models.TfidfModel(corpus, normalize=True)
# convert corpus to tfidf representation
corpus_tfidf = tfidf[corpus]
# return 10 most frequent/important words in one documents
freq_words = sorted(corpus_tfidf[1], key=lambda tup: tup[1], reverse=True)[1:10]
for tup in freq_words:
    print dictionary.get(tup[0]), tup

#### LSI Modeling ###
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=100)
corpus_lsi = lsi[corpus_tfidf]
# print topics and word probabilites
printTupleList(lsi.print_topics(5))

lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=3)
corpus_lsi = lsi[corpus_tfidf]
# print for each document the probability a certain topic is covered
for doc in corpus_lsi[0:5]:
    print(doc)

#### SIMILARITY ANALYSIS ####
# select document and preprocess it
doc = dictionary.doc2bow(documents[2].lower().split())
# convert to lsi space
lsi_doc = lsi[doc]
print lsi_doc

# similarity matrix
index = similarities.MatrixSimilarity(lsi[corpus])
# similarity of one document to all docs in the corpus
sim = index[lsi_doc]

# get most similar topic
index_best = similarities.MatrixSimilarity(lsi[corpus])
index_best.num_best = 5
sim_best = index_best[lsi_doc]
print sim_best
#for sim_doc in sim_best:
#    print documents[sim_doc[0]]

#### TOPIC MODELING #####
# Applying LDA model
ldamodel = models.ldamodel.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=20)
topics = ldamodel.show_topics(num_topics=5, num_words=5, formatted=True)
printTupleList(topics)

# Applying LDA model with tf-idf corpus
ldamodel_tf = models.ldamodel.LdaModel(corpus_tfidf, num_topics=5, id2word=dictionary, passes=20)
topics = ldamodel.show_topics(num_topics=5, num_words=5, formatted=True)
printTupleList(topics)

##### OUTPUT to html file ####
import webbrowser
numTopic = 3
f = open('html/topics.html', 'w')
f.write("<html><head><h1>Topics</h1></head>")

f.write("<body><p>Topics and their related words - LSI Model</p><table>") 
f.write("""<col style="width:7%"> <col style="width:80%">""")
for topic in lsi.print_topics(num_topics=numTopic):
   	f.write("<tr><td><a href='topic%d.html'>Topic %d</a></td><td>%s</td></tr>" % (topic[0], topic[0], str(topic[1])))

f.write("</table>")
f.write("</body></html>")
f.close()

filename = '//home/natalie/Documents/Huridocs/LDA/html/'+'topics.html'
webbrowser.open_new_tab(filename)

# Create a html page for each topic
for num in range(0, numTopic): 
	pagename = 'html/topic%d.html' % num
	f = open(pagename, 'w')
	f.write("<html><head><h1>Document Relevance for Topic %d</h1></head>" % num)
	
	f.write("<body><table>") 
	f.write("""<col style="width:40%"> <col style="width:50%">""")
	# get index and relevance for each document regarding a topic
	# TODO: check meaning of negative numbers -> take absolute value if necessary
	relDocs = sorted(enumerate([doc[num][1] for doc in corpus_lsi]), reverse=True, key=lambda x:abs(x[1]))
	for doc in relDocs[0:15]:
		f.write("<tr><td><a href='doc%02d.html'>Document %d</a></td><td>Relevance: %.2f</td></tr>" % (doc[0], doc[0], doc[1]))

	f.write("</table><p>Test</p></body></html>")
	f.close()


# Create a html page for each document
for ind,doc in enumerate(documents): 
	pagename = 'html/doc%02d.html' % ind
	f = open(pagename, 'w')
	f.write("<html><head><h1>Document %02d</h1></head>" % ind)
	f.write("""<body><div style="width:100%;"><div style="float:right; width:40%;">""")
	f.write("""<h3>Topic coverage: \n</h3><table>""")
	f.write("""<col style="width:40%"> <col style="width:50%">""")
	for num in range(0, numTopic):
		f.write("""<tr><td><a href='topic%d.html'>Topic %d</a</td><td> Coverage %.2f</td></tr>""" % (num, num, corpus_lsi[ind][num][1]))
	f.write("</table>")
	f.write("""<h3>Relevant Words in Document: \n</h3><table>""")
	f.write("""<col style="width:40%"> <col style="width:50%">""")
	freq_words = sorted(corpus_tfidf[ind], key=lambda tup: tup[1], reverse=True)[1:10]
	for tup in freq_words:
		f.write("""<tr><td>%s </td><td> %.2f</td></tr>""" % (dictionary.get(tup[0]).encode('utf8'), tup[1]))
	f.write("</table>")
	
	lsi_doc = lsi[dictionary.doc2bow(documents[ind].lower().split())]
	# get most similar topics
	index_best = similarities.MatrixSimilarity(lsi[corpus], num_best=7)
	sim_best = index_best[lsi_doc]
	f.write("""<h3>Similar documents: \n</h3><table>""")
	f.write("""<col style="width:40%"> <col style="width:50%">""")
	for simDoc in sim_best:
		f.write("""<tr><td><a href='doc%02d.html'>Document %d</a></td>""" % (simDoc[0], simDoc[0]))
		f.write("""<td> Similarity: %.4f</td></tr>""" % simDoc[1])
	f.write("""</table></div>""")
	f.write("""<div style="float:left; width:55%%;"><p>%s</p></div></div></body></html>""" % doc.encode('utf8'))
	f.close()

