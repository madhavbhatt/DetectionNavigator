import sys
import socket
from datetime import datetime

target = "127.0.0.1"

f = open(target+'.txt','w')
print("-" * 50)
print("Scanning Target: " + target)
print("Scanning started at:" + str(datetime.now()))
print("-" * 50)
f.write("-" * 50)
f.write("\nScanning Target: " + target)
f.write("\nScanning started at:" + str(datetime.now())+ "\n")
f.write("-" * 50 + "\n")

try:
    for port in range(1,65535):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = s.connect_ex((target,port))
        if result ==0:
            print("Port {} is open".format(port))
            f.write("Port {} is open \n".format(port))
        s.close()
except KeyboardInterrupt:
    print("\n Exitting Program !!!!")
    sys.exit()
except socket.gaierror:
    print("\n Hostname Could Not Be Resolved !!!!")
    sys.exit()
except socket.error:
    print("\ Server not responding !!!!")
    sys.exit()

f.close()