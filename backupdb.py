import os
import datetime

'''
To restore this database use following command. Date and time stamp will give you latest backup. 

mysql --one-database detectionnav < backup-alldatabases-<%datetime%>.sql
'''


def backupDataBase():
    now = datetime.datetime.now()
    filename = '/var/www/DetectionNavigator/BackupDBs/backup-alldatabases-' + now.strftime('%Y-%m-%d--%H:%M:%S') + '.sql'
    if not os.path.exists('/var/www/DetectionNavigator/BackupDBs'):
        os.makedirs('/var/www/DetectionNavigator/BackupDBs')
    os.popen('mysqldump -u root -proot --all-databases > ' + filename).read()

