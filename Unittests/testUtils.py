import unittest
import os, sys
from lda import utils

class testUtils(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_getListDifference(self):
        testList = [2,3,8,9,10,35,37,38,40]
        differences = [1,5,1,1,25,2,1,2]
        self.assertEqual(utils.getListDifference(testList), differences)

    def test_getConsecutiveIndices(self):
        diffList = [1,1,0,4,5,1,1,10,20,1]
        indList = [0,1,5,6,9]
        self.assertEqual(utils.getConsecutiveIndices(diffList), indList)


if __name__ =='__main__':
    unittest.main()
