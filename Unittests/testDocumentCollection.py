import unittest
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath('documentCollection'))))
from documentCollection import documentCollection

class testDocumentCollection(unittest.TestCase):
   
    collection = documentCollection(' ')
    collection.titles = ['doc1','doc2','doc3']
    collection.docs = ['Simulated document collection to recognize named entities','African Commission is a named entity','Also names like Peter, ']
    
    def test(self):
        self.assertTrue(True)

    def test_getNamedEntities()
        

if __name__ == '__main__':
    unittest.main()

