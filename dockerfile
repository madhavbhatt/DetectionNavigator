FROM ubuntu:latest
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y apt-utils vim curl apache2 apache2-utils 
RUN apt-get -y install python3 libapache2-mod-wsgi-py3  
RUN apt-get -y install python3-pip 
RUN apt-get install python3-mysqldb -y
RUN apt-get install mysql-server -y
RUN apt-get install mysql-client -y
RUN apt-get install net-tools -y
RUN mkdir /var/www/DetectionNavigator
RUN mkdir /etc/apache2/ssl

ADD ./000-default.conf /etc/apache2/sites-available/000-default.conf 
ADD ./default-ssl.conf /etc/apache2/sites-available/default-ssl.conf
ADD ./server.key /etc/apache2/ssl/server.key
ADD ./server.crt /etc/apache2/ssl/server.crt
ADD ./requirements.txt /var/www/DetectionNavigator

WORKDIR /var/www/DetectionNavigator
RUN pip3 install -r requirements.txt 
ADD ./config-db-django.sh /root
CMD chmod +x /root/config-db-django.sh
RUN a2enmod ssl
RUN a2ensite default-ssl.conf

EXPOSE 80 443 
CMD ["apache2ctl", "-D", "FOREGROUND"]

