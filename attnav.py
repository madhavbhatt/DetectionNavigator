import requests
import re
from lxml import html
from bs4 import BeautifulSoup
import pandas as pd
import validators
from DetectionChart.models import *
from collections import Counter
import mysql.connector


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}


def dataPullMITRE():
    global techniquesList

    baseURI = "https://attack.mitre.org"
    basehref = []

    tacticshref = []
    tacticsList = []
    tacticsID = []
    tacticsList = []
    tacticsTechniquesDict = {}

    tableHeaders = []
    techniquesList = []

    reqBaseURI = requests.get(baseURI,headers=headers)
    soupBaseURI = html.fromstring(reqBaseURI.content)
    basehref = soupBaseURI.xpath('//a/@href')

    rBase = re.compile("/tactics/TA\d+")
    #tacList = list(filter(rBase.match, basehref))
    tacList = list(filter(rBase.search, basehref))

    for z in tacList:
        if z not in tacticsList:
            tacticsList.append(z)

    for tacturi in tacticsList:
        if not validators.url(tacturi):
            tacticshref.append(str(baseURI) + str(tacturi))
        else:
            tacticshref.append(str(tacturi))

    for tacturi in tacticshref:
        tacticsID.append(tacturi.split("/")[-1])

    l = len(tacticshref)
    j = 0

    for i in range(0, l):
        T = TTP.objects.create(Tactic="", Technique=[])
        T1 = Tactic.objects.create(tacticName="")
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
        T.Tactic = title
        T.FuncTact = title[:3]
        T1.tacticName = title
        T1.save()
        for i in range(0, l):
            subid = df['ID'][i]
            if str(subid) == "nan":
                j += 1
                id = df['ID'][i - j]
                ndf.append(str(id) + "." + str('{:03}'.format(j)))
            else:
                ndf.append(str(subid))
                j = 0

        tacticsTechniquesDict[title] = []
        for k in range(0, l):
            Tech = str(ndf[k]) + " : " + str(df['Name'][k])
            tacticsTechniquesDict[title].append(Tech)
            T.Technique.append(str(Tech))
            if Tech in techniquesList:
                T2 = Techniques.objects.create(techniqueName="")
                T2.techniqueName = str(Tech)
                T2.techniqueId = ndf[k]

                if not re.findall('T\d{4}.\d{3}', ndf[k]):
                    T2.SubTechnique = False
                else:
                    T2.SubTechnique = True
                T2.tactic = T
                T2.save()
            else:
                T2 = Techniques.objects.create(techniqueName="")
                T2.techniqueName = str(Tech)
                T2.techniqueId = ndf[k]

                if not re.findall('T\d{4}.\d{3}', ndf[k]):
                    T2.SubTechnique = False
                else:
                    T2.SubTechnique = True
                T2.tactic = T
                T2.save()
                techniquesList.append(Tech)
        # T.Technique = techniquesList
        T.TotalTech = len(tacticsTechniquesDict[title])
        T.save()

def attnavupdateRepeats():
    ID = []
    for Technique in techniquesList:
        id = Technique.split(" :")[0].split(".")[0]
        ID.append(id)
    a = dict(Counter(ID))

    db_connection = mysql.connector.connect(host="localhost", user="django", passwd="django-user-password",database="detectionnav")
    db_cursor = db_connection.cursor()

    for key, value in a.items():
        db_cursor.execute('update DetectionChart_techniques set techniqueRepeat=' + str(value) + ' WHERE techniqueId="' + key + '";')
        db_connection.commit()
