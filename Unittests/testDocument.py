import unittest
from lda import document
from lda import entities

class testDocument(unittest.TestCase):
    
    def setUp(self):
        self.emptyDocument = document('','')
        self.emptyDocument.getNamedEntities()
    
    def test_getWords(self):
        testDocument = document('Test Doc', 'Test of tokenization\n dates like 12.03.1998, 103/78 and later also Article 7 should be kept together.?')
        testDocument.getWords()
        self.emptyDocument.words = set([u'test',u'of',u'tokenization',u'dates',u'like',u'12.03.1998',u',',u'103/78', u'and', u'later', u'also',u'article',u'7',u'should', u'be', u'kept', u'together', u'.', u'?'])
        self.assertEqual(testDocument.words, self.emptyDocument.words)

    
    def test_getNamedEntities(self):
        testDocument = document('Test Document','Name entities like World Health Organization, person names like Sir James and Ms Rosa Wallis but also locations like Lebanon, United States of America or cities like New York have to be recognized')
        testDocument.getNamedEntities()
        
        self.emptyDocument.entities.LOCATION = [u'United States of America', u'Lebanon', u'New York']
        self.emptyDocument.entities.PERSON = [u'Sir James', u'Ms Rosa Wallis']
        self.emptyDocument.entities.ORGANIZATION = [u'World Health Organization']
        
        self.assertTrue(testDocument.entities.__dict__, self.emptyDocument.entities.__dict__)
        

if __name__ == '__main__':
    unittest.main()
