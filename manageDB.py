import mysql.connector
from backupdb import *


def flushDB():
    backupDataBase()
    db_connection = mysql.connector.connect(host="localhost", user="django", passwd="django-user-password", database="detectionnav")
    db_cursor = db_connection.cursor()
    db_cursor.execute('DELETE FROM DetectionChart_techniques')
    db_cursor.execute('DELETE FROM DetectionChart_ttp')
    db_cursor.execute('DELETE FROM DetectionChart_tactic')
    db_connection.commit()
