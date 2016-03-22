import unittest
from lda import documentCollection

class testDocumentCollection(unittest.TestCase):
    
    def setUp(self):
        self.collection = documentCollection(' ')
        self.collection.titles = ['doc1','doc2','doc3']
    
    def test(self):
        self.assertTrue(True)
    
    def test_createDictionary(self):
        self.collection.documents = ['Test -tokenization- and if common words are deleted.', 'stopwords like of, and, but?','special\ characters?\n, Article\n\n78(5), constitution references 103/93 and dates 23.01.1998 or 12th of March 2003']
        self.collection.createDictionary(rmStopwords=False)
        self.assertEqual(self.collection.dictionary, set(['test', '-tokenization-', 'and', 'if','common', 'words','are','deleted','.','stopwords','like','of',',','but','?','special\\','characters','article','78','(','5',')','constitution','references','103/93','dates','23.01.1998','or', '12th','march','2003']))
        self.collection.createDictionary()
        self.assertEqual(self.collection.dictionary, set(['test','like','-tokenization-','common','words','deleted','.','stopwords',',','?','special\\','characters','article','78','(','5',')','constitution','references','103/93','78','dates','23.01.1998','12th','march','2003']))
       
    def test_getNamedEntities(self):
        self.collection.documents = ['Test named entity recognition of a Collection of documents.',' African Commission is a named entity, also countries like Senegal and Lybia and names like Peter and Anna.','Also organizations like the United Nations or UNICEF should be recognized.']
        testEntities = [[('ORGANIZATION', []), ('LOCATION', []), ('PERSON', [])], [('ORGANIZATION', [u'African Commission']), ('LOCATION', [u'Senegal',u'Lybia']), ('PERSON', [u'Anna', u'Peter'])], [('ORGANIZATION', [u'UNICEF', u'United Nations']),('LOCATION', []), ('PERSON', [])]]
        self.collection.getNamedEntities()
        self.assertEqual(testEntities, self.collection.namedEntities)
    
    def tearDown(self):
        del self.collection

if __name__ == '__main__':
    unittest.main()

