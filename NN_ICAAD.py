import pandas as pd
import numpy as np
import tensorflow as tf
from lda import ClassificationModel, Viewer, Info
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import doc2vec


def NN_ICAAD():

    stopwords = set([x.strip() for x in open("stopwords/english.txt")])
    path = 'Documents/ICAAD/ICAAD.pkl'
    model = ClassificationModel(path, target='Sexual.Assault.Manual')
    model.data = model.data[1:2000]
    texts = model.data['text']

    vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1,2), token_pattern='[a-zA-Z]+', max_df=1200, min_df=1, stop_words=stopwords, max_features=8000)
    vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1,2), token_pattern='[a-zA-Z]+', max_df=1200, min_df=10, stop_words=stopwords, max_features=8000)
    tokens = vectorizer.fit_transform(texts).toarray()
    wordsPerDoc = vectorizer.inverse_transform(tokens)

    labeledDocs2 = [doc2vec.TaggedDocument(words=wordsPerDoc[ind], tags=['ID_%d' % model.data.id.tolist()[ind]]) for ind, doc in enumerate(tokens)]

    doc2vec_model = doc2vec.Doc2Vec(size=70, window=8, min_count=5)
    doc2vec_model.build_vocab(labeledDocs2)

    for epoch in range(10):
        print 'Epoch %d' % epoch
        doc2vec_model.train(labeledDocs2)
        doc2vec_model.alpha -= 0.002
        doc2vec_model.min_alpha = doc2vec_model.alpha

    docvecs = [doc2vec_model.docvecs[ind] for ind in range(0,len(doc2vec_model.docvecs))]
    tokenData = pd.DataFrame(docvecs, dtype='float32')
        
    model.data = pd.concat([model.data, tokenData], axis=1, join_axes=[model.data.index])
    
    
    vocabulary = vectorizer.get_feature_names()
    vocab_dict = dict(zip(range(0,len(vocabulary)), vocabulary))

    model.keeplist = range(0,50) 
    model.droplist = []

    ### SELECT TEST AND TRAINING DATA ###
    model.factorFalseCases = 1 
    model.balanceDataset(model.factorFalseCases)
    model.createTarget()
    model.dropFeatures()
   
    model.dropNANRows() 
    model.numberTrainingDocs = len(model.data)/2
    model.splitDataset(model.numberTrainingDocs)

    ### CLASSIFICATION ###
    model.buildClassifier('DecisionTree')
    model.trainClassifier()
    model.predict()

    model.evaluate()
    model.evaluation.confusionMatrix()

    info = Info()
    info.data = 'ICAAD'
    info.identifier = 'Test_NN'

    html = Viewer(info)
    html.classificationResults(model)



    


    



if __name__=='__main__':
    NN_ICAAD()
