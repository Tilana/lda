import webbrowser

# create html overview file for a document
def htmlOutput(doc, ind, namedEntities):	
	name = 'html/nlpDoc%02d.html' % ind
	f = open(name, 'w')
	f.write("<html><head><h1>Doc %02d - %s </h1></head>" % (ind, doc[0:10].encode('utf8')))
	f.write("""<body><div style="width:100%;"><div style="float:right; width:40%;">""")
	f.write("""<h3>Named Entities: \n</h3><table>""")
	f.write("""<col style="width:40%"> <col style="width:50%">""")
	for ent in namedEntities:
		f.write("""<tr><td>%s</td> </tr>""" % ent)
	f.write("""</table></div>""")
	f.write("""<div style="float:left; width:55%%;"><p>%s</p></div></div></body></html>""" % doc.encode('utf8'))
	f.close()
	webbrowser.open_new_tab('html/nlpDoc%02d.html' % ind)

# print unprocessed and processed dictionary
def createDictHtml(doc, namedEntities, origDict, procDict):
	name = 'html/dictionary.html'
	f = open(name, 'w')
	f.write("<html><head><h1> Dictionary </h1></head>")
	f.write("""<body><div style="width:100%;"><div style="float:left; width:20%;">""")
	f.write("""<h3> Un-Processed \n</h3><table>""")
	for words in origDict: 
		f.write("""<tr><td>%s</td> </tr>""" % words.encode('utf8'))
	f.write("""</table></div>""")
	f.write("""<div style="float:left; width:20%%;">""")
	f.write("""<h3> Processed \n</h3><table>""")
	for words in procDict:
		f.write("""<tr><td>%s</td> </tr>""" % words.encode('utf8'))
	f.write("""</table></div>""")
	f.write("""<div style="float:left; width:50%%;">""")
	f.write("""<h3> Removed Words \n</h3><table>""")
	for words in procDict:
		f.write("""<tr><td>%s</td> </tr>""" % words.encode('utf8'))
	f.write("""</table></div>""")
	f.write("""</div></body></html>""")
	f.close()
	webbrowser.open_new_tab('html/dictionary.html')


