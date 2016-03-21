import unittest
import os,sys

sys.path.append(os.path.dirname(os.path.abspath('LDA')))
import nlpProcessing as nlp
from documentCollection import documentCollection

class testNlpProcessing(unittest.TestCase):
    
    def setUp(self):
        self.documents = ['Ignore\n. Split!?',' Mr. Jone`s "words in quotes."','Lower Case']
    
    def test(self):
        self.assertTrue(True)
    
    def test_tokenizeCollection(self):
        self.assertEqual(nlp.tokenizeCollection(self.documents), set(['ignore','.','split','!','?','mr.',"''", '``','jone`s','words','in','quotes','lower','case']))


if __name__ == '__main__':
    unittest.main()
