import pandas as pd
import os
import shutil

files = pd.read_csv('hrc_files2.csv')
files['title'] = files['title'].astype(str)

files['newTitle'] = files['title'].apply(lambda x: x.split('.')[0])
files['newTitle'] = files['newTitle'].apply(lambda x: x.split('-')[0])

#resolutions = data[data.name.str.contains('HRC')]

resolutions = pd.read_excel('HRC_TopicAssignment.xlsx')
resolutionNames = resolutions['Symbol'].tolist()
resolutions['title']  = [name.replace('/', '_')+'-clean.html' for name in resolutionNames]

data = files[files['title'].isin(resolutions['title'].tolist())]
data = data[['content_id', 'title', 'newTitle']]

categories = resolutions[resolutions['title'].isin(data['title'].tolist())]
categories = categories[['title', 'Title', 'Topic 1', 'Topic 2', 'Topic 3']]

topics = pd.merge(data, categories, on='title')
topics = topics.rename(columns={'title': 'path', 'newTitle': 'identifier', 'Title':'title', 'content_id': 'filenr'})

if not os.path.exists('resolutions'):
    os.makedirs('resolutions')

for index, row in topics.iterrows():
    filename = '2016/02/26/%d' % row['filenr']
    shutil.copy(filename, 'resolutions/%s' % row['identifier'])

topics.to_csv('hrc_topics.csv', encoding='utf8')



