"""A dependency free SNMP Agent.

Run as main to run a server.

Inputs:
$1: port

This code uses delimitry/snmp-server as a dependency imported by the name of
srv.
"""
import socket
import logging
import psutil
from srv import craft_response, _read_int_len


logging.basicConfig(level=logging.DEBUG)

DEFAULT_PORT = 1161


class SNMPAgent:
    """An SNMP agent.

    Consult ``listen`` and ``listen_thread`` for running the server.
    OIDs are managed with ``get_value`` function.
    """

    @classmethod
    def listen(cls, port=None):
        """Run the server."""
        if port is None:
            port = DEFAULT_PORT

        # Create the server and keep on listening
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            server_socket.bind(("127.0.0.1", port))
            logging.info(f"SNMP Agent listening on port {port}")

            while True:
                data, addr = server_socket.recvfrom(4096)
                logging.debug(f"Received data from {addr}: {data}")
                logging.debug(f"Hex data: {data.hex()}")

                if True:
                    # try:
                    (
                        version,
                        community,
                        pdu_type,
                        oid,
                        oid_bytes,
                        request_id,
                    ) = cls.parse_snmp_packet(data)
                    version_name = cls.get_snmp_version_name(version)
                    logging.debug(
                        f"Decoded SNMP Request: Version={version_name},"
                        f" Community={community}, PDU Type={pdu_type},"
                        f" OID={oid}"
                    )

                    try:
                        value = cls.get_value(oid)
                    except KeyError as e:
                        value = str(e)

                    response_str = f"Response for {oid}: {value}".encode()

                    response_bytes = (
                        b"\x04"
                        + bytes(bytearray([len(response_str)]))
                        + response_str
                    )

                    response_packet = craft_response(
                        version,
                        community,
                        request_id,
                        error_status=0,  # always 0 in RFC1157 (4.1.2)
                        error_index=0,
                        oid_items=[("TODO", response_bytes)],
                    )

                    server_socket.sendto(response_packet, addr)

                    logging.debug(
                        f"Encoded SNMP Response for OID {oid}: {value}"
                    )
                # except Exception as e:
                #     logging.error(f"Error processing packet: {e}")

    @classmethod
    def parse_snmp_packet(cls, packet):
        # The first INTEGER is the version
        version = packet[3]

        # The first string is the community (NOTE is the process below okay?)
        community_end_index = packet.find(b"\xa0")
        community = packet[6:community_end_index].decode("utf-8")
        pdu_type = format(packet[community_end_index], "02x")

        # The REQUEST ID is the next integer (\x02).
        length_index = (
            packet[community_end_index:].find(b"\x02")
            + community_end_index
            + 1
        )

        length = packet[length_index]
        try:
            from StringIO import StringIO
        except ImportError:
            from io import StringIO

        request_id_bytes = packet[
            length_index + 1 : length_index + 1 + length * 8
        ]

        # request_id_bytes is a valid integer which must be converted to SNMP
        # compatible, since delimitry's code is used I'll just simply use
        # his methods
        request_id = _read_int_len(
            StringIO(request_id_bytes.decode("latin")), length
        )

        oid_start_index = packet.find(b"\x06", community_end_index) + 2
        oid_length = packet[oid_start_index - 1]
        oid_bytes = packet[oid_start_index : oid_start_index + oid_length]

        logging.debug(f"oid_bytes: {oid_bytes.hex()}")

        oid = cls.decode_oid(oid_bytes)

        return version, community, pdu_type, oid, oid_bytes, request_id

    @staticmethod
    def decode_oid(oid_bytes):
        oid = []
        index = 0

        if oid_bytes:
            first_byte = oid_bytes[0]
            oid.append(1)  # the 1-st part of OID is always 1
            oid.append(
                first_byte - 40
            )  # subtract 40 from the 1-st byte to get the 2-nd part of OID
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
        return ".".join(str(num) for num in oid)

    @staticmethod
    def get_snmp_version_name(version):
        """Convert SNMP version to its name."""
        if version == 0:
            return "(SNMPv1)"
        elif version == 1:
            return "(SNMPv2c)"
        elif version == 3:
            return "(SNMPv3)"
        else:
            return "Unknown"

    @staticmethod
    def get_value(oid):
        """Return the value in response to the OID.

        Raises:
            KeyError: If the OID is not known to the system.

        Returns:
            str
        """
        if oid == "1.3.6.1.4.1.2021.4.6.0":
            return str(psutil.virtual_memory().available)
        elif oid == "1.3.6.1.4.1.2021.11.10.0":
            return str(psutil.cpu_times_percent().system)
        elif oid in [
            "1.3.6.1.4.1.2021.9.1.7.1",
            "1.3.6.1.4.1.9999.3",
        ]:
            try:
                return str(psutil.disk_usage("/").free)
            except FileNotFoundError:
                return "0"
        elif oid == "1.3.6.1.4.1.9999.1":
            return str(psutil.virtual_memory().available)
        elif oid == "1.3.6.1.4.1.9999.2":
            return str(psutil.cpu_times_percent().system)

        raise KeyError("Unknown OID")


if __name__ == "__main__":
    from sys import argv

    port = None if len(argv) < 2 else argv[1]
    SNMPAgent.listen(port)
