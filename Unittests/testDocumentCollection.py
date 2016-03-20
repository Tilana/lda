import unittest
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath('documentCollection'))))
from documentCollection import documentCollection

class testDocumentCollection(unittest.TestCase):
   
    collection = documentCollection(' ')
    collection.titles = ['doc1','doc2','doc3']
    collection.documents = ['document collection to test named entity recognition.',' African Commission is a named entity, also countries like Senegal and Lybia and names like Peter and Anna.','Also organizations like the United Nations or UNICEF should be recognized.']
    
    def test(self):
        self.assertTrue(True)

    def test_getNamedEntities(self):
        collection.getNamedEntities()
        testEntities = [set([]), set(['African Commission', 'Senegal', 'Lybia', 'Peter', 'Anna']), set(['United Nations', 'UNICEF'])]
        self.assertEqual(testEntities, collection.namedEntities)

if __name__ == '__main__':
    unittest.main()

