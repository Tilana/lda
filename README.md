#lda

lda provides a framework to analyse different collections of documents:
 * *topicModeling.py* - uses gensim to extract the most relevant topics
 * *frequencyAnalysis.py* - returns most frequent words based on the Stanford Named-Entity Recognizer
 * *classification.py* - analysis and classification of document features with scikit-learn
 
##Dependencies

* [gensim - Topic Modeling for Humans](https://radimrehurek.com/gensim/install.html) <br />
Gensim is a free Python library designed to automatically extract semantic topics from documents by implementing Latent Semantic Analysis, Latent Dirichlet Allocation and Term-Frequency Inverse-Document Frequency models.
```
pip install --upgrade gensim
```
* [Scikit-learn - Machine Learning for Python](http://scikit-learn.org/stable/install.html) <br />
Scikit-learn is an open source machine learning library which includes various classification, regression and clustering algorithms like support vector machines, random forests, naive bayes and k-means.
```
pip install -U scikit-learn
```
* [NLTK](http://www.nltk.org/install.html) <br />
NLTK provides various tools to work with texts written in natural language. For this project tokenization, stemming and tagging are used.
```
sudo pip install -U nltk
``` 
* [pandas](http://pandas.pydata.org/pandas-docs/stable/install.html) <br />
pandas is a Python package providing fast, flexible, and expressive data structures designed to make working with structured (tabular, multidimensional, potentially heterogeneous) and time series data both easy and intuitive.
```
pip install pandas
```
* [Stanford Named Entity Recognizer (NER)](http://nlp.stanford.edu/software/CRF-NER.shtml) <br />
Stanford Named Entity Recognizer labels sequences of words in a text which represent proper names for persons, locations and organizations. The Stanford NER is included in this repository.


## Scripts
Use the following command to run the scripts:
```
python topicModeling.py
python frequencyAnalysis.py
python classification.py
```
Parameters and the document collection used for the analysis can be changed withing the corresponding script file.

##Testing
The folder *Unittests* contains the tests corresponding to each module. [*nose*](http://nose.readthedocs.org/) provides an easy way to run all tests together. <br  />
Install *nose* with:
```
pip install nose
```
Run the tests with:
```
nosetests Unittests/
```
