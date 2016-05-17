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

    def test_labelTopic(self):
        categories = ['computer', 'food', 'books', 'fruit', 'politics']
        self.testTopic.wordDistribution = [(u'apple', 0.32), (u'pear', 0.22), (u'strawberry', -0.20), ('banana', 0.1), ('cherry', 0.11)]
        targetCategories1 = ['fruit', 'food', 'books', 'computer', 'politics']
        self.testTopic.labelTopic(categories)
        self.assertEqual(targetCategories1, self.testTopic.keywords)

        self.testTopic.wordDistribution = [(u'mouse', 0.32), (u'power', 0.22), (u'computation', -0.20), ('screen', 0.1)] 
        targetCategories2 = ['computer', 'fruit', 'food', 'books', 'politics']
        self.testTopic.labelTopic(categories)
        self.assertEqual(targetCategories2, self.testTopic.keywords)
        
        self.testTopic.wordDistribution = [(u'president', 0.32), (u'constitution', 0.22), (u'discussion', -0.20), ('election', 0.1)] 
        targetCategories3 = ['politics', 'computer', 'food', 'books', 'fruit'] 
        self.testTopic.labelTopic(categories)
        self.assertEqual(targetCategories3, self.testTopic.keywords)        


if __name__ == '__main__':
    unittest.main()
