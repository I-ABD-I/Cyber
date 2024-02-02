from scapy.all import sniff, Packet, conf, Raw
from scapy.layers.inet import UDP


def filter_emtpy(pkt: Packet):
    return UDP in pkt and Raw not in pkt


chars = []


def print_char(pkt: Packet):
    chars.insert(pkt[UDP].sport, chr(pkt[UDP].dport))
    print("".join(chars), end="\r")


def main():
    sniff(
        lfilter=filter_emtpy,
        prn=print_char,
        iface=conf.loopback_name,
    )


if __name__ == "__main__":
    main()
