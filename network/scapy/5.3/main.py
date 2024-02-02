from scapy.layers.inet import TCP
from scapy.all import Raw, Packet, sniff

HTTP_SPLITTER = b"\r\n"
HOST = "Host"


def http_filter(p):
    return TCP in p and Raw in p and p[Raw].load.startswith(b"GET")


def print_url(packet: Packet):
    pkt: bytes = packet[Raw].load
    headers, body = pkt.split(HTTP_SPLITTER * 2)
    start, *headers = headers.split(HTTP_SPLITTER)
    headers = dict(h.decode().split(": ") for h in headers)
    path = start.split(b" ")[1].decode()
    print(f"{headers[HOST]}{path}")


def main():
    sniff(lfilter=http_filter, prn=print_url)


if __name__ == "__main__":
    main()
