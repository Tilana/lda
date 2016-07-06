from lda import ClassificationModel, Viewer, Info, Evaluation
from sklearn.tree import DecisionTreeClassifier
import pandas as pd

def classification_ICAAD():

    ##### PARAMETERS #####
    info = Info()
    info.data = 'ICAAD'
    info.identifier = 'LDA_T70P100I300_word2vec'
    
    targetFeature = 'Domestic.Violence.Manual'
    droplist = ['Unnamed: 0', 'File', 'DV', 'SA']

    ### LOAD DATA ###
    path = 'html/%s/DocumentFeatures.csv' % (info.data + '_' + info.identifier)
    model = ClassificationModel(path, targetFeature, droplist)

    evaluationFile = 'Documents/PACI.csv'
    dataFeatures = pd.read_csv(evaluationFile)
    dataFeatures = dataFeatures.rename(columns={'Unnamed: 0': 'id'})

    ### PREPROCESSING ###
    features = dataFeatures.columns.tolist()
    if targetFeature in features:
        column = dataFeatures[['id', targetFeature]]
        model.mergeDataset(column)

    model.dropNANRows()
    model.createNumericFeature('court')
    model.toBoolean(['SA', 'DV'])

    ### SELECT TEST AND TRAINING DATA ###
    model.factorFalseCases = 1 
    model.balanceDataset(model.factorFalseCases)
    model.createTarget()
    model.dropFeatures()

    model.numberTrainingDocs = len(model.data)/4
    model.splitDataset(model.numberTrainingDocs)

    ### CLASSIFICATION ###
    classifier = DecisionTreeClassifier()
    model.trainClassifier(classifier)
    model.predict(classifier)

    ### EVALUATION ###
    model.evaluate()
    model.confusionMatrix()
    model.featureImportance()
    model.getTaggedDocs()

    Viewer(info).classificationResults(model)

   
if __name__ == "__main__":
    classification_ICAAD()

