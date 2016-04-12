import webbrowser

class htmlCreator:
    def __init__(self):
        pass
    
    def listToHtmlTable(self, f, title, unicodeList):
        f.write("""<h5>%s</h5><table>""" % title.encode('utf8'))
        for items in unicodeList:
            f.write("""<tr><td>%s</td></tr>""" % items.encode('utf8'))
        f.write("""</table>""")
        
    
    # create html file of dictionary
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

    def printTopics(self, model, topicType='LDA'):
        if topicType=='LSI':
            print "LSI Topic TYPE"
            topicList = model.lsiTopics
        else:
            topicList = model.ldaTopics
        print  len(model.ldaTopics)
        filename = 'html/%stopics.html' % topicType
        f = open(filename, 'w')
        f.write("<html><head><h1> %s Topics</h1></head>" % topicType)
        f.write("<body><p>Topics and related words - %s Model</p><table>" % topicType )
        f.write("""<col style="width:7%"> <col style="width:80%">""")
        for topic in topicList:
            f.write("<tr><td><a href='%stopic%d.html'> Topic %d</a></td><td>%s</td></tr>" % (topicType, topic.number, topic.number, str(topic.wordDistribution)[1:-1]))
        f.write("</table>")
        f.write("</body></html>")
        f.close()
        
        path = '//home/natalie/Documents/Huridocs/LDA/'+filename
        webbrowser.open_new_tab(path)
    
    
    def printDocuments(self, model, openHtml=False):
        for ind, doc in enumerate(model.collection):
            pagename = 'html/doc%02d.html' % ind
            f = open(pagename, 'w')
            f.write("<html><head><h1>Document %02d - %s</h1></head>" % (ind, doc.title.encode('utf-8')))
            f.write("""<body><div style="width:100%;"><div style="float:right; width:40%;">""")
            f.write("""<h3>Topic coverage: \n</h3><table>""")
            f.write("""<col style="width:40%"> <col style="width:50%">""")
            for topicNr, coverage in enumerate(doc.lsiCoverage):
                f.write("""<tr><td><a href='topic%d.html'>Topic %d</a</td><td> Coverage %.2f</td></tr>""" % (topicNr, topicNr, coverage[1]))
            f.write("</table>")
            f.write("""<h3>Relevant Words in Document: \n</h3><table>""")
            f.write("""<col style="width:40%"> <col style="width:50%">""")
            for freqWord in doc.freqWords:
                f.write("""<tr><td>%s </td><td> %.2f</td></tr>""" % (freqWord[0], freqWord[1])) 
            f.write("</table>")
            
            f.write("""<h3>Similar documents: \n</h3><table>""")
            f.write("""<col style="width:40%"> <col style="width:50%">""")
            for similarDoc in doc.lsiSimilarity:
                f.write("""<tr><td><a href='doc%02d.html'>Document %d</a></td>""" % (similarDoc[0], similarDoc[0]))
                f.write("""<td> Similarity: %.4f</td></tr>""" % similarDoc[1])
            f.write("""</table>""")
            f.write("""<h3> Named Entities: \n</h3>""")
            for tag in doc.entities.__dict__.keys():
                self.listToHtmlTable(f, tag, getattr(doc.entities, tag))
            f.write("""</div>""")
            f.write("""<div style="float:left; width:55%%;"><p>%s</p></div></div></body></html>""" % doc.text.encode('utf8'))
            f.close()
            if openHtml:
                filename = '//home/natalie/Documents/Huridocs/LDA/html/'+ 'doc%02d.html' % ind
                webbrowser.open_new_tab(filename)
               
# Create a html page for each topic
    def printDocsRelatedTopics(self, model, topicType='LDA', openHtml=False):
        if topicType=='LSI':
            topicList = model.lsiTopics
        else:
            topicList = model.ldaTopics
        for num in range(0, model.numberTopics): 
    	    pagename = 'html/%stopic%d.html' % (topicType, num)
    	    f = open(pagename, 'w')
    	    f.write("<html><head><h1>Document Relevance for %s Topic %d</h1></head>" %  (topicType, num))
            f.write("<body><h4>Topics and related words - %s Model</h4><table>" % topicType)
            f.write("""<col style="width:7%"> <col style="width:80%">""")
            topic = topicList[num]
            f.write("<tr><td><a href='%stopic%d.html'>Topic %d</a></td><td>%s</td></tr>" % (topicType, topic.number, topic.number, str(topic.wordDistribution)[1:-1].encode('utf-8')))
            f.write("</table>")
    	    f.write("<h4>Related Documents</h4>")
            f.write("<table>") 
    	    f.write("""<col style="width:10%"> <col style="width:40%"> <col style="width:25%">""")
    	    # get index and relevance for each document regarding a topic
    	    # TODO: check meaning of negative numbers -> take absolute value if necessary
    	    for doc in topicList[num].relatedDocuments[0:15]:
    	    	f.write("<tr><td><a href='doc%02d.html'>Document %d</a></td><td>%s</td><td>Relevance: %.2f</td></tr>" % (doc[0], doc[0], model.collection[doc[0]].title.encode('utf8'), doc[1]))
    
    	    f.write("</table></body></html>")
    	    f.close()
            if openHtml:
                path = '//home/natalie/Documents/Huridocs/LDA/'+ pagename
                webbrowser.open_new_tab(path)
   
       
