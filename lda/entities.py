import namedEntityRecognition as ner
# stores named entities of a document sorted by its different tags, like location, person and organization
class entities:
    
    def __init__(self, document=None):
        entityTuples = ner.getNamedEntities(document)
        for entities in entityTuples:
            setattr(self, entities[0], set(entities[1]))
    
    def addEntities(self, tag, entityList):
        setattr(self, tag, entityList)


