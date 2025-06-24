import struct
import socket
import subprocess

class Ping:
    @staticmethod
    def host(host: str):
        request = subprocess.run(['ping', host, '-c 1', '-4', '-W 5'], capture_output=True)
        if "1 packets transmitted, 1 received" in request.stdout.decode().lower():
            return True
        return False

    @staticmethod
    def gateway():
        return Ping.host(Ping.getDefaultGateway())

    @staticmethod
    def getDefaultGateway():
        """Read the default gateway directly from /proc."""
        with open("/proc/net/route") as fh:
            for line in fh:
                fields = line.strip().split()
                if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                    # If not default route or not RTF_GATEWAY, skip it
                    continue

                return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))