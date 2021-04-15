import requests
import re
from lxml import html
from bs4 import BeautifulSoup
import pandas as pd
from mitrenv.models import *
from collections import Counter
import mysql.connector

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}


def dataUpdateMITRE():
    global techniquesList
    global title

    db_connection = mysql.connector.connect(host="localhost", user="django", passwd="django-user-password",
                                            database="detectionnav")
    db_cursor = db_connection.cursor()

    baseURI = "https://attack.mitre.org"

    tacticshref = []
    tacticsID = []
    tacticsList = []
    tacticsTechniquesDict = {}

    tableHeaders = []
    techniquesList = []

    reqBaseURI = requests.get(baseURI, headers=headers)
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

    l = len(tacticshref)
    j = 0

    for i in range(0, l):
        URI = tacticshref[i]
        respTactURI = requests.get(URI)
        soupTactURI = BeautifulSoup(respTactURI.text, 'html.parser')
        t1 = soupTactURI.find('title').string.split("-")[0]
        title = str(t1.split(",")[0])
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
        # print(title)
        tacticsTechniquesDict[title] = []
        print("-" * 120)

        print(title)
        db_cursor.execute("SELECT * FROM mitrenv_ttp WHERE Tactic='" + title + "'")
        tacresult = db_cursor.fetchall()
        print(tacresult)
        '''
        tacresult = TTP.objects.filter(Tactic=title)
        for a in tacresult:
            x = a.id
            print(x)
        '''

        print(tacresult)

        if tacresult:
            print("TACTIC FOUND")
            for k in range(0, l):
                Tech = str(ndf[k]) + " : " + str(df['Name'][k])
                tacticsTechniquesDict[title].append(Tech)
                db_cursor.execute(
                    "SELECT * FROM mitrenv_techniques WHERE techniqueName='" + str(Tech) + "' AND tactic_id=" + str(
                        tacresult[0][0]))
                techresult = db_cursor.fetchall()
                print(title)
                if not techresult:
                    print("Technique not Found")
                    T = TTP.objects.all().filter(Tactic=title)
                    T1 = Tactic.objects.filter(tacticName=title)

                    for a in T:
                        techList = a.Technique
                        techList.append(Tech)

                    T.update(Technique=techList)

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

                        for ttp in T:
                            T2.tactic_id = ttp.id

                        T2.save()
                        techniquesList.append(Tech)

                    T.update(TotalTech=len(tacticsTechniquesDict[title]))

        else:
            print("TACTIC NOT FOUND")
            T = TTP.objects.create(Tactic="", Technique=[])
            T1 = Tactic.objects.create(tacticName="")
            T.Tactic = title
            T.FuncTact = title[:3]
            T1.tacticName = title
            T1.save()
            print(title)

            for k in range(0, l):
                Tech = str(ndf[k]) + " : " + str(df['Name'][k])
                # print(Tech)
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


def updateRepeats():
    ID = []
    for Technique in techniquesList:
        id = Technique.split(" :")[0].split(".")[0]
        ID.append(id)
    a = dict(Counter(ID))

    db_connection = mysql.connector.connect(host="localhost", user="django", passwd="django-user-password",
                                            database="detectionnav")
    db_cursor = db_connection.cursor()

    for key, value in a.items():
        db_cursor.execute(
            'update mitrenv_techniques set techniqueRepeat=' + str(value) + ' WHERE techniqueId="' + key + '";')
        db_connection.commit()
