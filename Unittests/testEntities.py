import unittest
from lda import entities

class testEntities(unittest.TestCase):
    
    def setUp(self):
        self.testEntities = entities('This is a Text to see if locations like Beirut in Lebanon, but also locations and organisations are recognized. Charles Isaac Leopold is working for the World Health Organisation and the UN in the United States of America.')
        
    def test_getEntities(self):
        targetEntities = [(u'world health organisation', 1), (u'un', 2), (u'lebanon', 1), (u'beirut', 1), (u'united states of america', 1), (u'charles isaac leopold', 1)]
        self.assertEqual(set(self.testEntities.getEntities()), set(targetEntities))


    def test_getEntitiesAddedEntities(self):
        testEntity = entities()
        testEntity.addEntities('LOCATION', [('london', 1), ('new york', 2), ('San Diego', 1)])

        targetEntities = [('london', 1), ('new york', 2), ('San Diego', 1)]
        self.assertEqual(testEntity.getEntities(), targetEntities)


    def test_isEmpty(self):
        emptyEntity = entities()
        self.assertTrue(emptyEntity.isEmpty())

        self.assertFalse(self.testEntities.isEmpty())


    def test_countOccurence(self):
        entityList = entities()
        entityList.addEntities('ORGANIZATION', set([u'African Commission', u'United Nations', u'Human Rights Council']))
        entityList.addEntities('LOCATION', set([u'Gambia', 'United States of America']))
        text = 'The Human Rights Council in Gambia and the United Nations in the United States of America and the Human Rights Council and Gambiar should appear in the counter'

        targetOrganization = set([(u'united nations', 1), (u'human rights council', 2)])
        targetAllEntities = set([(u'united nations', 1), (u'human rights council', 2), (u'gambia', 2), (u'united states of america',1)])

        self.assertEqual(set(entityList.countOccurence(text, 'ORGANIZATION')), targetOrganization)

        self.assertEqual(set(entityList.countOccurence(text)), targetAllEntities)
        print entityList.countOccurence(text)
        
if __name__ == '__main__':
    unittest.main()
