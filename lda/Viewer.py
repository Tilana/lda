import webbrowser
import os, sys

class Viewer:

    def __init__(self, identifier):
        path = 'hmtl/'+identifier
        try:
            os.makedirs(path)
        except OSError:
            if not os.path.isdir(path):
                raise
    
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
        name = 'html/wordDocFrequency%d%d.html' % (start, end)
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
        webbrowser.open_new_tab('html/wordDocFrequency%d%d.html' % (start, end))


    def htmlDictionary(self, dictionary):
        name = 'html/dictionaryCollection.html'
        f = open(name, 'w')
        f.write("""<html><head><h1>Dictionary of Document Collection</h1><style type="text/css"> body>div {width: 23%; float: left; border: 1px solid} </style></head>""") 

        f.write("""<body>""")
        self.printColumn(f, 'Words in Dictionary ', dictionary.ids.values())
        self.printColumn(f, 'Removed Special Characters ', dictionary.specialCharacters)
        self.printColumn(f, 'Stopwords ', dictionary.stopwords)
        f.write("""</body></html>""")
        f.close()
        webbrowser.open_new_tab('html/dictionaryCollection.html')


    def printTopics(self, model):
        filename = 'html/%stopics.html' % model.name
        f = open(filename, 'w')
        f.write("<html><head><h1> %s Topics</h1></head>" % model.name)
        f.write("<body><p>Topics and related words - %s Model</p><table>" % model.name )
        f.write("""<col style="width:7%"> <col style="width: 20%"> <col style="width: 7%"> <col style="width:80%"> <col style="width:8%">""")

        for topic in model.topics:
            f.write("<tr><td><a href='%stopic%d.html'> Topic %d</a></td><td>%s </td><td>%.4f</td><td>%s</td><td>%s</td></tr>" % (model.name, topic.number, topic.number, topic.keywords[0:3], topic.meanSimilarity, str(topic.wordDistribution[0:7])[1:-1], topic.intruder))
        f.write("</table>")
        
        f.write("Mean Similarity Score: %.4f" % model.meanScore)
        f.write("<p> <h4> Possible Categories: </h4> %s</p>" % model.categories)
        f.write("</body></html>")
        f.close()
        
        webbrowser.open_new_tab(filename)
    
    
    def printDocuments(self, collection, lda, topics=1, openHtml=False):
        for ind, doc in enumerate(collection):
            pagename = 'html/doc%02d.html' % ind
            attributes = doc.__dict__.keys()
            f = open(pagename, 'w')
            f.write("<html><head><h1>Document %02d - %s</h1></head>" % (ind, doc.title))
            f.write("""<body><div style="width:100%;"><div style="float:right; width:45%;">""")
            
            if 'LDACoverage' in attributes:
                f.write("""<h4> LDA Topic coverage:</h4><table>""")
                f.write("""<col style="width:20%"> <col style="width:50%"> <col style = "width:30%"> """)
                for coverage in doc.LDACoverage[0:5]:
                    topicNr = coverage[0]
                    f.write("""<tr><td><a href='LDAtopic%d.html'>Topic %d</a</td> <td> %s</td> <td> Coverage %.2f</td></tr>""" % (topicNr, topicNr, lda.topics[topicNr].keywords[0:2], coverage[1]))
                f.write("</table>")

            if 'LSICoverage' in attributes:
                f.write("""<h4> LSI Topic coverage:</h4><table>""")
                f.write("""<col style="width:20%"> <col style="width:50%"> <col style = "width:30%"> """)
                for coverage in doc.LSICoverage[0:5]:
                    topicNr = coverage[0]
                    f.write("""<tr><td><a href='LSItopic%d.html'>Topic %d</a</td> <td> %s</td> <td> Coverage %.2f</td></tr>""" % (topicNr, topicNr, lda.topics[topicNr].keywords[0:2], coverage[1]))
                f.write("</table>")

            if 'targetCategories' in attributes:
                self.listToHtmlTable(f, 'Target Categories', doc.targetCategories)

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
                self.printTupleList(f, tag, getattr(doc.entities, tag))
            f.write("""</div>""")
            f.write("""<div style="float:left; width:55%%;"><p>%s</p></div></div></body></html>""" % doc.text.encode('utf8'))
            f.close()
            if openHtml:
                webbrowser.open_new_tab(pagename)
               
    
    def printDocsRelatedTopics(self, model, collection, openHtml=False):
        for num in range(0, model.numberTopics): 
    	    pagename = 'html/%stopic%d.html' % (model.name, num)
    	    f = open(pagename, 'w')
    	    f.write("<html><head><h1> %s Document Relevance for Topic %d</h1></head>" %  (model.name, num))
            f.write("<body><h4>Topics and related words - %s Model</h4><table>" % model.name)
            f.write("""<col style="width:7%"> <col style="width:80%">""")
            topic = model.topics[num]
            f.write("<tr><td><a href='%stopic%d.html'>Topic %d</a></td><td>%s</td></tr>" % (model.name, topic.number, topic.number, str(topic.wordDistribution)[1:-1].encode('utf-8')))
            f.write("</table>")
    	    f.write("<h4>Related Documents</h4>")
            f.write("<table>") 
    	    f.write("""<col style="width:10%"> <col style="width:40%"> <col style="width:25%">""")
    	    for doc in model.topics[num].relatedDocuments[0:15]:
    	    	f.write("<tr><td><a href='doc%02d.html'>Document %d</a></td><td>%s</td><td>Relevance: %.2f</td></tr>" % (doc[1], doc[1], collection[doc[1]].title.encode('utf8'), doc[0]))
    
    	    f.write("</table></body></html>")
    	    f.close()
            if openHtml:
                webbrowser.open_new_tab(path)
    

    def freqAnalysis(self, collection, openHtml=False):
        for ind, doc in enumerate(collection):
            pagename = 'html/%s' % doc.title
            f = open(pagename, 'w')
            f.write("<html><head><h1>Document %02d - %s</h1></head>" % (ind, doc.name))
            f.write("""<body><div style="width:100%;"><div style="float:right; width:40%;">""")
            f.write("""<h4> Topic Suggestions <h4>""")
          
            self.printTupleList(f, ' ', doc.mostFrequent)
            self.printColoredList(f, 'Manual Topic Assignment', doc.assignedKeywords)

            f.write("""<h4> All Keywords \n</h4>""")
            for tag in doc.entities.__dict__.keys():
                if getattr(doc.entities, tag):
                    self.printTupleList(f, tag, getattr(doc.entities, tag))
            f.write("""</div>""")
            f.write("""<div style="float:left; width:55%%;"><p>%s</p></div></div></body></html>""" % doc.text.encode('utf8'))
            f.close()
            if openHtml:
                webbrowser.open_new_tab(pagename)


    def freqAnalysis_eval(self, model):
        pagename = 'html/freqAnalysis_eval.html'
        f = open(pagename, 'w')
        f.write("<html><head><h1> Evaluation of frequency analysis </h1></head>")
        f.write("""<body><div style="width:100%;">""")
        f.write(""" <h4> Number of analysed documents: %d </h4> """ % len(model.collection))
        f.write(""" <h4>%d out of %d keywords are not detected </h4>""" % (len(model.undetectedKeywords), model.numberKeywords))
        f.write("""<h4> Accuracy: %f </h4>""" % ((1-(len(model.undetectedKeywords)/float(model.numberKeywords)))*100) )

        f.write("""<h4> Missed keywords: </h4>""")
        
        f.write("""<table>""")
        for keywords in model.undetectedKeywords:
            f.write("<tr><td><a href='%s.html'>%s</a></td><td>%s</td></tr>" % (keywords[0].replace('/','_'), keywords[0], keywords[1]))

        f.write("""</table></div></body></html>""")
        f.close()
        webbrowser.open_new_tab(pagename)


    def classificationResults(self, model):
        pagename = 'html/classificationResults.html'
        f = open(pagename, 'w')
        f.write("<html><head><h1> Classification results </h1></head>")
        f.write("""<body><div style="width:100%;">""")
        f.write(""" <p><b> Target Feature: </b> %s </p> """ % model.targetFeature) 
        f.write(""" <p><b> Size of Training Data: </b> %s </p> """ % len(model.trainData))
        f.write(""" <p><b> Size of Test Data: </b> %s </p>""" % len(model.testData))
        self.listToHtmlTable(f, 'Ignored Features', model.droplist)

        f.write(""" <h2> Evaluation: </h2>""")
        f.write("""<table> """)
        f.write("""<tr><td> Accuracy: </td><td> %.2f </td></tr>""" % model.accuracy)
        f.write("""<tr><td> Precision: </td><td> %.2f </td></tr>""" % model.precision)
        f.write("""<tr><td> Recall: </td><td> %.2f </td></tr>""" % model.recall)
        f.write("""</table>""")

        self.printConfusionMatrix(f, model.confusionMatrix)

        self.printTupleList(f, 'Feature Importance', model.featureImportance, format='float')

        f.write("""</table></div></body></html>""")
        f.close()
        webbrowser.open_new_tab(pagename)

    def LDATopics(self, name, lda, numberTopics):
        f = open(name, 'w')
        f.write("""<html><head><h2> LDA - 30 Topics - 40 passes </h2></head><body> <table>""")
        
        for index in range(0, numberTopics):
            f.write("<tr><td> Topic %d </td> <td> %s </td></tr>" % (index, lda.print_topic(index)))
        f.write("</table></body></html>")
        f.close()
        
        webbrowser.open_new_tab(name)
