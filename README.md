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

To install NLTK Data run the Python interpreter with the commands:
```
import nltk
nltk.download()
```
* [pandas](http://pandas.pydata.org/pandas-docs/stable/install.html) <br />
pandas is a Python package providing fast, flexible, and expressive data structures designed to make working with structured (tabular, multidimensional, potentially heterogeneous) and time series data both easy and intuitive. To read excel files also the xlrd packages is required.
```
pip install pandas
pip install xlrd
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
In the **TopicModeling** and **frequencyAnalysis** files the following parameters can be adapted:
* *path* - path to the location of the documents
* *fileType* - specifies how the documents are stored and loaded: one of *csv*, *couchdb*, *folder* 
* *startDoc* - index of document to start upload
* *numberDoc* - specifies how many documents are processed - set to *None* to load all documents
* *preprocess* - boolean operator to force preprocessing
* *numberTopics* - specify how many topics are extracted
* *specialChars* - remove these characters from text
* *dictionaryWords* - set words in dictionary manually. *None* if not applicable
* *keywords* - check frequency of manually set keywords 
* *fileName* - save preprocessed document objects at *filename*

The **classification** script by default loads a csv file.
* *path* - specifies the location and name of the file
* *predictColumn* - determines which column is selected to be classified
* *dropList* - contains all columns that are ignored in the classification


## Testing
The folder *Unittests* contains the tests corresponding to each module. [*nose*](http://nose.readthedocs.org/) provides an easy way to run all tests together. <br  />
Install *nose* with:
```
pip install nose
```
Run the tests with:
```
nosetests Unittests/
```
