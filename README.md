#lda

lda provides a framework to analyse different collections of documents:
 * *topicModeling.py* - uses gensim to extract the most relevant topics
 * *frequencyAnalysis.py* - returns most frequent words based on the Stanford Named-Entity Recognizer
 * *classification.py* - analysis and classification of document features with scikit-learn
 
#Dependencies

* [gensim - Topic Modeling for Humans](https://radimrehurek.com/gensim/install.html)
```pip install --upgrade gensim```
* [Scikit-learn - Machine Learning for Python](http://scikit-learn.org/stable/install.html)
``` pip install -U scikit-learn ```
* [NLTK](http://www.nltk.org/install.html)
``` sudo pip install -U nltk ``` 
* [pandas](http://pandas.pydata.org/pandas-docs/stable/install.html)
``` pip install pandas ```
* [Stanford Name Entity Recognizer (NER)](http://nlp.stanford.edu/software/CRF-NER.shtml)
included in folder
