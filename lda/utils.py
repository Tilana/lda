# flatten list - convert list of sublist to one listA
def flattenList(l):
	return [item for sublist in l for item in sublist]

# compare Object with list attributes
def compareListObjects(obj1, obj2):
    keysObj1 = obj1.__dict__.keys()
    keysObj2 = obj2.__dict__.keys()
    if len(keysObj1) == len(keysObj2):
        if keysObj1 == keysObj2:
            for attribute in keysObj1:
                if not (getattr(obj1, attribute) == getattr(obj2, attribute)):
                    return False
    return True




