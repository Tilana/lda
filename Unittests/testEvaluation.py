import unittest
from lda import Evaluation

class testEvaluation(unittest.TestCase):

    def setUp(self):
        target =     [0,1,1,0,1,0]
        prediction = [0,1,0,0,1,1]
        self.evaluation = Evaluation(target, prediction)

    def test_createTags(self):
        self.evaluation.createTags()
        result = ['TN','TP','FN','TN','TP','FP']
        self.assertEqual(self.evaluation.tags, result)

    def test_getTag(self):
        self.evaluation.tags = ['TN', 'TP', 'FN', 'TN', 'TP']
        
        self.evaluation.getTag('TP')
        self.assertEqual(self.evaluation.TP, [1,4])

        self.evaluation.getTag('FP')
        self.assertEqual(self.evaluation.FP, [])



if __name__ == '__main__':
    unittest.main()
