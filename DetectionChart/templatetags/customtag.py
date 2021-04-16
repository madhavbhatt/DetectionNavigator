from django import template
import mysql.connector

register = template.Library()

@register.filter(name='updateColor')
def updateColor(value,arg):
    techname = str(value)
    color=str(arg)
    print("tech name : " + str(techname))
    print("color name :" + str(color))
    db_connection = mysql.connector.connect(host="localhost", user="django", passwd="django-user-password", database="detectionnav")
    db_cursor = db_connection.cursor()
    db_cursor.execute("UPDATE DetectionChart_techniques SET techColor='"+ color +"' WHERE techniqueName = 'T1529 : System Shutdown/Reboot'")
    db_connection.commit()
    return techname

'''
@register.filter(name='orange')
def orange(value):
    techname = value
    # color=str(arg)
    print("tech name : " + str(techname))
    #print("color name :" + str(color))
    db_connection = mysql.connector.connect(host="localhost", user="django", passwd="django-user-password", database="detectionnav")
    db_cursor = db_connection.cursor()
    db_cursor.execute("UPDATE mitrenv_techniques SET techColor='orange' WHERE techniqueName = 'T1529 : System Shutdown/Reboot'")
    db_connection.commit()
    return techname

@register.filter(name='green')
def green(value):
    techname = value
    # color=str(arg)
    print("tech name : " + str(techname))
    #print("color name :" + str(color))
    db_connection = mysql.connector.connect(host="localhost", user="django", passwd="django-user-password", database="detectionnav")
    db_cursor = db_connection.cursor()
    db_cursor.execute("UPDATE mitrenv_techniques SET techColor='green' WHERE techniqueName = 'T1529 : System Shutdown/Reboot'")
    db_connection.commit()
    return techname

@register.filter(name='grey')
def grey(value):
    techname = value
    # color=str(arg)
    print("tech name : " + str(techname))
    #print("color name :" + str(color))
    db_connection = mysql.connector.connect(host="localhost", user="django", passwd="django-user-password", database="detectionnav")
    db_cursor = db_connection.cursor()
    db_cursor.execute("UPDATE mitrenv_techniques SET techColor='grey' WHERE techniqueName = 'T1529 : System Shutdown/Reboot'")
    db_connection.commit()
    return techname

@register.filter(name='white')
def white(value):
    techname = value
    #color=str(arg)
    print("tech name : " + str(techname))
    #print("color name :" + str(color))
    db_connection = mysql.connector.connect(host="localhost", user="django", passwd="django-user-password", database="detectionnav")
    db_cursor = db_connection.cursor()
    db_cursor.execute("UPDATE mitrenv_techniques SET techColor='white' WHERE techniqueName = 'T1529 : System Shutdown/Reboot'")
    db_connection.commit()
    return techname
'''
"""
# var sql = "UPDATE mitrenv_techniques SET techColor='Red' WHERE techniqueName = 'T1529 : System Shutdown/Reboot';"
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