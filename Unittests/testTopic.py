import unittest
from lda import Topic

class testTopic(unittest.TestCase):

    def setUp(self):
        self.testTopic = Topic()
        self.targetTopic = Topic()

    def test_addTopic(self):
        self.testTopic.addTopic((0, [(u'Test', -0.31), (u'Words', 0.045), (u'in', -0.23), (u'Topic', -0.002)])) 
        
        self.targetTopic.number = 0
        self.targetTopic.wordDistribution = [(u'Test', -0.31), (u'Words', 0.045), (u'in', -0.23), (u'Topic', -0.002)] 

        self.assertTrue(self.targetTopic.__eq__(self.testTopic))




if __name__ == '__main__':
    unittest.main()
