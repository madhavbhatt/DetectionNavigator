mysql -u "$MYSQL_ROOT" -e "CREATE DATABASE testattnv"
mysql -u "$MYSQL_ROOT" -e "CREATE USER 'django'@'localhost' IDENTIFIED BY 'django-user-password'"
mysql -u "$MYSQL_ROOT" -e "GRANT ALL PRIVILEGES ON testattnv.* TO 'django'@'localhost'"
mysql -u "$MYSQL_ROOT" -e "flush privileges"
