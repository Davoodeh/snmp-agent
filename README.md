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
