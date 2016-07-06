from lda import ClassificationModel, Viewer, Info, Evaluation
from sklearn.tree import DecisionTreeClassifier
import pandas as pd

def classification_ICAAD():

    ##### PARAMETERS #####
    evaluationFile = 'Documents/PACI.csv'
    dataFeatures = pd.read_csv(evaluationFile)
    dataFeatures = dataFeatures.rename(columns={'Unnamed: 0': 'id'})

    features = [feature for feature in dataFeatures.columns.tolist() if dataFeatures[feature].dtypes==bool]

    info = Info()
    info.data = 'ICAAD'
    info.identifier = 'LDA_T15P30I500_word2vec'
    
    #targetFeature = 'Sexual.Assault.Manual'
    droplist = ['Unnamed: 0', 'File', 'DV', 'SA', 'id']

    for feature in features:
        targetFeature = feature
        print feature

        ### LOAD DATA ###
        path = 'html/%s/DocumentFeatures.csv' % (info.data + '_' + info.identifier)
        model = ClassificationModel(path, targetFeature, droplist)

        ### PREPROCESSING ###
        column = dataFeatures[['id', targetFeature]]
        model.mergeDataset(column)

        model.dropNANRows()
        model.createNumericFeature('court')

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

        html = Viewer(info)
        html.classificationResults(model)

   
if __name__ == "__main__":
    classification_ICAAD()

