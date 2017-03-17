from lda import Info, docLoader
from lda import dataframeUtils as df
import pandas as pd

def combine_ICAAD_data():

    info = Info()
    info.data = 'ICAAD'
    info.setPath()
    
    titles, text = docLoader.loadEncodedFiles(info.path)
    data = pd.DataFrame([titles[0:], text[0:]], index = ['title', 'text'])
    data = data.transpose()
    df.changeStringsInColumn(data, 'title', '.rtf.txt', '')

    evaluationFile = 'Documents/PACI.csv'
    dataFeatures = pd.read_csv(evaluationFile)
    df.changeStringsInColumn(dataFeatures, 'Filename', '.txt', '')
    dataFeatures = dataFeatures.rename(columns = {'Unnamed: 0':'id',  'Filename':'title'})


    data = data.merge(dataFeatures, on='title', how='left')
    data = data.dropna(subset=['Sexual.Assault.Manual', 'Domestic.Violence.Manual'])

    df.save(data, 'Documents/ICAAD/ICAAD2.pkl')


if __name__ == "__main__":
    combine_ICAAD_data()
