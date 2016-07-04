from lda import ClassificationModel, Viewer, Info
from sklearn.tree import DecisionTreeClassifier

def classification_ICAAD():

    ##### PARAMETERS #####
    info = Info()
    info.data = 'ICAAD'
    info.identifier = 'LDA_T21P5I300_word2vec'
    path = 'html/%s/DocumentFeatures.csv' % (info.data + '_' + info.identifier)

    targetFeature = 'DV'
    droplist = ['Unnamed: 0', 'File', 'DV']

    ### PREPROCESSING ###
    model = ClassificationModel(path, targetFeature, droplist)
    model.dropNANRows()
    
    model.createNumericFeature('court')
    model.toBoolean('SA')
    model.toBoolean('DV')


    ### SELECT TEST AND TRAINING DATA ###
    model.balanceDataset(2)
    model.createTarget()
    model.dropFeatures()

    model.splitDataset(len(model.data)/3)

    ### CLASSIFICATION ###
    classifier = DecisionTreeClassifier()
    model.trainClassifier(classifier)
    model.predict(classifier)

    ### EVALUATION ###
    model.evaluate()
    model.confusionMatrix()
    model.featureImportance()

    Viewer(info).classificationResults(model)

   
if __name__ == "__main__":
    classification_ICAAD()

