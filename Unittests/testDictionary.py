import unittest
from lda import Dictionary
from lda import entities
from lda import document

class testDictionary(unittest.TestCase):

    def setUp(self):
        self.doc = document('TestDoc','Test to see if this text is added to dictionary.words')
        self.testDictionary = Dictionary()
        self.targetDictionary = Dictionary()

    def test_removeShortWords(self):
        self.testDictionary.words = set(['remove', 'too', '.', 'short', 'ab', 'words'])
        self.testDictionary.removeShortWords(threshold=2)
        self.targetDictionary.words = set(['remove', 'too', 'short',  'words'])

        self.assertEqual(self.targetDictionary.words, self.testDictionary.words)


    def test_addDocument(self):
        self.testDictionary.words.update(['words', 'already', 'added', 'to', 'dictionary'])
        self.testDictionary.addDocument(self.doc)
        
        self.targetDictionary.words= set(['test', 'words', 'already', 'dictionary', 'to', 'see', 'if', 'this', 'text', 'is', 'added', 'to', 'dictionary.words'])
        self.compareDictionaries()

    def test_setDictionary(self):
        wordList = ['Create', 'dictionary entries', 'manually']
        self.testDictionary.setDictionary(wordList)
        self.targetDictionary.words = set(['create', 'dictionary entries', 'manually'])
        self.assertEqual(self.targetDictionary.words, self.testDictionary.words)
    
    def test_createDictionaryIds(self):
        self.testDictionary.words = set(['test', 'if', 'this', 'test', 'set', 'is', 'converted', 'to', 'a', 'dictionary', 'representation', 'with', 'a', 'corpus'])
        self.testDictionary.createDictionaryIds()
        self.targetDictionary.ids = {7:u'test', 11:u'if', 3:u'this', 1:u'set', 4:u'is', 6:u'converted', 5:u'to', 0:u'a', 2:u'dictionary', 8:u'representation', 9:u'corpus', 10:u'with'}
        self.assertEqual(self.testDictionary.ids.items(), self.targetDictionary.ids.items())

    def test_createEntityDictionary(self):
        self.testDictionary.entities = entities()
        self.testDictionary.entities.addEntities('LOCATION', ['New York', 'Sevilla', 'United States of America'])
        self.testDictionary.entities.addEntities('PERSON', ['Stephen Hawking', 'Peter Pan'])

        self.testDictionary.createEntityDictionary('LOCATION')

        self.targetDictionary.LOCATIONdictionary = {2:u'New York', 0:u'Sevilla', 1:u'United States of America'}

        self.assertEqual(self.testDictionary.LOCATIONdictionary.items(), self.targetDictionary.LOCATIONdictionary.items())

    def test_getDictionaryId(self):
        self.targetDictionary.ids = {7:u'test', 11:u'if', 3:u'this', 1:u'set', 4:u'is', 6:u'converted', 5:u'to', 0:u'a', 2:u'dictionary', 8:u'representation', 9:u'corpus', 10:u'with'}
        self.assertEqual(9, self.targetDictionary.getDictionaryId('corpus'))
        self.assertEqual(7, self.targetDictionary.getDictionaryId('test'))

   
    def test_addDocumentEmptyDict(self):
        self.testDictionary.addDocument(self.doc)
        self.targetDictionary.words= set(['test', 'to', 'see', 'if', 'this', 'text', 'is', 'added', 'to', 'dictionary.words'])

        self.compareDictionaries()
    
    def test_addCollection(self):
        collection = [document('doc1', 'Test 1.'), document('doc2', 'Test 2?'), document('doc3', 'Test 3!')]
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

    def test_addWords(self):
        self.testDictionary.words = set(['words', 'in', 'dictionary'])
        self.testDictionary.stopwords = set(['to', 'also'])

        self.testDictionary.addWords(['words', 'to', 'add', 'also', 'separated entities'])
        self.targetDictionary.words = set(['words', 'in', 'dictionary', 'add', 'separated entities'])
        self.targetDictionary.stopwords = set(['to','also'])
        
        self.compareDictionaries()

    
    def compareDictionaries(self):
        for attribute in self.targetDictionary.__dict__.keys():
            self.assertEqual(getattr(self.targetDictionary, attribute), getattr(self.testDictionary, attribute))
    
    def test_createEntities(self):
        testDictionary = Dictionary()
        collection = [document('doc1','Test named entity recognition of a Collection of documents.'),document('doc2',' African Commission is a named entity, also countries like Senegal and Lybia and names like Peter and Anna.'),document('doc3', 'Also organizations like the United Nations or UNICEF should be recognized.')]
        testEntities = entities('')
        testEntities.addEntities('ORGANIZATION', set([(u'african commission',1), (u'unicef', 1), (u'united nations', 1)]))
        testEntities.addEntities('PERSON', set([(u'anna',1), (u'peter',1)]))
        testEntities.addEntities('LOCATION', set([(u'senegal',1), (u'lybia',1)]))
        testDictionary.createEntities(collection)
        self.assertEqual(testEntities.__dict__, testDictionary.entities.__dict__)




if __name__ =='__main__':
    unittest.main()
