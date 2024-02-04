# snmp-agent
**SETTING UP ENVIRONMENT**



pip3 install psutil


brew install libsmi


**Starting my Agent in 1st Terminal:**

python3 d-snmp.py 

INFO:root:SNMP Agent listening on port 1161

DEBUG:root:Received data from ('127.0.0.1', 61826):


**Testing with Net-SNMP and using debugging(-d) option in 2nd Terminal:**

$ snmpget -v2c -c public -d 127.0.0.1:1161 1.3.6.1.4.1.2021.4.6.0

No log handling enabled - using stderr logging

**Starting tcpdump in 3rd Terminal:**

sudo tcpdump -i any port 1161 -vv

tcpdump: data link type PKTAP

