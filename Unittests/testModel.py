import unittest
from lda import Model
from lda import Document
from lda import Topic

class testModel(unittest.TestCase):

    def test_tupleToTopicList(self):
        model = Model('LDA', 3)
        wordDistribution1 = [(u'Test', 0.45), (u'Topic', 0.003), (u'List', -0.01)]
        wordDistribution2 = [(u'List', 0.0021), (u'2', -0.001)]
        topicList = [(0, wordDistribution1), (1, wordDistribution2)]

        topic1 = Topic()
        topic1.number = 0
        topic1.wordDistribution = wordDistribution1

        topic2 = Topic()
        topic2.number = 1
        topic2.wordDistribution = wordDistribution2
        
        testList = model._tupleToTopicList(topicList)
        targetList = [topic1, topic2]
        for ind,topics in enumerate(targetList):
            self.assertEqual(targetList[ind].number, testList[ind].number)
            self.assertEqual(targetList[ind].wordDistribution, testList[ind].wordDistribution)

#    def test_getTopicRelatedDocuments(self):
#        targetList0 = [(0.23, 0), (0, 0.77, 2)]
#
#
#    def test_getTopicCoverageInCollection(self):
#        model = Model('LDA', 3)
#        collection = [document(), document(), document()]
#        collection[0].LDACoverage = [(0, 0.23), (1, 0.77)]
#        collection[1].LDACoverage = [(1, 0.74), (2, 0.21)]
#        collection[2].LDACoverage = [(1, 0.83), (2, 0.42)]
#
#        targetList = [[(0, 0.23), (1, 0.77)], [(1, 0.74), (2, 0.21)], [(1, 0.83), (2, 0.42)]]
#
#        self.assertEqual(targetList, model.getTopicCoverageInCollection(collection))
#
    
#    def test_getTopicRelatedDocuments(self):
#
#        corpus = [[(0,1), (1,2), (2,1)]
#                [(0,1), (3,1), (4,2), (5,1)]
#                [(1,2), (2,1), (4,1), (6,2), (7,1)]]
#        targetModel = Model('LSI', 3)
#        testModel = Model('LDA', 3)
#
#        targetModel.topics = [Topic(), Topic(), Topic()]
#        testModel.topics = [Topic(), Topic(), Topic()]
#
#        collection = [document(), document(), document()]
#        collection[0].LDACoverage = [(0, 0.23), (1, 0.77)]
#        collection[1].LDACoverage = [(1, 0.74), (2, 0.21)]
#        collection[2].LDACoverage = [(1, 0.83), (2, 0.42)]
#
#        testModel.getTopicRelatedDocuments(collection)
#        targetModel.topics[0].relatedDocuments = [(0.23, 0)]
#        targetModel.topics[1].relatedDocuments = [(0.83, 2), (0.77, 0), (0.74, 1)]
#        targetModel.topics[2].relatedDocuments = [(0.42, 2), (0.21, 1)]
#        for ind, topic in enumerate(targetModel.topics):
#            self.assertEqual(targetModel.topics[ind].relatedDocuments, testModel.topics[ind].relatedDocuments)
#
       
    def test_zipTopicCoverageList(self):

        model = Model('LDA', 3)
        collection = [[(0,0.23), (1,0.942), (2,0.94)], [(1, 0.42), (3,0.21)], [(0, 0.77), (2, 0.22), (2, 0.47)]]
        targetList0 = [(0.23, 0), (0.77, 2)]
        targetList1 = [(0.942, 0), (0.42, 1)]
        targetList2 = [(0.94, 0), (0.22, 2), (0.47, 2)]

        self.assertEqual(model.zipTopicCoverageList(collection, 0), targetList0)
        self.assertEqual(model.zipTopicCoverageList(collection, 1), targetList1)
        self.assertEqual(model.zipTopicCoverageList(collection, 2), targetList2)



if __name__ == '__main__':
    unittest.main()
