# snmp-agent
**SETTING UP ENVIRONMENT
**
darina@MacBook-Air:~$ mkdir appl
darina@MacBook-Air:~$ cd appl/
darina@MacBook-Air:~/appl$ mkdir project
darina@MacBook-Air:~/appl$ cd project/

darina@MacBook-Air:~/appl/project$ pip3 install pysnmp
darina@MacBook-Air:~/appl/project$ pip3 install psutil
darina@MacBook-Air:~/appl/project$ pip3 install pysnmp_mibs

darina@MacBook-Air:~/appl/project$ $ brew install libsmi

I have something I already made, I created a MIB file "~/appl/project$ vim MY-MIB.txt "
and then compiled it using "smidump -k -f python -o my-mib.py MY-MIB.txt" - works, then to implement the agent I ran "my_snmp-agent.py"
to run the python i used "python3 my_snmp-agent.py" but I get the following error when I open a second terminal : “~$ snmpget -v2c -c public 127.0.0.1 1.3.6.1.4.1.9999.1
Timeout: No Response from 127.0.0.1." 

**TROUBLESHOOTING**
IN 3-rd TERMINAL:
I see from tcpdump that there are GetRequest b/w 1-st and 2-nd Terminal, but maybe my snmp agent or snmpget  didn’t recognise custom 1.3.6.1.4.1.9999.1

darina@MacBook-Air:~$ sudo tcpdump -i any port 161 -vv
Password:
tcpdump: data link type PKTAP
tcpdump: listening on any, link-type PKTAP (Apple DLT_PKTAP), capture size 262144 bytes
22:51:22.000744 IP (tos 0x0, ttl 64, id 15327, offset 0, flags [none], proto UDP (17), length 71, bad cksum 0 (->40c5)!)
    localhost.55973 > localhost.snmp: [bad udp cksum 0xfe46 -> 0x8c3c!]  { SNMPv2c { GetRequest(28) R=984748106  E:9999.1 } } 
22:51:22.000763 IP (tos 0x0, ttl 64, id 15327, offset 0, flags [none], proto UDP (17), length 71, bad cksum 0 (->40c5)!)
    localhost.55973 > localhost.snmp: [bad udp cksum 0xfe46 -> 0x8c3c!]  { SNMPv2c { GetRequest(28) R=984748106  E:9999.1 } } 
22:51:23.004528 IP (tos 0x0, ttl 64, id 8039, offset 0, flags [none], proto UDP (17), length 71, bad cksum 0 (->5d3d)!)
    localhost.55973 > localhost.snmp: [bad udp cksum 0xfe46 -> 0x8c3c!]  { SNMPv2c { GetRequest(28) R=984748106  E:9999.1 } } 
22:51:23.004564 IP (tos 0x0, ttl 64, id 8039, offset 0, flags [none], proto UDP (17), length 71, bad cksum 0 (->5d3d)!)
    localhost.55973 > localhost.snmp: [bad udp cksum 0xfe46 -> 0x8c3c!]  { SNMPv2c { GetRequest(28) R=984748106  E:9999.1 } } 
22:51:24.009322 IP (tos 0x0, ttl 64, id 58999, offset 0, flags [none], proto UDP (17), length 71, bad cksum 0 (->962c)!)
    localhost.55973 > localhost.snmp: [bad udp cksum 0xfe46 -> 0x8c3c!]  { SNMPv2c { GetRequest(28) R=984748106  E:9999.1 } } 
…



Or starting snmpget with -d option

darina@MacBook-Air:~$ snmpget -v2c -c public -d 127.0.0.1 1.3.6.1.4.1.9999.1
No log handling enabled - using stderr logging

Sending 43 bytes to UDP: [127.0.0.1]:161->[0.0.0.0]:0
0000: 30 29 02 01  01 04 06 70  75 62 6C 69  63 A0 1C 02    0).....public?..
0016: 04 4B 27 7B  6F 02 01 00  02 01 00 30  0E 30 0C 06    .K'{o......0.0..
0032: 08 2B 06 01  04 01 CE 0F  01 05 00                    .+....?....


Sending 43 bytes to UDP: [127.0.0.1]:161->[0.0.0.0]:0
0000: 30 29 02 01  01 04 06 70  75 62 6C 69  63 A0 1C 02    0).....public?..
0016: 04 4B 27 7B  6F 02 01 00  02 01 00 30  0E 30 0C 06    .K'{o......0.0..
0032: 08 2B 06 01  04 01 CE 0F  01 05 00                    .+....?....


Sending 43 bytes to UDP: [127.0.0.1]:161->[0.0.0.0]:0
0000: 30 29 02 01  01 04 06 70  75 62 6C 69  63 A0 1C 02    0).....public?..
0016: 04 4B 27 7B  6F 02 01 00  02 01 00 30  0E 30 0C 06    .K'{o......0.0..
0032: 08 2B 06 01  04 01 CE 0F  01 05 00                    .+....?....


Sending 43 bytes to UDP: [127.0.0.1]:161->[0.0.0.0]:0
0000: 30 29 02 01  01 04 06 70  75 62 6C 69  63 A0 1C 02    0).....public?..
0016: 04 4B 27 7B  6F 02 01 00  02 01 00 30  0E 30 0C 06    .K'{o......0.0..
0032: 08 2B 06 01  04 01 CE 0F  01 05 00                    .+....?....


Sending 43 bytes to UDP: [127.0.0.1]:161->[0.0.0.0]:0
0000: 30 29 02 01  01 04 06 70  75 62 6C 69  63 A0 1C 02    0).....public?..
0016: 04 4B 27 7B  6F 02 01 00  02 01 00 30  0E 30 0C 06    .K'{o......0.0..
0032: 08 2B 06 01  04 01 CE 0F  01 05 00                    .+....?....


Sending 43 bytes to UDP: [127.0.0.1]:161->[0.0.0.0]:0
0000: 30 29 02 01  01 04 06 70  75 62 6C 69  63 A0 1C 02    0).....public?..
0016: 04 4B 27 7B  6F 02 01 00  02 01 00 30  0E 30 0C 06    .K'{o......0.0..
0032: 08 2B 06 01  04 01 CE 0F  01 05 00                    .+....?....

**Timeout: No Response from 127.0.0.1.
**
