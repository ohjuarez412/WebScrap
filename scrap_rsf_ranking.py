import requests
import lxml.html as lh
import pandas as pd
import matplotlib.pyplot as plt


url = "https://rsf.org/en/ranking_table"
page = requests.get(url)
#Store the contents of the website under doc
doc = lh.fromstring(page.content)
#Parse data that are stored between <tr>..</tr> of HTML
tr_elements = doc.xpath('//tr')
#print(tr_elements)
print ([len(T) for T in tr_elements[:12]])
#Create empty list
col=[]
i=0
#For each row, store each first element (header) and an empty list
for t in tr_elements[0]:
    i+=1
    name=t.text_content()
    print ('%d:"%s"'%(i,name))
    col.append((name,[]))

#Since out first row is the header, data is stored on the second row onwards
for j in range(1,len(tr_elements)):
    #T is our j'th row
    T=tr_elements[j]
    
    #If row is not of size 10, the //tr data is not from our table 
    if len(T)!=8:
        break
    
    #i is the index of our column
    i=0
    
    #Iterate through each element of the row
    for t in T.iterchildren():
        data=t.text_content() 
        #Check if row is empty
        if i>0:
        #Convert any numerical value to integers
            try:
                data=int(data)
            except:
                pass
        #Append the data to the empty list of the i'th column
        col[i][1].append(data)
        #Increment i for the next column
        i+=1

#print([len(C) for (title,C) in col])
Dict={title:column for (title,column) in col}
df=pd.DataFrame(Dict)
#pd.to_numeric(df["Abuse score"])
#df=pd.DataFrame(columns=[ 'Abuse score' ], dtype=float)
#df['bee'Abuse score'] = df.beer_servings.astype(float)
df['Countries & regions'] = df['Countries & regions'].astype(str)
df['Abuse score']= df['Abuse score'].astype(float)
df['Underlying situation score']=df['Underlying situation score'].astype(float)
df['Global score']= df['Global score'].astype(float)
df['Diff. score 2018']=df['Diff. score 2018'].astype(float)
print(df.head())
print(df.to_string())
print(df.dtypes)
df2 = df[df.columns[2:]]
df2.to_csv('data_csv.csv')
print(df2.head())
print(df2.describe())
#df2.options.display.mpl_style = 'default'
df2.boxplot()
print(df2.info())
