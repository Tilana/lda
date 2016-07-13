from lda import ClassificationModel, Viewer, Info, Evaluation
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf

evaluationFile = 'Documents/PACI.csv'
dataFeatures = pd.read_csv(evaluationFile)
dataFeatures = dataFeatures.rename(columns={'Unnamed: 0': 'id'})

targetFeature = 'Sexual.Assault.Manual'
info = Info()
info.data = 'ICAAD'
info.identifier = 'LDA_T60P10I70_tfidf_word2vec'

#targetFeature = 'Sexual.Assault.Manual'
#topicList =  [('Topic%d' % topicNr) for topicNr in range(0,54)]
#similarDocList = [('similarDocs%d' % docNr) for docNr in range(1,6)]
#keep = topicList + ['Unnamed: 0'] + similarDocList
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

model.numberTrainingDocs = len(model.data)/2
model.splitDataset(model.numberTrainingDocs)

model.trainTarget = pd.get_dummies(model.trainTarget)
model.testTarget = pd.get_dummies(model.testTarget)

length = len(model.trainData.columns)
classNumber = 2
# Regression
x = tf.placeholder(tf.float32, [None, length])
W = tf.Variable(tf.zeros([length, classNumber]))
b = tf.Variable(tf.zeros([classNumber]))

y = tf.nn.softmax(tf.matmul(x, W) + b)

# cross-entropy
y_ = tf.placeholder(tf.float32, [None, classNumber])
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))

# backpropagation to reduce cost
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)


# Init session and Train
init = tf.initialize_all_variables()

sess = tf.Session()
sess.run(init)

for i in range(1000):
    sess.run(train_step, feed_dict = {x: model.trainData, y_: model.trainTarget})

# Evaluation
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

print(sess.run(accuracy, feed_dict = {x: model.testData, y_: model.testTarget}))


