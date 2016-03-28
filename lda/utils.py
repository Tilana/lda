from unittest import TestCase

# flatten list - convert list of sublist to one listA
def flattenList(l):
	return [item for sublist in l for item in sublist]

# compute distance between elements in integer list
def listDifference(l):
    return [(elem[1]-elem[0], elem[0]) for elem in zip(l[:-1],l[1:])]
