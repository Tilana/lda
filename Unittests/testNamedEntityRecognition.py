import unittest
from lda import namedEntityRecognition

class testNamedEntityReconition(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_getNamedEntities(self):
        text = 'This is a Text to see if locations like Beirut in Lebanon, but also locations and organisations are recognized. Charles Isaac Leopold is working for the World Health Organisation and the UN in the United States of America.'
        entities = set([('Beirut','LOCATION'),('Lebanon','LOCATION'),('Charles Isaac Leopold', 'PERSON'), ('World Health Organisation', 'ORGANIZATION'), ('UN','ORGANIZATION'), ('United States of America','LOCATION')])
        self.assertEqual(namedEntityRecognition.getNamedEntities(text), entities)

if __name__ == '__main__':
    unittest.main()
