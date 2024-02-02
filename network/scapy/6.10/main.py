from scapy.layers.inet import UDP, IP
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.all import send, sr1

import sys


def main():
    qr = sys.argv[1]
    dns_pkt = (
        IP(dst="8.8.8.8")
        / UDP(sport=24000, dport=53)
        / DNS(qdcount=1, qd=DNSQR(qname=qr))
    )
    # dns_pkt.show()
    resp = sr1(dns_pkt, verbose=0)

    for i in range(resp[DNS].ancount):
        rr = resp[DNS].an[i]
        if rr.type == 1:
            print(rr.rdata)


if __name__ == "__main__":
    main()
