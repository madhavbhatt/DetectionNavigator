# If you decide to not use docker OR ova file option , you can use this script. It has been tested on ubuntu 20.04 image.

#!/bin/bash

apt-get update
apt-get install -y apt-utils vim curl apache2 apache2-utils 
apt-get -y install python3 libapache2-mod-wsgi-py3  
apt-get -y install python3-pip 
apt-get install python3-mysqldb -y
apt-get install mysql-server -y
apt-get install mysql-client -y
apt-get install net-tools -y
apt-get install systemctl -y

pip3 install -r requirements.txt

mkdir /var/www/DetectionNavigator
mkdir /etc/apache2/ssl
cp -r * /var/www/DetectionNavigator/
cp 000-default.conf /etc/apache2/sites-available/000-default.conf
cp default-ssl.conf /etc/apache2/sites-available/default-ssl.conf
cp server.key /etc/apache2/ssl/server.key
cp server.crt /etc/apache2/ssl/server.crt

chmod +x config-db-django.sh # configure mysql database for Django
chown -R www-data /var/www/DetectionNavigator # allows downloading detection chart to excel

sh config-db-django.sh

a2enmod ssl
a2ensite default-ssl.conf
systemctl restart apache2

echo "Please manually run config-db-django.sh if you get a mysql error"

