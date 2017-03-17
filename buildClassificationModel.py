#from lda import ClassificationModel, Viewer, Info
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB, GaussianNB

def buildClassificationModel():

    nrLabels = 5000
    data = pd.read_pickle('Documents/ICAAD/ICAAD.pkl')
    docs = data.text.tolist()
    labels = data['Sexual.Assault.Manual'].tolist()

    vectorizer = TfidfVectorizer(min_df=10, max_df=0.8, stop_words='english', ngram_range = (1,2))
    wordCounts = vectorizer.fit_transform(docs) #.toarray()

    clf = MultinomialNB(alpha=0.2)
    clf = BernoulliNB(alpha=0.1)
    clf = GaussianNB()
    clf.fit(wordCounts[0:nrLabels], labels[0:nrLabels])
    pred = clf.predict(wordCounts[nrLabels:])
    predProbability = clf.predict_proba(wordCounts[nrLabels:])
                                                          
    accuracy = accuracy_score(labels[nrLabels:], pred)
    precision = precision_score(labels[nrLabels:], pred)
    recall = recall_score(labels[nrLabels:], pred)
    print 'Test Accuracy: %f' % accuracy 
    print 'Test Precision: %f' % precision 
    print 'Test Recall: %f' % recall 


if __name__=='__main__':
    buildClassificationModel()

