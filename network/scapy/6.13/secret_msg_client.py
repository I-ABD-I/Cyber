from scapy.layers.inet import UDP, IP
from scapy.all import send

IP_ADDR = "127.0.0.1"
id = 0


def main():
    global id
    msg = input("Please enter a msg to send: ")
    for c in msg:
        pkt = IP(dst=IP_ADDR) / UDP(sport=id, dport=ord(c))
        id += 1
        send(pkt)


if __name__ == "__main__":
    main()
