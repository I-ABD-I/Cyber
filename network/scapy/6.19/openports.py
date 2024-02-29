from scapy.layers.inet import IP, TCP
from scapy.all import sr1, conf

DEST = "127.0.0.1"


def test(port):
    pkt = IP(dst=DEST) / TCP(dport=port, seq=123, flags="S")
    ret = sr1(pkt, timeout=1, verbose=0, iface=conf.loopback_name)
    if ret is not None and ret[TCP].flags == "SA":
        print(f"Port {port} is open")
    else:
        print(f"Port {port} is closed")


for port in range(1, 1025):
    test(port)
