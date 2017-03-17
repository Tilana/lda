import os
import sys
import copy
import numpy as np
from scipy.special import digamma
from sklearn.feature_extraction.text import CountVectorizer
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
print ROOT_DIR
os.environ['BNPYROOT'] = os.path.join(ROOT_DIR, 'bnpy-dev')
os.environ['BNPYOUTDIR'] = os.path.join(ROOT_DIR, 'bnpy-out')
sys.path.append(os.environ['BNPYROOT'])
sys.path.append(os.environ['BNPYROOT'] + '/third-party/spectral/')
import bnpy
import logging


def preprocess(corpus):
    """
    Given a dataframe consisting text content, preprocess for topic modeling

    :param corpus: The dataframe containing url and content (at a minimum)
    :param min_document_frequency: the minimum number of documents a word term has to appear in
    :param max_document_frequency: the maximum number of documents a word can appear in
    :param language: Language of the corpus
    :return: the bnpy data object and a learned vocabulary
    """
    stopwords = set([x.strip() for x in open(os.path.join(ROOT_DIR, "stopwords", "english.txt"))])
    MIN_DOCUMENT_FREQUENCY = 8 
    MAX_DOCUMENT_FREQUENCY = 1200 

    nDocs = len(corpus['text'])
    text = corpus['text'].get_values()

    MAX_FEATURES = 8000
    print "Vectorizing corpus with maximum features set to " + str(MAX_FEATURES)
    vectorizer = CountVectorizer(analyzer='word',
                                      ngram_range=(1,2),
                                      token_pattern='[a-zA-Z]+',
                                      max_df=MAX_DOCUMENT_FREQUENCY,
                                      min_df=MIN_DOCUMENT_FREQUENCY,
                                      stop_words=stopwords,
                                      max_features=MAX_FEATURES,
                                      binary=True)\

    #vectorizer.fit_transform(text)
    word_counts = vectorizer.fit_transform(text)
    #t = word_counts.tocsr()
    vocabulary = vectorizer.get_feature_names()
    tokens = [[vocabulary[index] for index in doc.indices] for doc in word_counts]

    # Begin the process of converting this into a wordsData item
    #docrange = []
    #word_id = []
    #word_count = []
    #start = 0
    #total_docs = 0
    #skipped_docs = 0
    #for ii in xrange(nDocs):
    #    #if len(word_counts.getrow(ii).indices) > 20:
    #    # we want the document to have at least 20 tokens
    #    word_id.extend(word_counts.getrow(ii).indices)
    #    word_count.extend(word_counts.getrow(ii).data)
    #    end = start + len(word_counts.getrow(ii).indices)
    #    docrange.append([start, end])
    #    start = end
    #    total_docs += 1
    #    #else:
    #    #    skipped_docs += 1

    #print "Building BNPy Data Object"
    #bnpy_data = bnpy.data.WordsData(word_id, word_count, docrange, len(vocabulary), vocabulary, len(docrange))
    #bnpy_data.name = "readerscope"
    #print "Number of Documents Skipped: " + str(skipped_docs)

    return vocabulary, tokens 

def learn(bnpy_data, nTask=2, numK=20, gamma=10, alpha=0.5, lam=0.1, nlap=20, nbatch=2, savefid='newTest', taskid=1):
    '''
    This runs the actual topic model
    :param bnpy_data:
    :param nTask:
    :param numK:
    :param gamma:
    :param alpha:
    :param lam:
    :param nlap:
    :param nbatch:
    :param savefid:
    :param taskid:
    :return:
    '''
    #model = bnpy.Run.run(bnpy_data, 'HDPTopicModel', 'Mult', 'moVB', #'memoVB'
    model = bnpy.Run.run(bnpy_data, 'HDPTopicModel', 'Mult', 'VB', #'moVB', #'memoVB'
                          doSaveToDisk=False,
                          jobname=savefid, taskid=taskid,
                          K=numK, nLap=nlap, nBatch=nbatch,
                          moves='merge,delete', mergePairSelection='corr',
                          gamma=gamma, alpha=alpha, lam=lam,
                          doMemoizeLocalParams=0, restartLP=1,
                          restartNumTrialsLP=50, restartNumItersLP=2,
                          m_startLap=10, d_startLap=10, nTask=nTask,
                          nCoordAscentItersLP=100, convThrLP=0.001, doFullPassBeforeMstep=1,
                          initname='randomfromprior')
                          #initname='randexamples')
                          #initname="anchorwordtopics")

    beta = model[0].obsModel.Post.lam
    model_score = model[1]['evBound']
    return beta, model_score, model

def generate_theta(beta, vocabulary, text):
    """
    generate_theta is a function that takes in a new piece of text and fits the currently learned topic model
    to that text. It answers the question; given a set of global topics, what is the best topic decomposition for it?

    :param: beta: the set of global topics learned from the topic model
    :param: vocabulary: the unique vocabulary for the topic model
    :param: text: text that has been stripped of its html tags
    :return: theta: normalized topic vector
    """

    # Convert the raw text into word indices
    alpha = 0.2
    count = CountVectorizer(vocabulary=vocabulary)
    wfreq = count.fit_transform([text])
    wc = wfreq.data.astype(float)
    word_ind = wfreq.nonzero()[1]
    num_tokens = len(word_ind)
    num_topics = len(beta)
    counter = 0

    # Calculate E[log(X)]
    elog_beta = digamma(beta) - digamma(np.sum(beta, axis=1))[:, np.newaxis]

    # Initialize phi to be uniformly distributed
    phi = np.ones((num_tokens, num_topics)) / num_topics

    # Run our local steps to learn theta
    theta_old = np.zeros(num_topics) + alpha
    theta_new = alpha + np.dot(phi.T, wc)
    elog_theta = digamma(theta_new) - digamma(np.sum(theta_new))
    iterdiff = 1

    # Iterate through Local E-Step until threshold is met or 100 iterations have passed
    while (iterdiff > CONVERGENCE_THRESHOLD) and (counter < MAX_ITERATIONS):
        # update phi and theta
        for dw in xrange(len(word_ind)):
            wix = word_ind[dw]
            phi[dw, :] = np.exp(elog_beta[:, wix] + elog_theta)
            phi[dw, :] /= np.sum(phi[dw, :])
        theta_new = alpha + np.dot(phi.T, wc)
        elog_theta = digamma(theta_new) - digamma(np.sum(theta_new))

        # check convergence
        iterdiff = np.sum(np.abs(theta_old - theta_new))
        theta_old = copy.deepcopy(theta_new)
        counter += 1

        if iterdiff < CONVERGENCE_THRESHOLD:
            break

        return theta_new / np.sum(theta_new)


