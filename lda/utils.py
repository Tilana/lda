#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase

# flatten list - convert list of sublist to one listA
def flattenList(l):
	return [item for sublist in l for item in sublist]

# compute distance between elements in integer list
def listDifference(l):
    return [(elem[1]-elem[0], elem[0]) for elem in zip(l[:-1],l[1:])]

def containsAny(str, specialChars):
    for letter in str:
        if letter in specialChars:
            return 1;
    return 0;

def absoluteTupleList(tupleList):
    return [(abs(elem[0]), abs(elem[1])) for elem in tupleList]



