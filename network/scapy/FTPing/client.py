from scapy.layers.inet import IP, ICMP
from scapy.all import sr1, Raw, sniff, conf

DST = "172.23.112.1"


def send_pkt(data: bytes, type=8, id=0, seq=0):
    pkt = IP(dst=DST) / ICMP(type=type, id=id, seq=seq) / data
    while True:
        response = sr1(
            pkt,
            timeout=1,
        )
        if response is not None and response[Raw].load.startswith(b"ACK"):
            break
        else:
            response = sniff(
                lfilter=lambda pkt: ICMP in pkt and pkt[IP].src == DST,
                count=1,
                timeout=1,
            )
            if response is None or not response:
                continue
            if response is not None and response[0][Raw].load.startswith(b"ACK"):
                break

    response.show()


def main():
    id = 28
    count = 0

    with open("smth.txt") as file:
        while data := file.read(32):
            send_pkt(data.encode(), id=id, seq=count)
            count += 1

    send_pkt(bytes([0xC3, 0x28]), seq=count, id=id)


if __name__ == "__main__":
    main()
