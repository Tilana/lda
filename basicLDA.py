from lda import Controller
from lda import Word2Vec
import os.path
from gensim.parsing.preprocessing import STOPWORDS
from gensim import corpora, models

def basicLDA():

    filename = 'dataObjects/ICAAD2000_default.txt'
    numberTopics = 20
    specialChars = None


    #### MODEL ####
    print 'Load Documents'
    ctrl = Controller(numberTopics, specialChars)
    ctrl.load(filename)

    print 'Tokenize'
    documents = [doc.text for doc in ctrl.collection]
    tokens = [[word for word in document.lower().split() if word not in STOPWORDS] for document in documents]

    print 'Create Dictionary'
    dictionary = corpora.Dictionary(tokens)
    print dictionary
    dictionary.filter_extremes(no_above=0.45)
    print dictionary
    print 'Create Corpus'
    corpus = [dictionary.doc2bow(text) for text in tokens]
    
    print 'LDA'
    lda = models.ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=10, passes=10, update_every=0)
    print lda.print_topics()

    print 'HDP'
#    hdp = models.hdpmodel.HdpModel(corpus, id2word=dictionary)
#    print hdp.print_topics()



if __name__ == '__main__':
    basicLDA()
