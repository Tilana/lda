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
        
    
