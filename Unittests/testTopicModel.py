import unittest
import copy
from lda import TopicModel
from lda import document
from lda import dictionary
from lda import entities

class testTopicModel(unittest.TestCase):

    def setUp(self):
        self.testModel = TopicModel()
        self.testModel.dictionary.words = set(['test', 'if', 'this', 'test', 'set', 'is', 'converted', 'to', 'a', 'dictionary', 'representation', 'with', 'a', 'corpus'])
        self.testModel.collection = [document('doc1', 'test corpus representation'), document('doc2', 'a corpus and a test')]
        self.testModel.collection[0].tokens= [u'test', u'corpus', u'representation']
        self.testModel.collection[1].tokens= [u'a', u'corpus', u'and', u'a', u'test']

        self.targetModel = copy.deepcopy(self.testModel)

    def test_createvectorDictionary(self):
        self.testModel.createvectorDictionary()
        self.targetModel.vectorDictionary = {7:u'test', 11:u'if', 3:u'this', 1:u'set', 4:u'is', 6:u'converted', 5:u'to', 0:u'a', 2:u'dictionary', 8:u'representation', 9:u'corpus', 10:u'with'}
        self.assertEqual(self.testModel.vectorDictionary.items(), self.targetModel.vectorDictionary.items())

    def test_createCorpus(self):
        self.testModel.createvectorDictionary()
        self.testModel.createCorpus()
        self.targetModel.corpus = [[(7,1), (8,1), (9,1)], [(0,2),(7,1),(9,1)]]

        self.assertEqual(self.testModel.corpus, self.targetModel.corpus)
    
    def test_createDictionary(self):
        testModel = TopicModel()
        collection = [document('doc1', 'Test -tokenization- and if common words are deleted.'), document('doc2', 'stopwords like of, and, but?'), document('doc3', 'special\ characters?\n, Article\n\n78(5), constitution references 103/93 and dates 23.01.1998 or 12th of March 2003')]
        testModel.createDictionary(collection)

        targetDictionary = dictionary()
        targetDictionary.words = set(['test', '-tokenization-', 'and', 'if','common', 'words','are','deleted','.','stopwords','like','of',',','but','?','special\\','characters','article','78','(','5',')','constitution','references','103/93','dates','23.01.1998','or', '12th','march','2003'])
        targetDictionary.stopwords = set([])

        for attribute in targetDictionary.__dict__.keys():
            self.assertEqual(getattr(testModel.dictionary, attribute), getattr(targetDictionary, attribute))
    
    def test_createEntities(self):
        testModel = TopicModel()
        testModel.collection = [document('doc1','Test named entity recognition of a Collection of documents.'),document('doc2',' African Commission is a named entity, also countries like Senegal and Lybia and names like Peter and Anna.'),document('doc3', 'Also organizations like the United Nations or UNICEF should be recognized.')]
        testEntities = entities('')
        testEntities.addEntities('ORGANIZATION', set([u'African Commission', u'UNICEF', u'United Nations']))
        testEntities.addEntities('PERSON', set([u'Anna', u'Peter']))
        testEntities.addEntities('LOCATION', set([u'Senegal', u'Lybia']))
        testModel.createEntities()
        self.assertEqual(testEntities.__dict__, testModel.entities.__dict__)



if __name__ == '__main__':
    unittest.main()


