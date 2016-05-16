def getRow(df, colname, value, columns):
    return list(df.loc[df[colname]==value, columns].values[0])

def filterData(df, colname):
    return df[df[colname]]

def getIndex(df):
    return df.index.tolist()


