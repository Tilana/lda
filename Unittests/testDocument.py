import unittest
from lda import document
from lda import entities

class testDocument(unittest.TestCase):
    
    def setUp(self):
        self.targetDocument = document('','')
        self.targetDocument.createEntities()

    def test_lemmatizeTokens(self):
        testDocument = document('','')
        testDocument.tokens = set(['children', 'forced', 'trafficking', 'prisons', 'arrested',  'United Nations', '12.03.1992', 'are', 'violations', 'bags of words'])
        testDocument.lemmatizeTokens()

        self.targetDocument.tokens = set(['child', 'United Nations', '12.03.1992', 'be', 'violation', 'force', 'arrest', 'traffic', 'prison', 'bags of words'])

        self.assertEqual(testDocument.tokens, self.targetDocument.tokens)

    def test_deleteSpecialCharacterTokens(self):
        testDocument = document('', '')
        testDocument.tokens = set(['child`s', '23.09.1998', 'test entity', 'normal', '$200 000', '809/87', 'http://asfd.org', 'talib@n?'])
        testDocument.deleteSpecialCharacterTokens()

        self.targetDocument.tokens = set(['child`s', '23.09.1998', '809/87', '$200 000', 'test entity', 'normal'])
        self.assertEqual(testDocument.tokens, self.targetDocument.tokens)
    

    def test_createTokens(self):
        testDocument = document('Test Doc', 'Test of tokenization\n dates like 12.03.1998, 103/78 and World Health Organisation should be kept together. Words appear more more often.?')
        stoplist = [u'and', u'.', u'?', u'of']
        testDocument.createEntities()
        print testDocument.entities.ORGANIZATION

        testDocument.createTokens(stoplist)
        self.targetDocument.tokens = ['test','tokenization','dates','like','12.03.1998',',','103/78', 'world health organisation', 'should', 'be', 'kept', 'together', 'words', 'appear', 'more', 'more', 'often']
        self.assertEqual(testDocument.tokens, self.targetDocument.tokens)

    def test_includeEntities(self):
        testDocument = document('Test Document','Name entities like World Health Organization, person names like Sir James and Ms Rosa Wallis but also world locations or states like Lebanon, United States of America or new cities like New York have to be recognized')
        testDocument.createEntities()
        testDocument.createTokens()
        testDocument.includeEntities()

        self.targetDocument.tokens = ['name', 'entities', 'like', 'world health organization', ',', 'person', 'names', 'like', 'sir', 'james', 'and', 'ms', 'rosa wallis', 'but', 'also', 'world', 'locations', 'or', 'states', 'like', 'lebanon', ',', 'united states of america', 'or', 'new', 'cities', 'like', 'new york', 'have', 'to', 'be', 'recognized']
        self.assertEqual(self.targetDocument.tokens, testDocument.tokens)

    
    def test_createEntities(self):
        testDocument = document('Test Document','Name entities like World Health Organization, person names like Sir James and Ms Rosa Wallis but also locations like Lebanon, United States of America or cities like New York have to be recognized')
        testDocument.createEntities()
        
        self.targetDocument.entities.LOCATION = [u'United States of America', u'Lebanon', u'New York']
        self.targetDocument.entities.PERSON = [u'Sir James', u'Ms Rosa Wallis']
        self.targetDocument.entities.ORGANIZATION = [u'World Health Organization']
        
        self.assertTrue(testDocument.entities.__dict__, self.targetDocument.entities.__dict__)
        

if __name__ == '__main__':
    unittest.main()
