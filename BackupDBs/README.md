Files starting with name "automatic-backup" are the files generated when Update Database OR Reset Databse function is used.

Files starting with name "manual-backup" are the files generated when Backup Databse function is used.

In case the database is corrupted while updating OR reseting it , you can simply login to docker container OR the virtual machine and restore the database from /var/www/DetectionNavigator/BackupDBs/ folder using following command.

$ mysql --one-database detectionnav < manual-backup-alldatabases-<%datetime%>.sql

OR 

$ mysql --one-database detectionnav < automatic-backup-alldatabases-<%datetime%>.sql
