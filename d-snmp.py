import socket
import struct
import threading
import logging
import psutil

logging.basicConfig(level=logging.DEBUG)

class SNMPAgent:
    def __init__(self, port=1161):
        self.port = port

    def start(self):
        threading.Thread(target=self.listen).start()

    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            server_socket.bind(('127.0.0.1', self.port))
            logging.info(f'SNMP Agent listening on port {self.port}')

            while True:
                data, addr = server_socket.recvfrom(4096)
                logging.debug(f"Received data from {addr}: {data}")
                logging.debug(f"Hex data: {data.hex()}")

                try:
                    version, community, pdu_type, oid = self.parse_snmp_packet(data)
                    version_name = self.get_snmp_version_name(version)
                    logging.debug(f"Decoded SNMP Request: Version={version_name}, Community={community}, PDU Type={pdu_type}, OID={oid}")

                    value = self.get_system_info(oid)
                    response_packet = self.create_snmp_response(oid, value)
                    server_socket.sendto(response_packet, addr)
                    logging.debug(f"Encoded SNMP Response for OID {oid}: {value}")
                except Exception as e:
                    logging.error(f"Error processing packet: {e}")

    def parse_snmp_packet(self, packet):
        version = packet[3]  

        community_end_index = packet.find(b'\xa0') 
        community = packet[6:community_end_index].decode('utf-8')
        pdu_type = format(packet[community_end_index], '02x')

        oid_start_index = packet.find(b'\x06', community_end_index) + 2
        oid_length = packet[oid_start_index - 1]
        oid_bytes = packet[oid_start_index:oid_start_index + oid_length]

        logging.debug(f"oid_bytes: {oid_bytes.hex()}")

        oid = self.decode_oid(oid_bytes)
        
        return version, community, pdu_type, oid

    def decode_oid(self, oid_bytes):
        oid = [] 
        index = 0

        if oid_bytes:
            first_byte = oid_bytes[0]
            oid.append(1)  # the 1-st part of OID is always 1
            oid.append(first_byte - 40)  # subtract 40 from the 1-st byte to get the 2-nd part of OID
            index += 1
        
        while index < len(oid_bytes):
            byte = oid_bytes[index]
            if byte >= 128:
            
                next_byte = 0
                while byte >= 128:
                    next_byte = (next_byte << 7) | (byte & 0x7F)
                    index += 1
                    byte = oid_bytes[index]
                next_byte = (next_byte << 7) | byte
                oid.append(next_byte)
            else:
                oid.append(byte)
            index += 1

        # OID as string
        return '.'.join(str(num) for num in oid)

    def get_snmp_version_name(self, version):
        if version == 0:
            return "(SNMPv1)"
        elif version == 1:
            return "(SNMPv2c)"
        elif version == 3:
            return "(SNMPv3)"
        else:
            return "Unknown"

    def get_system_info(self, oid):
        if oid == "1.3.6.1.4.1.2021.4.6.0": # OID memory utilization
            mem = psutil.virtual_memory()
            return str(mem.available)
        elif oid == "1.3.6.1.4.1.2021.11.10.0": # OID cpu utilization
            cpu_times = psutil.cpu_times_percent()
            return str(cpu_times.system)
        elif oid == "1.3.6.1.4.1.2021.9.1.7.1": # OID disk utilization
            partitions = psutil.disk_partitions()
            for p in partitions:
                if p.mountpoint == '/':
                    usage = psutil.disk_usage(p.mountpoint)
                    return str(usage.free)
            return "0"  # Default to 0 if '/' partition not found
        elif oid == "1.3.6.1.4.1.9999.1": # custom OID memory utilization
            mem = psutil.virtual_memory()
            return str(mem.available)
        elif oid == "1.3.6.1.4.1.9999.2": # custom OID cpu utilization
            cpu_times = psutil.cpu_times_percent()
            return str(cpu_times.system)
            return str(cpu_times)
        elif oid == "1.3.6.1.4.1.9999.3": # custom OID disk utilization
            partitions = psutil.disk_partitions()
            for p in partitions:
                if p.mountpoint == '/':
                    usage = psutil.disk_usage(p.mountpoint)
                    return str(usage.free)
            return "0"  # Default to 0 if '/' partition not found
        else:
            return "Unknown OID"

    def create_snmp_response(self, oid, value):
        return f"Response for {oid}: {value}".encode()

if __name__ == "__main__":
    agent = SNMPAgent()
    agent.start()

