class Info:

    def __init__(self):
        pass

    def setup(self):
        self.setIdentifier()
        self.setPath()
        self.setFileType()
        self.setCollectionName()
        self.setProcessedCollectionName()


    def setIdentifier(self):
        self.identifier = '%s_T%dP%dI%d' %(self.modelType, self.numberTopics, self.passes, self.iterations)
        if self.tfidf:
            self.identifier = self.identifier + '_tfidf'


    def setFileType(self):
        if self.data == 'ICAAD':
            self.fileType = 'folder'
        elif self.data == 'NIPS':
            self.fileType = 'csv'
        elif self.data == 'scifibooks':
            self.fileType == 'folder'
        else:
            print 'Data not found'


    def setPath(self):
        if self.data == 'ICAAD':
            self.path = 'Documents/ICAAD/txt'           
        elif self.data == 'NIPS':
            self.path = 'Documents/NIPS/Papers.csv'
        elif self.data == 'scifibooks':
            self.path == 'Documents/scifibookspdf'
        else:
            print 'Data not found'


    def setCollectionName(self):
        if self.includeEntities:
            self.collectionName = 'dataObjects/'+self.data+'_entities'
        else:
            self.collectionName = 'dataObjects/'+self.data+'_noEntities'
        if self.numberDoc:
            self.collectionName = self.collectionName + '_%d' % self.numberDoc


    def setProcessedCollectionName(self):
        self.processedCollectionName = self.collectionName + '_' + self.identifier

    def saveToFile(self):
        dictionary = self.__dict__
        with open('html/' + self.identifier + '/info.txt', 'wb') as f:
            f.write('INFO - %s \n \n' % self.identifier)
            for key in dictionary:
                f.write(key + '  -  ' + str(dictionary[key]) +'\n')
        f.close()

