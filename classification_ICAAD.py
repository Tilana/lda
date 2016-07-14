from lda import ClassificationModel, Viewer, Info, Evaluation
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import logging

def classification_ICAAD():

    ##### PARAMETERS #####
    logging.basicConfig()
    evaluationFile = 'Documents/PACI.csv'
    dataFeatures = pd.read_csv(evaluationFile)
    dataFeatures = dataFeatures.rename(columns={'Unnamed: 0': 'id'})

    features = [feature for feature in dataFeatures.columns.tolist() if dataFeatures[feature].dtypes==bool]
    features = ['Domestic.Violence.Manual']

    info = Info()
    info.data = 'ICAAD'
    info.identifier = 'LDA_T60P10I70_tfidf_word2vec'
    
    #targetFeature = 'Sexual.Assault.Manual'
    topicList =  [('Topic%d' % topicNr) for topicNr in range(0,54)]
    similarDocList = [('similarDocs%d' % docNr) for docNr in range(1,6)]

    ### LOAD DATA ###
    path = 'html/%s/DocumentFeatures.csv' % (info.data + '_' + info.identifier)
    model = ClassificationModel(path)
    model.droplist = []
    model.keeplist = topicList + similarDocList
    
    for feature in features:
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


        model.numberTrainingDocs = len(model.data)/4
        model.splitDataset(model.numberTrainingDocs)
        print model.trainData.columns

        ### CLASSIFICATION ###
        classifier = DecisionTreeClassifier()
        #classifier = RandomForestClassifier()
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

