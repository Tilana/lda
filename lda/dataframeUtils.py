import pandas as pd

def getRow(df, colname, value, columns):
    return list(df.loc[df[colname]==value, columns].values[0])



        

