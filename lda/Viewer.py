from __future__ import division
import webbrowser
import os, sys


class Viewer:

    def __init__(self, info):
        self.path = 'html/'+ info.data +'_' + info.identifier
        self.createFolder(self.path)
        self.createFolder(self.path + '/Documents')
        self.createFolder(self.path + '/Topics')
        self.createFolder(self.path + '/Images')
        self.createFolder(self.path + '/Cluster')
        

    def createFolder(self, path):
        try:
            os.makedirs(path)
        except OSError:
            if not os.path.isdir(path):
                raise

    def writeHead(self, f, title):
        f.write("""<head><h1>%s</h1></head>""" % title)
        
    
    def listToHtmlTable(self, f, title, unicodeList):
        f.write("""<h4>%s</h4><table>""" % title.encode('utf8'))
        for items in unicodeList:
            f.write("""<tr><td>%s</td></tr>""" % items.encode('utf8'))
        f.write("""</table>""")
        
    
    def printTupleList(self, f, title, tupleList, format='int', colName1='', colName2=''):
        f.write("""<h4>%s</h4><table>""" % title.encode('utf8'))
        f.write("""<col style="width:40%"> <col style="width:50%">""")
        f.write("""<tr><td>%s</td> <td> %s </td></tr>""" % (colName1.encode('utf8'), colName2.encode('utf8')))

        for items in tupleList:
            if format=='int':
                f.write("""<tr><td>%s </td> <td> %d </td></tr>""" % (items[0].encode('utf8'), items[1]))
            else:
                f.write("""<tr><td>%s </td> <td> %.4f </td></tr>""" % (items[0].encode('utf8'), items[1]))

        f.write("""</table>""")


    def printColumn(self, f, title, l):
        f.write("""<div>""")
        self.listToHtmlTable(f, title + '- %d' % len(l), l)
        f.write("""</div>""")
    
    def printLinkedDocuments(self, f, title, documentTuples, folder=0):
        f.write("""<div>""")                                   
        f.write("""<h4>%s</h4><table>""" % title.encode('utf8'))
        for doc in documentTuples:
            f.write("""<tr><td><a href='%sDocuments/doc%02d.html'> %s </a></td></tr>""" % (folder*'../', doc[1], doc[0])) 
        f.write("""</table>""")
        f.write("""</div>""")

    def printClusterDocuments(self, f, title, documentTuples):
        f.write("""<div>""")                                   
        f.write("""<h4>%s</h4><table>""" % title.encode('utf8'))
        for doc in documentTuples:
            f.write("""<tr><td><a href='../Documents/doc%02d.html'> %s </a></td></tr>""" % (doc[1], doc[0].title)) 
        f.write("""</table>""")
        f.write("""</div>""")

    def printConfusionMatrix(self, f, matrix):
        f.write("""<h4> Confusion Matrix </h4><table>""" )
        f.write("""<tr> <td>. </td> <td> Predicted  </td> <td> Label </td></tr>""")
        f.write("""<tr> <td>True </td><td> %d </td> <td> %d </td> </tr>""" % (matrix[0][0], matrix[0][1]))
        f.write("""<tr> <td> Label </td> <td> %d </td><td> %d </td> </tr>""" % (matrix[1][0], matrix[1][1]))
        f.write("""</table>""")

    def printColoredList(self, f, title, l):
        f.write("""<h3>%s</h3><table>""" % title.encode('utf8'))
        f.write("""<col style="width:40%"> <col style="width:50%">""")
        for item in l:
            if item[1]==0:
                f.write("""<tr><td> <font color="red"> %s </font></td></tr>""" % (item[0].encode('utf8')))
            if item[1]==1:
                f.write("""<tr><td> <font color="green"> %s </font> </td></tr>""" % (item[0].encode('utf8')))

        f.write("""</table>""")

    def wordFrequency(self, dictionary, start=1, end=9):
        name = self.path + '/wordDocFrequency%d%d.html' % (start, end)
        f = open(name, 'w')
        f.write("""<html><head><h1> Frequency of words in documents</h1><style type="text/css"> body>div {width: 10%; float: left; border: 1px solid} </style></head>""") 
        f.write("""<body>""")
        for frequency in range(start,end):
            words = dictionary.inverseDFS.get(frequency, [])
            if words:
                 f.write("""<div>""")
                 self.listToHtmlTable(f, ('Frequency=%d Number of Words: %d' % (frequency, len(words))), words)
                 f.write("""</div>""")
        f.write("""</body></html>""")
        f.close()
        webbrowser.open_new_tab(name)


    def htmlDictionary(self, dictionary):
        name = self.path + '/dictionaryCollection.html'
        f = open(name, 'w')
        f.write("""<html><head><h1>Dictionary of Document Collection</h1><style type="text/css"> body>div {width: 23%; float: left; border: 1px solid} </style></head>""") 

        f.write("""<body>""")
        self.printColumn(f, 'Words in Dictionary ', dictionary.ids.values())
        self.printColumn(f, 'Removed Special Characters ', dictionary.specialCharacters)
        self.printColumn(f, 'Stopwords ', dictionary.stopwords)
        f.write("""</body></html>""")
        f.close()
        webbrowser.open_new_tab(self.path + '/dictionaryCollection.html')

    def documentOverview(self, collection):
        name = self.path + '/documents.html'
        f = open(name, 'w')
        f.write("<html>")
        self.writeHead(f, 'Document Overview')
        f.write("<body>")
        f.write("""<img src="Images/maxTopicCoverage.jpg" alt="wrong path" height="280">""")
        sortedCollection = sorted(collection, key=lambda document: document.LDACoverage[0][1], reverse=True)
        indices = [ind[0] for ind in sorted(enumerate(collection), key=lambda document: document[1].LDACoverage[0][1], reverse=True)]
        f.write("""<h4> LDA Topic coverage:</h4><table>""")
        f.write("""<col style="width:35%"> <col style="width:15%"> <col style = "width:20%"> """)

        for ind, document in enumerate(sortedCollection):
            f.write("""<tr><td><a href='Documents/doc%02d.html'> %s </a></td> <td> %0.4f </td> <td> <a href='Topics/LDAtopic%d.html' > Topic %d </a> </td></tr>""" % (indices[ind], document.title, document.LDACoverage[0][1], document.LDACoverage[0][0], document.LDACoverage[0][0]))
        f.write("</table>")
        f.write("</body></html>")
        f.close()
        webbrowser.open_new_tab(name)

    
    def printTopics(self, model):
        filename = self.path + '/%stopics.html' % model.name
        f = open(filename, 'w')
        f.write("<html>")
        self.writeHead(f, '%s Topics' % model.name)
        f.write("<body><p>Topics and related words - %s Model</p><table>" % model.name )
        f.write("""<col style="width:7%"> <col style="width: 15%"> <col style="width:7%"> <col style="width: 7%"> <col style="width:80%">""")

        for topic in model.topics:
            topic.score = sum(topic.relevanceScores)
            if max(topic.relevanceScores)<0.2:
                f.write("<tr><td><a href='Topics/%stopic%d.html'>  <font color='red'> Topic %d </font> </a></td><td>%s </td><td>%.4f</td><td>%.4f</td><td>%s</td></tr>" % (model.name, topic.number, topic.number, topic.keywords[0:2], topic.score, topic.medianSimilarity, str(topic.wordDistribution[0:10])[1:-1]))
            elif max(topic.relevanceScores)>0.8:
                f.write("<tr><td><a href='Topics/%stopic%d.html'>  <font color='green'> Topic %d </font> </a></td><td>%s </td><td>%.4f</td><td>%.4f</td><td>%s</td></tr>" % (model.name, topic.number, topic.number, topic.keywords[0:2], topic.score, topic.medianSimilarity, str(topic.wordDistribution[0:10])[1:-1]))
            else:
                f.write("<tr><td><a href='Topics/%stopic%d.html'> Topic %d </a></td><td>%s </td><td>%.4f</td><td>%.4f</td><td>%s</td></tr>" % (model.name, topic.number, topic.number, topic.keywords[0:2], topic.score, topic.medianSimilarity, str(topic.wordDistribution[0:10])[1:-1]))
        f.write("</table>")
        
        f.write("Mean Similarity Score: %.4f" % model.meanScore)
        f.write("<p> <h4> Possible Categories: </h4> %s</p>" % model.categories)
        f.write("</body></html>")
        f.close()
        webbrowser.open_new_tab(filename)
    
    
    def printDocuments(self, collection, lda, topics=1, openHtml=False):
        for doc in collection:
            pagename = self.path + '/Documents/doc%02d.html' % doc.nr 

            attributes = doc.__dict__.keys()
            f = open(pagename, 'w')
            f.write("<html>")
            self.writeHead(f, "Document %02d - %s" % (doc.nr, doc.title))

            f.write("""<body><div style="width:100%;"><div style="float:right; width:45%;">""")

            f.write("<h4> Properties: </h4>")
            if 'id' in attributes:
                f.write("ID:    %s <br>" % doc.id)
            if 'SA' in attributes:
                f.write("SA:    %s <br>" % doc.SA)
            if 'DV' in attributes:
                f.write("DV:    %s <br>" % doc.DV)
            if 'court' in attributes:
                f.write("Court: %s <br>" % doc.court)
            if 'year' in attributes:
                f.write("Year:  %s <br>" % doc.year)
            
            f.write("<h4> Topic Modeling Predictions: </h4>")
            if 'predSA' in attributes:
                f.write("predicted SA:")
                if doc.predSA == doc.SA:
                    f.write("""<font color="green"> %s </font> <br>""" % doc.predSA) 
                else:
                    f.write("""<font color="red"> %s </font> <br>""" % doc.predSA)
            if 'predDV' in attributes:
                f.write("predicted DV:")
                if doc.predDV == doc.DV:
                    f.write("""<font color="green"> %s </font> <br>""" % doc.predDV) 
                else:
                    f.write("""<font color="red"> %s </font> <br>""" % doc.predDV) 
            
            if 'LDACoverage' in attributes:
                f.write("""<h4> LDA Topic coverage:</h4><table>""")
                f.write("""<col style="width:20%"> <col style="width:50%"> <col style = "width:30%"> """)
                for coverage in doc.LDACoverage[0:5]:
                    topicNr = coverage[0]
                    f.write("""<tr><td><a href='../Topics/LDAtopic%d.html'>Topic %d</a</td> <td> Coverage %.2f</td></tr>""" % (topicNr, topicNr, coverage[1]))
                f.write("</table>")

            if 'LSICoverage' in attributes:
                f.write("""<h4> LSI Topic coverage:</h4><table>""")
                f.write("""<col style="width:20%"> <col style="width:50%"> <col style = "width:30%"> """)
                for coverage in doc.LSICoverage[0:5]:
                    topicNr = coverage[0]
                    f.write("""<tr><td><a href='../LSItopic%d.html'>Topic %d</a</td> <td> %s</td> <td> Coverage %.2f</td></tr>""" % (topicNr, topicNr, lda.topics[topicNr].keywords[0:2], coverage[1]))
                f.write("</table>")

            if 'targetCategories' in attributes:
                f.write("""<h4>Target Categories</h4><table>""")
                for items in list(zip(*doc.targetCategories)[0]):
                    f.write("""<tr><td>%s</td></tr>""" % items)
                f.write("""</table>""")

            if 'freqWords' in attributes:
                self.printTupleList(f, 'Relevant Words (TF-IDF)', doc.freqWords, 'float')

            if 'mostFrequentEntities' in attributes:
                self.printTupleList(f, 'Most frequent entities', doc.mostFrequentEntities)

            if 'LDASimilarity' in attributes:
                f.write("""<h4>Similar documents: \n</h4><table>""")
                f.write("""<col style="width:40%"> <col style="width:50%">""")
                for similarDoc in doc.LDASimilarity:
                    f.write("""<tr><td><a href='doc%02d.html'>Document %d</a></td>""" % (similarDoc[0], similarDoc[0]))
                    f.write("""<td> Similarity: %.4f</td></tr>""" % similarDoc[1])
                f.write("""</table>""")


            f.write("""<h4> Named Entities: \n</h4>""")
            for tag in doc.entities.__dict__.keys():
                wordList = getattr(doc.entities, tag)
                if wordList != []:
                    self.printTupleList(f, tag, wordList)
            f.write("""</div>""")
            f.write("""<div style="float:left; width:55%%;"><p>%s</p></div></div></body></html>""" % doc.text.encode('utf8'))
            f.close()
            if openHtml:
                webbrowser.open_new_tab(pagename)
               
    
    def printDocsRelatedTopics(self, model, collection, openHtml=False):
        for num in range(0, model.numberTopics): 
    	    pagename = self.path + '/Topics/%stopic%d.html' % (model.name, num)
    	    f = open(pagename, 'w')
    	    f.write("<html>")
            self.writeHead(f, '%s Document Relevance for Topic %d' %  (model.name, num))
            f.write("<body><h4>Topics and related words - %s Model</h4><table>" % model.name)
            f.write("""<col style="width:7%"> <col style="width:80%">""")
            topic = model.topics[num]
            f.write("<tr><td><a href='%stopic%d.html'>Topic %d</a></td><td>%s</td></tr>" % (model.name, topic.number, topic.number, str(topic.wordDistribution)[1:-1].encode('utf-8')))
            f.write("</table>")
            f.write(""" <h4> Relevance Histogram </h4> """)
            f.write("""<img src="../Images/documentRelevance_topic%d.jpg" alt="wrong path" height="280">""" % num)
            f.write("<h4>Related Documents</h4>")
            f.write("<table>") 
    	    f.write("""<col style="width:10%"> <col style="width:40%"> <col style="width:25%">""")
    	    for doc in model.topics[num].relatedDocuments[0:300]:
    	    	#f.write("<tr><td><a href='../Documents/doc%02d.html'>Document %d</a></td><td>%s</td><td>Relevance: %.2f</td></tr>" % (doc[1], doc[1], collection[doc[1]].title.encode('utf8'), doc[0]))
                f.write("<tr><td><a href='../Documents/doc%02d.html'>Document %d</a></td><td>%s</td><td>Relevance: %.2f</td></tr>" % (doc[1], doc[1], collection[doc[1]].title, doc[0]))
    
    	    f.write("</table></body></html>")
    	    f.close()
            if openHtml:
                webbrowser.open_new_tab(pagename)


    def classificationResults(self, model):
        self.createFolder(self.path + '/Classification')
        self.createFolder(self.path + '/Classification/%s' % model.classifierType)
        pagename = self.path + '/Classification/%s/%s.html' % (model.classifierType, model.targetFeature)
        f = open(pagename, 'w')
        title = '%s Classification - %s' % (model.classifierType, model.targetFeature)
        f.write("<html>")
        self.writeHead(f, title)
        f.write("""<body><div style="width:100%;">""")
        f.write(""" <p><b> Classifier: </b> %s </p> """ % model.classifierType)
        f.write(""" <p><b> Size of Training Data: </b> %s </p> """ % len(model.trainData))
        if model.binary:
            f.write("""<p> <b> Balance of Training Data: </b> True 1 : %d False """ % model.factorFalseCases)
        f.write(""" <p><b> Size of Test Data: </b> %s </p>""" % len(model.testData))
        #f.write(""" <p> <b> Features: </b> %s </p>""" % model.trainData.columns.tolist())
        #f.write(""" <p> <b> Ignored Features: </b> %s </p>""" % model.droplist)
        
        f.write(""" <h3> Evaluation: </h3>""")
        f.write("""<table> """)
        f.write("""<tr><td> Accuracy: </td><td> %.2f </td></tr>""" % model.evaluation.accuracy)
        f.write("""<tr><td> Precision: </td><td> %.2f </td></tr>""" % model.evaluation.precision)
        f.write("""<tr><td> Recall: </td><td> %.2f </td></tr>""" % model.evaluation.recall)
        f.write("""</table>""")

        f.write(""" <h3> Confusion Matrix: </h3>""")
        confusionMatrix = model.evaluation.confusionMatrix.to_html()
        f.write(confusionMatrix)

        if hasattr(model, 'featureImportance'):
            self.printTupleList(f, 'Feature Importance', model.featureImportance, format='float')

        f.write("""</table></div>""")
        
        if hasattr(model, 'TP_docs'):
            f.write("""<style type="text/css"> body>div {width: 23%; float: left; border: 1px solid} </style></head>""") 
            
            self.printLinkedDocuments(f, 'True Positives', model.TP_docs, 2) 
            self.printLinkedDocuments(f, 'False Positives', model.FP_docs, 2) 
            self.printLinkedDocuments(f, 'True Negatives', model.TN_docs, 2) 
            self.printLinkedDocuments(f, 'False Negatives', model.FN_docs, 2) 
        f.write("""</body></html>""")
        f.close()
        webbrowser.open_new_tab(pagename)


    def results(self, model, collection, info):
        pagename = self.path + '/TM_classification_%s.html' % model.feature
        topics = getattr(info, model.feature+'Topics')
        threshold = getattr(info, model.feature +'threshold')
        f = open(pagename, 'w')
        f.write("<html>")
        self.writeHead(f, '%s Classification results' % model.feature)
        f.write("""<body><div style="width:100%;">""")
        f.write(""" <p><b> Number of Documents: </b> %s </p> """ % len(model.prediction))
        f.write(""" <p><b> Selected Topics: </b> %s </p>""" % topics)
        f.write("""<p><b> Threshold: </b> %.2f </p>""" % threshold)
        f.write(""" <h3> Evaluation: </h3>""")
        f.write("""<table> """)
        f.write("""<tr><td> Accuracy: </td><td> %.2f </td></tr>""" % model.accuracy)
        f.write("""<tr><td> Precision: </td><td> %.2f </td></tr>""" % model.precision)
        f.write("""<tr><td> Recall: </td><td> %.2f </td></tr>""" % model.recall)
        f.write("""</table>""")
        
        f.write(""" <h3> Confusion Matrix: </h3>""")
        confusionMatrix = model.confusionMatrix.to_html()
        f.write(confusionMatrix)
        f.write("""</table></div>""")
        f.write("""<style type="text/css"> body>div {width: 23%; float: left; border: 1px solid} </style></head>""") 
        self.printLinkedDocuments(f, 'True Positives', getattr(collection, model.feature+ '_TP'))
        self.printLinkedDocuments(f, 'False Positives', getattr(collection, model.feature+ '_FP'))
        self.printLinkedDocuments(f, 'True Negatives', getattr(collection, model.feature+ '_TN'))
        self.printLinkedDocuments(f, 'False Negatives', getattr(collection, model.feature+ '_FN'))
        f.write("""</body></html>""")
        f.close()
        webbrowser.open_new_tab(pagename)

    def printCluster(self, cluster, openHtml=False):
    	pagename = self.path + '/Cluster/cluster%d.html' % cluster.number
    	f = open(pagename, 'w')
    	f.write("<html>")
        self.writeHead(f, 'Cluster %d' % cluster.number)
        f.write("<body><p> <b> Number of documents in cluster: </b> %d <p>" % len(cluster.features))
        f.write("<body><p> <b> Number of SA documents: </b> %d <p>" % len(cluster.SATrue))
        f.write("<p> <b> Number of DV documents: </b> %d <p>" % len(cluster.DVTrue))

        f.write("<h4>Documents in Cluster</h4>")
        f.write("""<style type="text/css"> body>div {width: 46%; float: left; border: 1px solid} </style></head>""") 
        self.printClusterDocuments(f, 'SA True', cluster.SATrue)
        self.printClusterDocuments(f, 'DV True', cluster.DVTrue)
        self.printClusterDocuments(f, 'Others', cluster.SAFalse + cluster.DVFalse)

    	f.write("</body></html>")
    	f.close()
        if openHtml:
            webbrowser.open_new_tab(pagename)

    def printClusterOverview(self, numbers, SA, DV):
    	pagename = self.path + '/clusterOverview.html'
    	f = open(pagename, 'w')
    	f.write("<html>")
        self.writeHead(f, 'Cluster Overview')
        f.write("<body><table>")
        f.write("""<col style="width:15%"> <col style="width:11%"> <col style="width:10%"> <col style="width:11%"> <col style="width:10%"> <col style="width:11%"> """)
        f.write("""<tr><td></td> <td> <b> Number Docs </b></td> <td><b>SA docs </b></td> <td> <b>SA &#37 </b></td> <td><b>DV docs</b></td> <td><b>DV &#37 </b> </td> </tr>""")
        for ind, elem in enumerate(numbers):
            percent = float(elem/100)
            f.write("""<tr><td><a href='Cluster/cluster%0d.html'> Cluster %d </a></td> <td> %d </td> <td> %d</td> <td> %0.2f &#37 </td> <td> %d</td> <td>%0.2f &#37</td> </tr>""" % (ind, ind, elem, SA[ind], SA[ind]/percent, DV[ind], DV[ind]/percent))
    	f.write("</table></body></html>")
    	f.close()
        webbrowser.open_new_tab(pagename)
