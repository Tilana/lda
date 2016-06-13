from lda import ClassificationModel, Viewer, Info
from sklearn.tree import DecisionTreeClassifier

def classification():

    ##### PARAMETERS #####
    path = 'Documents/PACI.csv'
    info = Info()
    info.data = 'ICAAD'
    info.identifier = 'classification'

    #targetFeature = 'Domestic.Violence.Manual'
    targetFeature = 'Sexual.Assault'

    droplist = ['Sexual.Assault.Manual', 'Unnamed: 0']
#    droplist = ['Strength.of.SA', 'Sexual.Assault.Manual', 'Unnamed: 0']
#    droplist = ['Unnamed: 0']

    ### PREPROCESSING ###
    model = ClassificationModel(path, targetFeature, droplist)
    
    # TO-DO: Consider symmetrie in age values
    model.createNumericFeature('Age')
    
    model.createNumericFeature('Court')
    model.data.loc[model.data['Reconciliation_freq']=='False', 'Reconciliation_freq' ] = '0'
    model.toNumeric('Reconciliation_freq')

    model.cleanDataset()

    ### SELECT TEST AND TRAINING DATA ###
    model.balanceDataset()
    model.createTarget()
    model.dropFeatures()

    model.splitDataset(len(model.data)/2)

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
    classification()

