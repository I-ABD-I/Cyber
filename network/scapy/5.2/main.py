from scapy.all import *  # type: ignore
from scapy.layers.inet import *  # type: ignore


def http_get_filter(packet: Packet):
    return TCP in packet and Raw in packet and packet[Raw].load.startswith(b"GET")


if __name__ == "__main__":
    packets = sniff(count=5, lfilter=http_get_filter, prn=lambda x: x.show())
