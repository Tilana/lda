# flatten list - convert list of sublist to one listA
def flattenList(l):
	return [item for sublist in l for item in sublist]

# compute difference between elements in a list of integer
def getListDifference(intList):
    return [ successor - predecessor for predecessor, successor in zip(intList, intList[1:])]

# find consecutive element in an integer list resembling differences between elements
def getConsecutiveIndices(intList):
    return [ind for ind, elem in enumerate(intList) if elem==1]

# split a list in sublist when difference between elements is bigger than 1
def splitInSublists(intList):
    lists = []
    sublist = []
    for ind, elem in enumerate(intList):
        if elem==1:
            sublist.append(ind)
        else:
            lists.append(sublist)
            sublist = [ind]
    return lists

