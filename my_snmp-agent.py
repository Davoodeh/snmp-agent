from pysnmp.hlapi import *
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdrsp, context
from pysnmp import debug
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.smi import instrum, builder
from pysnmp.proto.api import v2c
import psutil
from pysnmp.smi import exval

# Create SNMP engine
snmpEngine = engine.SnmpEngine()

# Custom OIDs from MY-MIB
CPU_OID = '1.3.6.1.4.1.9999.2'  # MY-MIB::cpuUtil
MEMORY_OID = '1.3.6.1.4.1.9999.1'  # MY-MIB::memoryUtil
DISK_OID = '1.3.6.1.4.1.9999.3'  # MY-MIB::diskUtil

def get_cpu_usage():
    """ CPU usage percentage """
    return int(psutil.cpu_percent(interval=1))

def get_memory_usage():
    """ Memory usage percentage """
    memory = psutil.virtual_memory()
    return int(memory.used * 100 / memory.total)

def get_disk_usage():
    """ Disk usage percentage: main partition """
    disk = psutil.disk_usage('/')
    return int(disk.used * 100 / disk.total)

def create_variable_binds(oid, value):
    return [ObjectType(ObjectIdentity(oid), Integer32(value))]

def create_snmp_agent():
    """ an SNMP agent listening for GET requests """
    
    def process_snmp_request(snmpEngine, stateReference, contextEngineId, contextName, varBinds, cbCtx):
        """ Processing SNMP GET requests """
        oid, = [x[0] for x in varBinds]
        oid_str = str(oid)
    
        print("Received request for OID:", oid_str)
    
        # Using appropriate response based on the OID
        if oid_str.startswith(CPU_OID):
            value = get_cpu_usage()
        elif oid_str.startswith(MEMORY_OID):
            value = get_memory_usage()
        elif oid_str.startswith(DISK_OID):
            value = get_disk_usage()
        else:
            value = 0  # Default response for unrecognized OIDs

        # Creating and sending the response
        varBinds = create_variable_binds(oid, value)
        cmdrsp.sendVarBinds(snmpEngine, stateReference, contextEngineId, contextName, varBinds, cbCtx)

    # Registering SNMP application
    cmdrsp.GetCommandResponder(snmpEngine, CommunityData('public', mpModel=1))

    # Processing SNMP GET requests
    snmpContext = context.SnmpContext(snmpEngine)
    snmpContext.registerContextName(v2c.OctetString('public'), process_snmp_request)
    # Transport (UDP over IPv4)
    config.addTransport(snmpEngine, udp.domainName, udp.UdpTransport().openServerMode(('0.0.0.0', 161)))

    print("SNMP Agent is running...")
    snmpEngine.transportDispatcher.jobStarted(1)

    try:
        # Start dispatcher for receiving queries and sending responses
        snmpEngine.transportDispatcher.runDispatcher()
    except:
        snmpEngine.transportDispatcher.closeDispatcher()
        raise

if __name__ == "__main__":
    create_snmp_agent()
