import webbrowser

class htmlCreator:
    def __init__(self):
        pass
    
    def listToHtmlTable(self, f, title, unicodeList):
        f.write("""<h3>%s</h3><table>""" % title.encode('utf8'))
        for items in unicodeList:
            f.write("""<tr><td>%s</td></tr>""" % items.encode('utf8'))
        f.write("""</table>""")
        
    # create html overview file for a document
    def htmlDocumentEntities(self, collection, ind):
        name = 'html/docEntities%02d.html' % ind
        f = open(name, 'w')
        document = collection.documents[ind]
        f.write("<html><head><h1>Document %02d - %s </h1></head>" % (ind, document.title.encode('utf8')))
        f.write("""<body><div style="width:100%;"><div style="float:right; width:40%;">""")
        f.write("""<h3>Named Entities: \n</h3>""")
        for tag in document.entities.__dict__.keys():
            self.listToHtmlTable(f, tag, getattr(document.entities, tag))
        f.write("""</div>""")
        f.write("""<div style="float:left; width:55%%;"><p>%s</p></div></div></body></html>""" % document.text.encode('utf8'))
        f.close()
        webbrowser.open_new_tab('html/docEntities%02d.html' % ind)
    
    # create html file of dictionary
    def htmlDictionary(self, collection):
        name = 'html/dictionaryCollection.html'
        f = open(name, 'w')
        dictionary = collection.dictionary
        f.write("<html><head><h1>Dictionary of Document Collection</h1></head>") 
        f.write("""<body><div style="width:100%;"><div style="float:right; width:40%;">""")
        self.listToHtmlTable(f, 'Stopwords', dictionary.stopwords)
        f.write("""</div>""")
        f.write("""<div style="float:left; width:55%%;">""")
        self.listToHtmlTable(f, 'Words in Dictionary', dictionary.words)
        f.write("""</div></div></body></html>""")
        f.close()
        webbrowser.open_new_tab('html/dictionaryCollection.html')
       
    # print unprocessed and processed dictionary
    def compareDictionaries(self, collection):
        name = 'html/dictionary.html'
        f = open(name, 'w')
        f.write("<html><head><h1> Dictionary </h1></head>")
        f.write("""<body><div style="width:100%;"><div style="float:left; width:20%;">""")
        f.write("""<h3> Un-Processed \n</h3><table>""")
        for words in collection.dictionary:
            f.write("""<tr><td>%s</td> </tr>""" % words.encode('utf8'))
        f.write("""</table></div>""")
        f.write("""<div style="float:left; width:20%%;">""")
        f.write("""<h3> Processed \n</h3><table>""")
        for words in collection.dictionary:
            f.write("""<tr><td>%s</td> </tr>""" % words.encode('utf8'))
        f.write("""</table></div>""")
        f.write("""<div style="float:left; width:50%%;">""")
        f.write("""<h3> Removed Words \n</h3><table>""")
        for words in collection.dictionary:
            f.write("""<tr><td>%s</td> </tr>""" % words.encode('utf8'))
        f.write("""</table></div>""")
        f.write("""</div></body></html>""")
        f.close()
        webbrowser.open_new_tab('html/dictionary.html')
    
    def printTopics(self, model, numTopic=10):
        f = open('html/topics.html', 'w')
        f.write("<html><head><h1>Topics</h1></head>")
        f.write("<body><p>Topics and their related words - LSI Model</p><table>")
        f.write("""<col style="width:7%"> <col style="width:80%">""")
        for topic in model.lsi.print_topics(num_topics=numTopic):
            f.write("<tr><td><a href='topic%d.html'>Topic %d</a></td><td>%s</td></tr>" % (topic[0], topic[0], topic[1].encode('utf-8')))
        f.write("</table>")
        f.write("</body></html>")
        f.close()
        
        filename = '//home/natalie/Documents/Huridocs/LDA/html/'+'topics.html'
        webbrowser.open_new_tab(filename)
    
    
    def printDocuments(self, model, numTopic=10):
    # Create a html page for each document
        for ind,doc in enumerate(model.collection.documents):
            pagename = 'html/doc%02d.html' % ind
            f = open(pagename, 'w')
            f.write("<html><head><h1>Document %02d</h1></head>" % ind)
            f.write("""<body><div style="width:100%;"><div style="float:right; width:40%;">""")
            f.write("""<h3>Topic coverage: \n</h3><table>""")
            f.write("""<col style="width:40%"> <col style="width:50%">""")
            for topicNr, coverage in enumerate(model.collection.documents[ind].lsiCoverage):
                f.write("""<tr><td><a href='topic%d.html'>Topic %d</a</td><td> Coverage %.2f</td></tr>""" % (topicNr, topicNr, coverage[1]))
            f.write("</table>")
            f.write("""<h3>Relevant Words in Document: \n</h3><table>""")
            f.write("""<col style="width:40%"> <col style="width:50%">""")
            for freqWord in model.collection.documents[ind].freqWords:
                f.write("""<tr><td>%s </td><td> %.2f</td></tr>""" % (freqWord[0], freqWord[1])) 
                f.write("</table>")
            
            f.write("""<h3>Similar documents: \n</h3><table>""")
            f.write("""<col style="width:40%"> <col style="width:50%">""")
            for similarDoc in model.collection.documents[ind].lsiSimilarity:
                f.write("""<tr><td><a href='doc%02d.html'>Document %d</a></td>""" % (similarDoc[0], similarDoc[0]))
                f.write("""<td> Similarity: %.4f</td></tr>""" % similarDoc[1])
            f.write("""</table></div>""")
            f.write("""<div style="float:left; width:55%%;"><p>%s</p></div></div></body></html>""" % model.collection.documents[ind].text.encode('utf8'))
            f.close()
            filename = '//home/natalie/Documents/Huridocs/LDA/html/'+ 'doc%02d.html' % ind
            webbrowser.open_new_tab(filename)
               
        
