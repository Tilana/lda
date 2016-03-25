import unittest
from lda import dictionary
from lda import document
from lda import documentCollection

class testDictionary(unittest.TestCase):

    def setUp(self):
        self.doc = document('TestDoc','Test to see if this text is added to dictionary.words')
        self.testDictionary = dictionary()
        self.targetDictionary = dictionary()

    def test_addDocument(self):
        self.testDictionary.words.update(['words', 'already', 'added', 'to', 'dictionary'])
        self.testDictionary.addDocument(self.doc)
        
        self.targetDictionary.words = set(['test', 'words', 'already', 'dictionary', 'to', 'see', 'if', 'this', 'text', 'is', 'added', 'to', 'dictionary.words'])
        self.compareDictionaries()
    
    def test_addDocumentEmptyDict(self):
        self.testDictionary.addDocument(self.doc)
        self.targetDictionary.words = set(['test', 'to', 'see', 'if', 'this', 'text', 'is', 'added', 'to', 'dictionary.words'])

        self.compareDictionaries()
    
    def test_addCollection(self):
        collection = documentCollection(' ')
        collection.documents = [document('doc1', 'Test 1.'), document('doc2', 'Test 2?'), document('doc3', 'Test 3!')]
        self.testDictionary.addCollection(collection)

        self.targetDictionary.words = set(['test', '1', '.', '2', '?', '3', '!'])
        self.compareDictionaries()

    def test_addStopwordsEmptyList(self):
        self.testDictionary.words = set(['add', 'words', 'to','dictionary'])
        self.testDictionary.addStopwords(['add', 'WORDS', 'to', 'stoplist'])
        
        self.targetDictionary.words = set(['dictionary'])
        self.targetDictionary.stopwords = set(['add', 'words','to', 'stoplist'])
        self.compareDictionaries()

    def test_addStopwordsSet(self):
        self.testDictionary.stopwords = set(['already', 'in', 'stoplist'])
        self.testDictionary.addStopwords(set(['add', 'WORDS', 'to', 'stoplist']))
        self.targetDictionary.stopwords = set(['already', 'in','add', 'words','to', 'stoplist'])
        self.compareDictionaries()

    def test_removeStopwords(self):
        self.testDictionary.stopwords = set(['words', 'to', 'remove'])
        self.testDictionary.words = set(['words', 'in', 'dictionary'])
        self.testDictionary.removeStopwords()

        self.targetDictionary.stopwords = set(['words', 'to', 'remove'])
        self.targetDictionary.words = set(['in', 'dictionary'])

        self.compareDictionaries()

    
    def compareDictionaries(self):
        for attribute in self.targetDictionary.__dict__.keys():
            self.assertEqual(getattr(self.targetDictionary, attribute), getattr(self.testDictionary, attribute))


if __name__ =='__main__':
    unittest.main()
