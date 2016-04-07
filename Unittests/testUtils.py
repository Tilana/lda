import unittest
import os, sys
from lda import utils

class testUtils(unittest.TestCase):
    
    def setUp(self):
        pass

    def test_listDifference(self):
        l = [3,6,9,10,11,22,23,30]
        self.assertEqual(utils.listDifference(l), [(3,3),(3,6),(1,9),(1,10),(11,11),(1, 22),(7,23)])
    
    
    def test_contains(self):
        self.assertTrue(utils.containsAny('w@rd','.@/!$'))
        self.assertFalse(utils.containsAny('word', ['.','p', '-']))
        self.assertTrue(utils.containsAny('(3)', '(.\\'))
if __name__ =='__main__':
    unittest.main()
