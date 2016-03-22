from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.chunk import conlltags2tree
class namedEntityRecognition:
    
    def __init__(self, text):
        self.nerTagger = StanfordNERTagger('/home/natalie/Documents/Huridocs/LDA/stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz','/home/natalie/Documents/Huridocs/LDA/stanford-ner-2014-06-16/stanford-ner.jar', encoding='utf-8')
        self.text = word_tokenize(text)
    
    def tagNamedEntities(self):
        self.taggedNameEntities = self.nerTagger.tag(self.text)

    def getTagIndices(self, name):
        return [(ind, item) for ind, item in enumerate(ner.taggedNameEntities) if item[1]==name]

    def combineConsecutiveTags(self, tags):
        print "Test"
    
    def bioTagger(self):
        bioTagged = []
        prevTag = "O"
        for token, tag in self.taggedNameEntities:
            if tag == "O":
                bioTagged.append((token, tag))
                prevTag = tag
                continue
            if tag != "O" and prevTag =="O":
                bioTagged.append((token, "B-"+tag))
                prevTag = tag
            elif prevTag != "O" and prevTag == tag:
                bioTagged.append((token, "I-"+tag))
                prevTag = tag
            elif prevTag != "O" and prevTag != tag:
                bioTagged.append((token, "B-"+tag))
                prevTag = tag
        return bioTagged
    
    def bio2Tree(self, bioTags):
        tokens, tags = zip(*bioTags)
        posTags = [pos for token, pos in pos_tag(tokens)]
        allTags = [(token, pos, entity) for token, pos, entity in zip(tokens, posTags, tags)]
        entityTree = conlltags2tree(allTags)
        return entityTree



