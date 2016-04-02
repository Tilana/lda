import unittest
import copy
from lda import TopicModel
from lda import document

class testTopicModel(unittest.TestCase):

    def setUp(self):
        self.testModel = TopicModel()
        self.testModel.collection.dictionary.words = set(['test', 'if', 'this', 'test', 'set', 'is', 'converted', 'to', 'a', 'dictionary', 'representation', 'with', 'a', 'corpus'])
        self.testModel.collection.documents = [document('doc1', 'test corpus representation'), document('doc2', 'a corpus and a test')]
        self.testModel.collection.documents[0].tokens= [u'test', u'corpus', u'representation']
        self.testModel.collection.documents[1].tokens= [u'a', u'corpus', u'and', u'a', u'test']

        self.targetModel = copy.deepcopy(self.testModel)

    def test_createDictionary(self):
        self.testModel.createDictionary()
        self.targetModel.dictionary = {7:u'test', 11:u'if', 3:u'this', 1:u'set', 4:u'is', 6:u'converted', 5:u'to', 0:u'a', 2:u'dictionary', 8:u'representation', 9:u'corpus', 10:u'with'}
        self.assertEqual(self.testModel.dictionary.items(), self.targetModel.dictionary.items())

    def test_createCorpus(self):
        self.testModel.createDictionary()
        self.testModel.createCorpus()
        self.targetModel.corpus = [[(7,1), (8,1), (9,1)], [(0,2),(7,1),(9,1)]]

        self.assertEqual(self.testModel.corpus, self.targetModel.corpus)
        



if __name__ == '__main__':
    unittest.main()


