import unittest
from lda import documentCollection
from lda import document
from lda import dictionary
from lda import entities

class testDocumentCollection(unittest.TestCase):
    
    def setUp(self):
        self.collection = documentCollection(' ')
    
    def test_createDictionary(self):
        self.collection.documents = [document('doc1', 'Test -tokenization- and if common words are deleted.'), document('doc2', 'stopwords like of, and, but?'), document('doc3', 'special\ characters?\n, Article\n\n78(5), constitution references 103/93 and dates 23.01.1998 or 12th of March 2003')]
        self.collection.createDictionary()

        targetDictionary = dictionary()
        targetDictionary.words = set(['test', '-tokenization-', 'and', 'if','common', 'words','are','deleted','.','stopwords','like','of',',','but','?','special\\','characters','article','78','(','5',')','constitution','references','103/93','dates','23.01.1998','or', '12th','march','2003'])
        targetDictionary.stopwords = set([])

        for attribute in targetDictionary.__dict__.keys():
            self.assertEqual(getattr(self.collection.dictionary, attribute), getattr(targetDictionary, attribute))
        
        # self.collection.createDictionary()
        # self.assertEqual(self.collection.dictionary, set(['test','like','-tokenization-','common','words','deleted','.','stopwords',',','?','special\\','characters','article','78','(','5',')','constitution','references','103/93','78','dates','23.01.1998','12th','march','2003']))
       
    def test_getNamedEntities(self):
        self.collection.documents = [document('doc1','Test named entity recognition of a Collection of documents.'),document('doc2',' African Commission is a named entity, also countries like Senegal and Lybia and names like Peter and Anna.'),document('doc3', 'Also organizations like the United Nations or UNICEF should be recognized.')]
        testEntities = entities('')
        testEntities.addEntities('ORGANIZATION', set([u'African Commission', u'UNICEF', u'United Nations']))
        testEntities.addEntities('PERSON', set([u'Anna', u'Peter']))
        testEntities.addEntities('LOCATION', set([u'Senegal', u'Lybia']))
        self.collection.getNamedEntities()
        self.assertEqual(testEntities.__dict__, self.collection.entities.__dict__)

    def tearDown(self):
        del self.collection

if __name__ == '__main__':
    unittest.main()

