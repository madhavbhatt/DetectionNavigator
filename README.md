# DetectionNavigator

This tool quickly helps build detection chart ( a.k.a. detection heatmap ).

More information can be found in this article : https://desi-jarvis.medium.com/detection-navigator-a97ffd4fbeff

#Version 2.0 - Beta 

**Web UI Credentials**

username : detectionchartadmin

password : detectionchartpassword1

You can change this form Django admin portal **https://IP:PORT/admin**

**SETUP**

Requires you to manually start apache and mysql when you start the container. 

$ docker pull desijarvis/detectionnavigator:v2.0

$ docker run -p 8443:443 -it desijarvis/detectionnavigator:v2.0          

root@containerID # service apache2 start                                

root@containerID # service mysql start

root@containerID # netstat -antp                                        ( Make sure both apache and mysql are running )

#Version 1.2  

Requires you to manually start apache and mysql when you start the container. 

$ docker pull desijarvis/detectionnavigator:v1.2

$ docker run -p 8443:443 -it desijarvis/detectionnavigator:v1.2          

root@containerID # service apache2 start

root@containerID # service mysql start

root@containerID # netstat -antp                                        ( Make sure both apache and mysql are running )
