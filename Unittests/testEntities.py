import unittest
from lda import entities

class testEntities(unittest.TestCase):
    
    def setUp(self):
        self.testEntities = entities('This is a Text to see if locations like Beirut in Lebanon, but also locations and organisations are recognized. Charles Isaac Leopold is working for the World Health Organisation and the UN in the United States of America.')
        
    def test_getEntities(self):
        targetEntities = [u'World Health Organisation', u'UN', u'Lebanon', u'Beirut', u'United States of America', u'Charles Isaac Leopold']
        self.assertEqual(set(self.testEntities.getEntities()), set(targetEntities))

    def test_isEmpty(self):
        emptyEntity = entities()
        self.assertTrue(emptyEntity.isEmpty())

        self.assertFalse(self.testEntities.isEmpty())


    def test_countOccurence(self):
        entityList = entities()
        entityList.addEntities('ORGANIZATION', set([u'African Commission', u'United Nations', u'Human Rights Council']))
        entityList.addEntities('LOCATION', set([u'Gambia', 'United States of America']))
        text = 'The Human Rights Council and the United Nations and the Human Rights Council appear in this test'

        target = set([(u'African Commission', 0), (u'United Nations', 1), (u'Human Rights Council', 2)])

        self.assertEqual(set(entityList.countOccurence(text, 'ORGANIZATION')), target)


        
if __name__ == '__main__':
    unittest.main()
