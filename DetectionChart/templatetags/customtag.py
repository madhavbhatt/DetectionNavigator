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

