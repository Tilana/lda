import docLoader

class docCollection:
	def __init__(self, path):
		(titles, docs) = docLoader.loadCouchdb(path)
		self.titles = titles
		self.docs = docs


