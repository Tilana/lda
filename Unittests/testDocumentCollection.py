import unittest
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath('documentCollection'))))
from documentCollection import documentCollection

class testDocumentCollection(unittest.TestCase):
   
    documentCollection.titles = ['doc1','doc2','doc3']
    documentCollection.docs = 
    
    def test(self):
        self.assertTrue(True)

    def test_getNamedEntities()
        

if __name__ == '__main__':
    unittest.main()

