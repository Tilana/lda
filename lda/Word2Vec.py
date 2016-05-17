from gensim.models import word2vec 
import os

class Word2Vec:

    def __init__(self):
        if os.path.exists('Word2Vec/text8Net.bin'):
            print 'Load trained Word2Vec net'
            self.net = word2vec.Word2Vec.load_word2vec_format('Word2Vec/text8Net.bin', binary = True)
        else:
            print 'Train Word2Vec model with text8 corpus'
            sentences = word2vec.Text8Corpus('Word2Vec/text8')
            self.net = word2vec.Word2Vec(sentences, size=200)
            self.net.init_sims(replace=True)
            self.net.save_word2vec_format('Word2Vec/text8Net.bin', binary=True)


