import namedEntityRecognition as ner
import utils

# stores named entities of a document sorted by its different tags, like location, person and organization
class entities:
    
    def __init__(self, document=None, frequency=1):
        if document is None:
            self.LOCATION = []
            self.PERSON =  []
            self.ORGANIZATION = []
        else:
            entityTuples = ner.getNamedEntities(document)
            for entities in entityTuples:
                setattr(self, entities[0], set(entities[1]))
                if frequency is not None:
                    print 'Frequency == True'
                    entityFrequency = [(entity.lower(), document.lower().count(entity.lower())) for entity in entities[1]]
                    setattr(self, entities[0], entityFrequency)
                       

    def addEntities(self, tag, entityList):
        setattr(self, tag, entityList)

    def countOccurence(self, text, field=None):
        entityList = self.getEntities(field)
        text = text.lower()
        occurence = []
        for entity in entityList:
            entity = entity.lower()
            if text.count(entity)>0:
                occurence.append((entity, text.count(entity)))
        return occurence 

    def getEntities(self, field=None):
        if field is None:
            return utils.flattenList([list(self.LOCATION), list(self.ORGANIZATION), list(self.PERSON)])
        return getattr(self, field)

    def isEmpty(self):
        return self.LOCATION == [] and self.PERSON == [] and self.ORGANIZATION == []


