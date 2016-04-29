import unittest
import pandas as pd
from lda import dataframeUtils as dfUtils

class testDataframeUtils(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            'row name': ['1st row', '2nd row', '3rd row'],
            'A': [1, 2, 3],
            'B': [4, 5, 6],
            'C': [True, True, False]},
            columns=['row name', 'A', 'B', 'C']) 


    def test_getRow(self):
        self.assertEqual(dfUtils.getRow(self.df, 'row name', '2nd row', ['A', 'B']), [2,5])
        self.assertEqual(dfUtils.getRow(self.df, 'row name', '2nd row', ['B']), [5])


    def test_filterData(self):
        target = self.df[0:2] 
        self.assertTrue(target.equals(dfUtils.filterData(self.df, 'C')))

    def test_getIndex(self):
        target = [0, 1, 2]
        self.assertEqual(dfUtils.getIndex(self.df), target)


if __name__ == '__main__':
    unittest.main()

