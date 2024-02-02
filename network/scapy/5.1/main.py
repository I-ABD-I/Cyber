import sys

from scapy.all import sniff


def filter_dns(packet):
    return "DNS" in packet


packets = sniff(count=4, lfilter=filter_dns)
packets.summary()

packet = packets[1]
packet.show()
