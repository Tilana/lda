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
    info.identifier = 'LDA_T55P12I100_tfidf_word2vec'
    
    #targetFeature = 'Sexual.Assault.Manual'
    droplist = ['File', 'DV', 'SA', 'id']

    for feature in features:
        targetFeature = feature
        print feature

        ### LOAD DATA ###
        path = 'html/%s/DocumentFeatures.csv' % (info.data + '_' + info.identifier)
        model = ClassificationModel(path, targetFeature, droplist)
        #model.data = model.data.set_index('Unnamed: 0')

        ### PREPROCESSING ###
        column = dataFeatures[['id', targetFeature]]
        model.mergeDataset(column)
        model.data = model.data.set_index('Unnamed: 0')
        model.orgData = model.data

        model.dropNANRows()
        model.createNumericFeature('court')

        ### SELECT TEST AND TRAINING DATA ###
        model.factorFalseCases = 1 
        model.balanceDataset(model.factorFalseCases)
        model.createTarget()
        model.dropFeatures()

        model.numberTrainingDocs = len(model.data)/3
        model.splitDataset(model.numberTrainingDocs)

        ### CLASSIFICATION ###
        classifier = DecisionTreeClassifier()
        model.trainClassifier(classifier)
        model.predict(classifier)

        ### EVALUATION ###
        model.evaluate()
        model.confusionMatrix()
        model.confusionMatrix = model.confusionMatrix.rename(index={0: 'Target True', 1: 'Target False'}, columns={0: 'Predicted True', 1: 'Predicted False'})
        model.featureImportance()
        model.getTaggedDocs()

        html = Viewer(info)
        html.classificationResults(model)

   
if __name__ == "__main__":
    classification_ICAAD()

