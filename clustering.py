import pandas as pd
from sklearn.cluster import KMeans
from lda import Collection, Cluster, Info, Viewer

def clustering():

    info = Info()
    info.data = 'ICAAD'
    info.identifier = 'LDA_T25P170I1400_word2vec_noNames'

    collectionName = 'processedDocuments/ICAAD_noEntities_word2vec_noNames'
    collection = Collection()
    collection.loadPreprocessedCollection(collectionName)

    identifier = 'ICAAD_LDA_T25P170I1400_word2vec'
    path = 'html/%s/DocumentFeatures.csv' % identifier
    data = pd.read_csv(path)
    data = data.drop(['File', 'id', 'Unnamed: 0'], 1)

    data = data.dropna()

    print 'Clustering'
    numCluster = 15
    km = KMeans(n_clusters = numCluster)

    km.fit(data)
    clusters = km.labels_.tolist()

    data['clusters'] = clusters
    html = Viewer(info)

    for clusterNo in range(0, numCluster):
        cluster = Cluster(clusterNo)
        cluster.features = data[data['clusters']==clusterNo]
        indices = cluster.features.index.tolist()
        cluster.documents = [(collection.documents[ind], ind) for ind in indices]
        cluster.createBinaryFeature('SA')
        cluster.createBinaryFeature('DV')

        html.printCluster(cluster)



if __name__ == "__main__":
    clustering()

