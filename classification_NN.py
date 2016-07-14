from lda import ClassificationModel, Viewer, Info, Evaluation
import pandas as pd
pd.set_option('chained_assignment', None)
import tensorflow as tf

evaluationFile = 'Documents/PACI.csv'
dataFeatures = pd.read_csv(evaluationFile)
dataFeatures = dataFeatures.rename(columns={'Unnamed: 0': 'id'})

targetFeature = 'Sexual.Assault.Manual'
targetFeature = 'Domestic.Violence.Manual'
info = Info()
info.data = 'ICAAD'
info.identifier = 'LDA_T60P10I70_tfidf_word2vec'

topicList =  [('Topic%d' % topicNr) for topicNr in range(0,54)]
similarDocList = [('similarDocs%d' % docNr) for docNr in range(1,6)]
#keep = ['Unnamed: 0'] + topicList 
#keep = ['domestic', 'husband', 'wife', 'violence', 'rape', 'child', 'Unnamed: 0']

droplist = ['File', 'DV', 'SA', 'id'] 

path = 'html/%s/DocumentFeatures.csv' % (info.data + '_' + info.identifier)
model = ClassificationModel(path, targetFeature, droplist)
#model.data = model.data.set_index('Unnamed: 0')
#model.droplist = list(set(model.data.columns.tolist())-set(keep))

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

model.trainTarget = model.oneHotEncoding(model.trainTarget)
model.testTarget = model.oneHotEncoding(model.testTarget)

length = len(model.trainData.columns)
print length
classNumber = 2

sess = tf.InteractiveSession()

# Setting up variables
x = tf.placeholder(tf.float32, [None, length])
y_ = tf.placeholder(tf.float32, [None, classNumber])

W = tf.Variable(tf.zeros([length, classNumber]))
b = tf.Variable(tf.zeros([classNumber]))

sess.run(tf.initialize_all_variables())

# Regression
y = tf.nn.softmax(tf.matmul(x, W) + b)

# cross-entropy - cost function
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))

# built in optimization algorithms
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)


# Init session and Train
#init = tf.initialize_all_variables()
#
#sess = tf.Session()
#sess.run(init)

for i in range(1000):
    sess.run(train_step, feed_dict = {x: model.trainData, y_: model.trainTarget})

# Evaluation
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

print(sess.run(accuracy, feed_dict = {x: model.testData, y_: model.testTarget}))


