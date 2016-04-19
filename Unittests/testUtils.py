import unittest
import os, sys
from lda import utils

class testUtils(unittest.TestCase):
    
    def setUp(self):
        pass

    def test_listDifference(self):
        l = [3,6,9,10,11,22,23,30]
        self.assertEqual(utils.listDifference(l), [(3,3),(3,6),(1,9),(1,10),(11,11),(1, 22),(7,23)])

    def test_sortTupleList(self):
        l = [('low frequency', 2), ('high frequency', 10), ('negative frequency', -1)]
        target = [('high frequency', 10), ('low frequency', 2), ('negative frequency', -1)]
        self.assertEqual(target, utils.sortTupleList(l))

    def test_sortSublist(self):
        l1 = [[(7,2), (1,4), (12,1), (11,1)], [(0,1), (6,2), (5,3)], [(1,3), (2,2), (4,2)]]
        targetList = [[(1,4), (7,2), (11,1), (12,1)], [(0,1), (5,3), (6,2)], [(1,3), (2,2), (4,2)]]

        self.assertEqual(targetList, utils.sortSublist(l1))

 

    def test_joinSublists(self):
        l1 = [[(0,2), (1,4)],[(0,1),(1,5),(5,3)], [(2,2), (1,3)]]
        l2 = [[(11,1), (2,1)], [(4,2)], []]

        targetList = [[(0,2), (1,4), (2,1), (11,1)], [(0,1), (1,5), (4,2), (5,3)], [(1,3), (2,2)]]

        self.assertEqual(utils.joinSublists(l1,l2), targetList)
    
    
    def test_contains(self):
        self.assertTrue(utils.containsAny('w@rd','.@/!$'))
        self.assertFalse(utils.containsAny('word', ['.','p', '-']))
        self.assertTrue(utils.containsAny('(3)', '(.\\'))


    def test_absoluteList(self):
        l = [(54.09, 2), (-200, 11), (-2, 3), (23.29, 19)]
        targetList = [(54.09, 2), (200, 11), (2, 3), (23.29, 19)]

        self.assertEqual(targetList, utils.absoluteTupleList(l))


if __name__ =='__main__':
    unittest.main()
