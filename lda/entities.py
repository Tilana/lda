import namedEntityRecognition as ner
import utils

# stores named entities of a document sorted by its different tags, like location, person and organization
class entities:
    
    def __init__(self, document=None):
        if document is None:
            self.LOCATION = []
            self.PERSON =  []
            self.ORGANIZATION = []
        else:
            entityTuples = ner.getNamedEntities(document)
            for entities in entityTuples:
                setattr(self, entities[0], set(entities[1]))
    
    def addEntities(self, tag, entityList):
        setattr(self, tag, entityList)

    def getEntities(self):
        return utils.flattenList([list(self.LOCATION), list(self.ORGANIZATION), list(self.PERSON)])


