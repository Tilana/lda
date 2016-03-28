import unittest
from lda import entities

class testEntities(unittest.TestCase):
    
    def setUp(self):
        self.testEntities = entities('This is a Text to see if locations like Beirut in Lebanon, but also locations and organisations are recognized. Charles Isaac Leopold is working for the World Health Organisation and the UN in the United States of America.')
        
    def test_getEntities(self):
        targetEntities = [u'World Health Organisation', u'UN', u'Lebanon', u'Beirut', u'United States of America', u'Charles Isaac Leopold']
        self.assertEqual(set(self.testEntities.getEntities()), set(targetEntities))

if __name__ == '__main__':
    unittest.main()
