import pandas as pd;
import seaborn as sns
import matplotlib.pyplot as plt
plt.style.use('ggplot')


import numpy as np


#Function to get sequels per platform
def sequelset(Games):
    a=Games.iloc[0][2]
    b=[a]
    c={a:1}
    for i in range(1,Games.count()[0]):
        if a in Games.iloc[i][2]:
            if a not in b:
                b.append(a)
                c[a]=1
            else:
                c[a] += 1
            b.append(Games.iloc[i][2])
        else:
            a=Games.iloc[i][2]

    c = {key: value for key, value in c.items() if value > 1}
    d = pd.DataFrame(c.items())
    e = Games[Games['title'].isin(list(c.keys()))]
    if len(d.columns)>1:
        d.columns=['title','count']
        e= pd.merge(e, d, on='title', sort=False)
    if len(b)>1:
        if b[0] not in b[1]:
            del b[0]
        return Games[Games['title'].isin(b)],e
    return None


#read data and sort it by title so as to filter and find sequel
df=pd.read_csv('ign.csv')
df=df.drop('url',1)
platform=df['platform'].unique().tolist()
df=df.sort_values(['title'])


#store as dictonary all the sequels per platform
DataFrameDict = {elem : pd.DataFrame for elem in platform}
for key in DataFrameDict.keys():
    DataFrameDict[key] = df[:][df.platform == key]
firstgames={elem : pd.DataFrame for elem in platform}
S={elem : pd.DataFrame for elem in platform}
for key in DataFrameDict.keys():
    if sequelset(DataFrameDict[key]) is not None:
        Games,listgames =sequelset(DataFrameDict[key])
        Sortseq=Games.sort_values(['title','release_year','release_month'])
        S[key]= pd.DataFrame(Sortseq)
        firstgames[key]=listgames
    else:
        del S[key]
        del firstgames[key]


result=pd.concat(list(S.values()))
total=result.groupby('platform')['platform'].count()
#Plot to find the platform with most sequels
total.plot(kind='bar')

#Analyse by release_year with sequels
year=result[['platform','release_year']].groupby(['platform','release_year']).size().unstack('platform')
year.plot(kind='bar',stacked=True,colormap='Paired')
plt.figure()

#find the avg score and make a boxplot to find variation
avgscore=result[['platform','score']].fillna(0)
sns.boxplot(avgscore['score'],avgscore['platform'])
plt.figure()

#check the sequel count.How many sequels do each game have
result2=pd.concat(list(firstgames.values()))
platformcount=result2[['platform','count']]
platformcount=platformcount[platformcount['count']<10]
sns.countplot(hue='platform',x='count',data=platformcount)
plt.figure()

#find the most popular genre to make sequels
genre=result[['platform','genre','release_year']]
sns.countplot(y='genre',data=genre)

plt.show()


#varscore=result[['platform','score']].groupby(['platform','score']).unstack('paltform')
#varscore.plot(kind='box',stacked=True)


