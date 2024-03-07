import time
from scapy.all import sr1
from scapy.layers.inet import IP, ICMP

import sys


def round(num: float | str) -> str:
    if isinstance(num, float):
        return f"{num*1000:.3f} ms"
    return num  # type: ignore


def get_time(pkt, dst) -> tuple[list[str], str | None, bool]:
    times = []
    reply_from = None
    to_quit = False
    for _ in range(3):
        start = time.perf_counter()
        reply = sr1(pkt, verbose=0, timeout=1)
        end = time.perf_counter()
        if reply is not None:
            times.append(round(end - start))
            reply_from = reply.src
            if reply[ICMP].type == 0:
                to_quit = True
        else:
            times.append("*")

    return times, reply_from, to_quit


def traceroute(dst, max_ttl=30):
    pkt = IP(dst=dst, ttl=0) / ICMP()
    for ttl in range(1, max_ttl + 1):
        pkt[IP].ttl = ttl
        times, _from, to_quit = get_time(pkt, dst)
        print(f"{ttl}\t{times[0]:>15}{times[1]:>15}{times[2]:>15}", end="\t")
        print(_from)
        if to_quit:
            break


def main():
    traceroute(sys.argv[1])


if __name__ == "__main__":
    main()
