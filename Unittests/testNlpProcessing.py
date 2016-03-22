import unittest
from lda import nlp
from lda import documentCollection

class testNlpProcessing(unittest.TestCase):
    
    def setUp(self):
        self.documents = ['Ignore\n. Split!?',' Mr. Jone`s "words in quotes."','Don\'t split Article 7 and 108/82']
    
    def test(self):
        self.assertTrue(True)
    
    def test_tokenizeCollection(self):
        self.assertEqual(nlp.tokenizeCollection(self.documents), set(['ignore','.','split','!','?','mr.',"''",'and','do','n\'t','108/82','7','article', '``','jone`s','words','in','quotes']))


if __name__ == '__main__':
    unittest.main()
