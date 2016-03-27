import unittest
import copy
from lda import TopicModel

class testTopicModel(unittest.TestCase):

    def setUp(self):
        self.testModel = TopicModel()
        self.testModel.collection.dictionary.words = set(['test', 'if', 'this', 'test', 'set', 'is', 'converted', 'to', 'a', 'dictionary'])

        self.targetModel = copy.deepcopy(self.testModel)

    def test_createDictionary(self):
        self.testModel.createDictionary()
        self.targetModel.dictionary = {1:u'test', 2:u'if', 3:u'this', 4:u'set', 5:u'is', 6:u'converted', 7:u'to', 8:u'a', 0:u'dictionary'}
        self.assertEqual(self.testModel.dictionary.keys(), self.targetModel.dictionary.keys())
        self.assertEqual(set(self.testModel.dictionary.values()), set(self.targetModel.dictionary.values()))


if __name__ == '__main__':
    unittest.main()


