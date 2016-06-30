def getRow(df, colname, value, columns):
    return list(df.loc[df[colname]==value, columns].values[0])

def getColumn(df, colname):
    columnValues = list(df[colname].unique())
    return [value for value in columnValues if value != 'nan']

def filterData(df, colname):
    return df[df[colname]]

def getIndex(df):
    return df.index.tolist()

def tolist(df, column):
    return df[column].values.tolist()

def toListMultiColumns(df, columnList):
    result = set() 
    for col in columnList:
        result.update(tolist(df, col))
    return result

def getValue(df, column):
    value = df[column].tolist()
    if value != []:
        return value[0]
    else:
        return 'nan'


