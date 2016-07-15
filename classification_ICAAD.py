from lda import ClassificationModel, Viewer, Info, Evaluation
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import logging

def classification_ICAAD():

    ##### PARAMETERS #####
    pd.set_option('chained_assignment', None)
    logging.basicConfig()
    evaluationFile = 'Documents/PACI.csv'
    dataFeatures = pd.read_csv(evaluationFile)
    dataFeatures = dataFeatures.rename(columns={'Unnamed: 0': 'id'})

    features = [feature for feature in dataFeatures.columns.tolist() if dataFeatures[feature].dtypes==bool]
    features = ['Domestic.Violence.Manual']

    info = Info()
    info.data = 'ICAAD'
    info.topicNr = 60
    info.identifier = 'LDA_T%dP10I70_tfidf_word2vec' % info.topicNr
    info.classifierType = 'NeuralNet'
    
    topicList =  [('Topic%d' % topicNr) for topicNr in range(0,info.topicNr)]
    similarDocList = [('similarDocs%d' % docNr) for docNr in range(1,6)]

    ### LOAD DATA ###
    for feature in features:
        
        path = 'html/%s/DocumentFeatures.csv' % (info.data + '_' + info.identifier)
        model = ClassificationModel(path)
        model.droplist = []
        model.keeplist = topicList

        model.targetFeature = feature

        ### PREPROCESSING ###
        column = dataFeatures[['id', model.targetFeature]]
        model.mergeDataset(column)
        model.data = model.data.set_index('Unnamed: 0')
        model.orgData = model.data

        model.dropNANRows()
        model.createNumericFeature('court')

        ### SELECT TEST AND TRAINING DATA ###
        model.factorFalseCases = 2 
        model.balanceDataset(model.factorFalseCases)
        model.createTarget()
        model.dropFeatures()


        model.numberTrainingDocs = len(model.data)/3
        model.splitDataset(model.numberTrainingDocs)

        ### CLASSIFICATION ###
        model.buildClassifier(info.classifierType)
        model.trainClassifier()
        model.predict()

        ### EVALUATION ###
        model.evaluate()
        model.confusionMatrix()
        
        if not info.classifierType=='NeuralNet':
            model.computeFeatureImportance()
        model.getTaggedDocs()

        html = Viewer(info)
        html.classificationResults(model)

   
if __name__ == "__main__":
    classification_ICAAD()

