import mysql.connector

def flushDB():
    db_connection = mysql.connector.connect(host="localhost", user="django", passwd="django-user-password", database="detectionnav")
    db_cursor = db_connection.cursor()
    db_cursor.execute('DELETE FROM DetectionChart_techniques')
    db_cursor.execute('DELETE FROM DetectionChart_ttp')
    db_cursor.execute('DELETE FROM DetectionChart_tactic')
    db_connection.commit()

"""
def checkSubTechnique(x):
    if re.findall('T\d{4}.\d{3}', x):
        return True
    elif re.findall('T\d{4}', x):
        return False

rows = cursor.execute('SELECT * FROM mitrenav_ttp').fetchall()
l = len(rows)

for i in range(0,l):
    Title = rows[i][1]
    print("-"*120)
    print(Title)
    print("-" * 120)
    ListA = rows[i][2]
    ListB = ListA.strip("[").strip("]").split(",")
    j = len(ListB)
    for k in range(0,j):
        Technique = ListB[k].replace("'","")
        print(Technique)


"""