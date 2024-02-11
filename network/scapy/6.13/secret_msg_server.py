from scapy.all import sniff, Packet, conf, Raw
from scapy.layers.inet import UDP
from scapy.layers.dns import DNS


def filter_emtpy(pkt: Packet):
    return UDP in pkt and Raw not in pkt and DNS not in pkt


seen = set()
chars = []


def print_char(pkt: Packet):
    global seen, chars
    if pkt[UDP].sport not in seen:
        seen.add(pkt[UDP].sport)
        chars.insert(pkt[UDP].sport, chr(pkt[UDP].dport))
        print("".join(chars), end="\r")
    else:
        seen = set()
        chars = []
        seen.add(pkt[UDP].sport)
        chars.insert(pkt[UDP].sport, chr(pkt[UDP].dport))
        print()


def main():
    sniff(
        lfilter=filter_emtpy,
        prn=print_char,
        iface=conf.loopback_name,
    )


if __name__ == "__main__":
    main()
