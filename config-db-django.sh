#!/bin/bash
service mysql start
systemctl enable mysql
mysql -u "$MYSQL_ROOT" -e "CREATE DATABASE detectionnav"
mysql -u "$MYSQL_ROOT" -e "CREATE USER 'django'@'localhost' IDENTIFIED BY 'django-user-password'"
mysql -u "$MYSQL_ROOT" -e "GRANT ALL PRIVILEGES ON *.* TO 'django'@'localhost'"
mysql -u "$MYSQL_ROOT" -e "flush privileges"
python3 /var/www/DetectionNavigator/manage.py makemigrations
python3 /var/www/DetectionNavigator/manage.py makemigrations DetectionChart
python3 /var/www/DetectionNavigator/manage.py migrate
chown -R www-data /var/www/DetectionNavigator
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('detectionchartadmin', 'detectionchartadmin@example.com', 'detectionchartpassword1')" | python3 /var/www/DetectionNavigator/manage.py shell
