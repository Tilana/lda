import unittest
import copy
from lda import Controller 
from lda import Document
from lda import Dictionary
from lda import Entities
from gensim import corpora

class testController(unittest.TestCase):

    def setUp(self):
        self.testModel = Controller()
        self.testModel.dictionary.words = set(['test', 'if', 'this', 'test', 'set', 'is', 'converted', 'to', 'a', 'dictionary', 'representation', 'with', 'a', 'corpus'])
        self.testModel.collection = [Document('doc1', 'test corpus representation'), Document('doc2', 'a corpus and a test')]
        self.testModel.collection[0].tokens= [u'test', u'corpus', u'representation']
        self.testModel.collection[1].tokens= [u'a', u'corpus', u'and', u'a', u'test']

        self.targetModel = copy.deepcopy(self.testModel)

    def test_createEntityCorpus(self):
        self.testModel.collection = [Document('doc1', 'London is the capital of the United Kingdom'), Document('doc2', 'The United Kingdom, the United Kingdom, and Donald Trump is the Mickey Mouse of the United States of America')]
        self.testModel.collection[0].entities = Entities()
        self.testModel.collection[0].entities.addEntities('LOCATION', [('london', 1), ('united kingdom', 1)])
        self.testModel.collection[1].entities = Entities()
        self.testModel.collection[1].entities.addEntities('LOCATION', [('united kingdom', 2), ('united states of america', 1)])
        self.testModel.collection[1].entities.addEntities('PERSON', [('donald trump', 1), ('mickey mouse', 1)])

        self.testModel.dictionary.ids = {0:'test', 1:'london', 2:'not in documents', 3:'united kingdom', 4:'united states of america', 5:'donald trump', 6:'mickey mouse'}
        
        self.testModel.createEntityCorpus()
        self.targetModel.entityCorpus = [[(1,1), (3,1)], [(3,2), (4,1), (5,1), (6,1)]]
        self.assertEqual(self.testModel.entityCorpus, self.targetModel.entityCorpus)

#        self.testModel.createEntityCorpus('LOCATION')
#        self.targetModel.entityCorpus = [[(1,1), (3,1)], [(3,2), (4,1)]]
#        self.assertEqual(self.testModel.entityCorpus, self.targetModel.entityCorpus)


    def test_createCorpus(self):

        self.testModel.dictionary.words = set(['test', 'if', 'this', 'test', 'set', 'is', 'converted', 'to', 'a', 'dictionary', 'representation', 'with', 'a', 'corpus'])
        self.testModel.dictionary.createDictionaryIds()
        self.testModel.createCorpus()
        self.targetModel.corpus = [[(7,1), (8,1), (9,1)], [(0,2),(7,1),(9,1)]]

        self.assertEqual(self.testModel.corpus, self.targetModel.corpus)
    
    def test_createDictionary(self):
        testModel = Controller()
        testModel.collection = [Document('doc1', 'Test -tokenization- and if common words are deleted.'), Document('doc2', 'stopwords like of, and, but?'), Document('doc3', 'special\ characters?\n, Article\n\n78(5), constitution references 103/93 and dates 23.01.1998 or 12th of March 2003')]
        testModel.createDictionary(lemmatize=False, wordList= None, stoplist=None, specialChars=None, removeShortWords=False, getOriginalWords=False)

        targetDictionary = Dictionary()
        targetDictionary.words = set(['test', '-tokenization-', 'and', 'if','common', 'words','are','deleted','.','stopwords','like','of',',','but','?','special\\','characters','article','78','(','5',')','constitution','references','103/93','dates','23.01.1998','or', '12th','march','2003'])
        targetDictionary.stopwords = set([])

        for attribute in targetDictionary.__dict__.keys():
            if attribute != 'ids':
                self.assertEqual(getattr(testModel.dictionary, attribute), getattr(targetDictionary, attribute))

#        self.assertEqual(testModel.dictionary.ids.items(), targetDictionary.ids.items())
    


if __name__ == '__main__':
    unittest.main()


