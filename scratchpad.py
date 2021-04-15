import requests
import re
from lxml import html
from bs4 import BeautifulSoup
import pandas as pd
from collections import Counter
import mysql.connector

baseURI = "https://attack.mitre.org"
basehref = []
tacticshref = []
tacticsList = []
tacticsID = []
tacticsList = []
tacticsTechniquesDict = {}
tableHeaders = []
techniquesList = []
ID = []

reqBaseURI = requests.get(baseURI)
soupBaseURI = html.fromstring(reqBaseURI.content)
basehref = soupBaseURI.xpath('//a/@href')
rBase = re.compile("/tactics/TA\d+")
tacList = list(filter(rBase.match, basehref))

for z in tacList:
    if z not in tacticsList:
        tacticsList.append(z)

for tacturi in tacticsList:
    tacticshref.append(str(baseURI) + str(tacturi))

for tacturi in tacticshref:
    tacticsID.append(tacturi.split("/")[-1])

m = len(tacticshref)
j = 0

for i in range(0, m):
    global j
    URI = tacticshref[i]
    respTactURI = requests.get(URI)
    soupTactURI = BeautifulSoup(respTactURI.text, 'html.parser')
    t1 = soupTactURI.find('title').string.split("-")[0]
    title = t1.split(",")[0]
    tableHeaders.append(title)
    dfs = pd.read_html(URI)
    df = dfs[0]
    ndf = []
    l = len(df['ID'])

    for i in range(0, l):
        subid = df['ID'][i]
        if str(subid) == "nan":
            j += 1
            id = df['ID'][i - j]
            ndf.append(str(id) + "." + str('{:03}'.format(j)))
        else:
            ndf.append(str(subid))
            j = 0

    print("-" * 120)
    print(title)
    tacticsTechniquesDict[title] = []
    print("-" * 120)

    for k in range(0,l):
        Tech = str(ndf[k]) + " : " + str(df['Name'][k])
        print(Tech)
        tacticsTechniquesDict[title].append(Tech)
        techniquesList.append(Tech)


for Technique in techniquesList:
    id = Technique.split(" :")[0].split(".")[0]
    ID.append(id)
a = dict(Counter(ID))

#for key,value in a.items():
#    print(str(key) + " : " + str(value))

db_connection = mysql.connector.connect(host="localhost", user="django", passwd="django-user-password",database="mitrenav")
db_cursor = db_connection.cursor()

for key,value in a.items():
    db_cursor.execute('update mitrenv_techniques set techniqueRepeat='+ str(value) +' WHERE techniqueId="'+ key +'";')
    db_connection.commit()

'''
    for k in range(0, l):
        Tech = str(ndf[k]) + " : " + str(df['Name'][k])
        print(Tech)
        tacticsTechniquesDict[title].append(Tech)
        # techniquesList.append(Tech)

for Technique in techniquesList:
    id = Technique.split(" :")[0].split(".")[0]
    ID.append(id)
a = dict(Counter(ID))
print(a)
'''