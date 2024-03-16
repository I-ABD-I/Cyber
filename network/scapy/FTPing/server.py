from scapy.all import sniff, send, Raw
from scapy.layers.inet import ICMP, IP

FILE = open("out.txt", "w")


def process_pkt(pkt):
    print(f"Received packet: {pkt.show()}")

    response = (
        IP(dst=pkt[IP].src) / ICMP(type=0, id=pkt[ICMP].id, seq=pkt[ICMP].seq) / "ACK"
    )

    send(response)

    if pkt[Raw].load == bytes([0xC3, 0x28]):
        exit(0)

    FILE.write(pkt[Raw].load.decode())


def main():
    sniff(
        lfilter=lambda pkt: ICMP in pkt and pkt[ICMP].type == 8,
        prn=process_pkt,
        iface="Hyper-V Virtual Ethernet Adapter",
    )


# if __name__ == "__main__":
main()
