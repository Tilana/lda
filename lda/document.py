from entities import entities
import utils
import nltk

class document:
    
    def __init__(self, title=None, text=None):
        self.title = title
        self.text = text 
        self.entities = entities()
       
    def createEntities(self):
        self.entities = entities(self.text)

    def createWords(self):
        self.words = set(self._tokenizeDocument())
    
    def createTokens(self, stoplist=[]):
        self.tokens= self._tokenizeDocument()
        print self.tokens
        self.removeStopwords(stoplist)
        self.includeEntities()

    def hasWordsAttribute(self):
        return hasattr(self, 'words')

    def _tokenizeDocument(self):
        return [word.lower() for word in nltk.word_tokenize(self.text)]

    def removeStopwords(self, stoplist):
        self.tokens = [word for word in self.tokens if word not in stoplist]

    def includeEntities(self):
        entityList = self.entities.getEntities()
        print entityList
        for entity in entityList:
            ent = entity.lower().split()
            lengthEntity = len(ent)
            if lengthEntity>1:
                print ent
                wordInd = []
                for pos in range(lengthEntity):
                   indices = [index for index, word in enumerate(self.tokens) if word == ent[pos]]
                   wordInd = wordInd + indices
                distList = utils.listDifference(sorted(wordInd))
                print distList
                count = 1
                for elem in distList:
                    if elem[0]==1:
                        print "Distance 1"
                        count+=1
                        if count==lengthEntity:
                            print "Same entity length"
                            print ' '.join(self.tokens[elem[1]+2-lengthEntity:elem[1]+2])
                            self.tokens[elem[1]+1] = ' '.join(self.tokens[elem[1]+2-lengthEntity:elem[1]+2])
                            del self.tokens[elem[1]+2-count:elem[1]+1]
        print self.tokens

        



