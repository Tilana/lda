import webbrowser

class htmlCreator:
    def __init__(self):
        pass
    
    def listToHtmlTable(self, f, title, unicodeList):
        f.write("""<h5>%s</h5><table>""" % title.encode('utf8'))
        for items in unicodeList:
            f.write("""<tr><td>%s</td></tr>""" % items.encode('utf8'))
        f.write("""</table>""")
        
    
    def printTupleList(self, f, title, tupleList, colName1='', colName2=''):
        f.write("""<h5>%s</h5><table>""" % title.encode('utf8'))
        f.write("""<col style="width:40%"> <col style="width:50%">""")
        f.write("""<tr><td>%s</td> <td> %s </td></tr>""" % (colName1.encode('utf8'), colName2.encode('utf8')))

        for items in tupleList:
            f.write("""<tr><td>%s </td> <td> %d </td></tr>""" % (items[0].encode('utf8'), items[1]))
        f.write("""</table>""")
    
    
    def htmlDictionary(self, dictionary):
        name = 'html/dictionaryCollection.html'
        f = open(name, 'w')
        f.write("""<html><head><h1>Dictionary of Document Collection</h1><style type="text/css"> body>div {width: 23%; float: left; border: 1px solid} </style></head>""") 
        f.write("""<body><div>""")
        self.listToHtmlTable(f, 'Words in Dictionary', dictionary.words)
        f.write("""</div>""")
        f.write("""<div>""")
        self.listToHtmlTable(f, 'Original (Unlemmatized) Dictionary', dictionary.original)
        f.write("""</div>""")

        f.write("""<div>""")
        self.listToHtmlTable(f, 'Removed Special Characters', dictionary.specialCharacters)
        f.write("""</div>""")
        f.write("""<div>""")
        self.listToHtmlTable(f, 'Stopwords', dictionary.stopwords)

        f.write("""</div></body></html>""")
        f.close()
        webbrowser.open_new_tab('html/dictionaryCollection.html')


    def printTopics(self, model):
        filename = 'html/%stopics.html' % model.name
        f = open(filename, 'w')
        f.write("<html><head><h1> %s Topics</h1></head>" % model.name)
        f.write("<body><p>Topics and related words - %s Model</p><table>" % model.name )
        f.write("""<col style="width:7%"> <col style="width:80%">""")
        for topic in model.topics:
            f.write("<tr><td><a href='%stopic%d.html'> Topic %d</a></td><td>%s</td></tr>" % (model.name, topic.number, topic.number, str(topic.wordDistribution)[1:-1]))
        f.write("</table>")
        f.write("</body></html>")
        f.close()
        
        path = '//home/natalie/Documents/Huridocs/LDA/'+filename
        webbrowser.open_new_tab(path)
    
    
    def printDocuments(self, model, topics=1, openHtml=False):
        for ind, doc in enumerate(model.collection):
            pagename = 'html/doc%02d.html' % ind
            f = open(pagename, 'w')
            f.write("<html><head><h1>Document %02d - %s</h1></head>" % (ind, doc.title.encode('utf-8')))
            f.write("""<body><div style="width:100%;"><div style="float:right; width:40%;">""")
            if topics:
                f.write("""<h3> LSI Topic coverage: \n</h3><table>""")
                f.write("""<col style="width:40%"> <col style="width:50%">""")
                for topicNr, coverage in enumerate(doc.LSICoverage):
                    f.write("""<tr><td><a href='LSItopic%d.html'>Topic %d</a</td><td> Coverage %.2f</td></tr>""" % (topicNr, topicNr, coverage[1]))
                f.write("</table>")
                f.write("""<h3> LDA Topic coverage: \n</h3><table>""")
                f.write("""<col style="width:40%"> <col style="width:50%">""")
                for topicNr, coverage in enumerate(doc.LDACoverage):
                    f.write("""<tr><td><a href='LDAtopic%d.html'>Topic %d</a</td><td> Coverage %.2f</td></tr>""" % (topicNr, topicNr, coverage[1]))
                f.write("</table>")
                f.write("""<h3>Relevant Words in Document: \n</h3><table>""")
                f.write("""<col style="width:40%"> <col style="width:50%">""")
                for freqWord in doc.freqWords:
                    f.write("""<tr><td>%s </td><td> %.2f</td></tr>""" % (freqWord[0], freqWord[1])) 
                f.write("</table>")
                
                f.write("""<h3>Similar documents: \n</h3><table>""")
                f.write("""<col style="width:40%"> <col style="width:50%">""")
                for similarDoc in doc.LSISimilarity:
                    f.write("""<tr><td><a href='doc%02d.html'>Document %d</a></td>""" % (similarDoc[0], similarDoc[0]))
                    f.write("""<td> Similarity: %.4f</td></tr>""" % similarDoc[1])
                f.write("""</table>""")

            self.printTupleList(f, 'Most Frequent Entities', doc.entities.getMostFrequentEntities())

            f.write("""<h3> Named Entities: \n</h3>""")
            for tag in doc.entities.__dict__.keys():
                self.printTupleList(f, tag, getattr(doc.entities, tag))
            f.write("""</div>""")
            f.write("""<div style="float:left; width:55%%;"><p>%s</p></div></div></body></html>""" % doc.text.encode('utf8'))
            f.close()
            if openHtml:
                filename = '//home/natalie/Documents/Huridocs/LDA/html/'+ 'doc%02d.html' % ind
                webbrowser.open_new_tab(filename)
               
# Create a html page for each topic
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
                path = '//home/natalie/Documents/Huridocs/LDA/'+ pagename
                webbrowser.open_new_tab(path)
   
       
