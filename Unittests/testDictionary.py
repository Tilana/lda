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
        self.testDictionary.words = self.testDictionary.words.union(['words', 'already', 'added', 'to', 'dictionary'])
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
    
    def compareDictionaries(self):
        for attribute in self.targetDictionary.__dict__.keys():
            self.assertEqual(getattr(self.targetDictionary, attribute), getattr(self.testDictionary, attribute))
            
if __name__ =='__main__':
    unittest.main()
