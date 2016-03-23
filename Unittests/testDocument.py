import unittest
from lda import document
from lda import entities

class testDocument(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_getNamedEntities(self):
        testDocument = document('Test Document','Name entities like World Health Organization, person names like Sir James and Ms Rosa Wallis but also locations like Lebanon, United States of America or cities like New York have to be recognized')
        emptyDocument = document('','')
        testDocument.getNamedEntities()
        emptyDocument.getNamedEntities()
        
        emptyDocument.entities.LOCATION = [u'United States of America', u'Lebanon', u'New York']
        emptyDocument.entities.PERSON = [u'Sir James', u'Ms Rosa Wallis']
        emptyDocument.entities.ORGANIZATION = [u'World Health Organization']
        
        self.assertTrue(testDocument.entities.__dict__, emptyDocument.entities.__dict__)
        

if __name__ == '__main__':
    unittest.main()
