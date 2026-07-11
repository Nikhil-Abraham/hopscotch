import time

from scapy.all import ICMP, IP, sr1

from models import Hop

ICMP_ECHO_REPLY = 0
ICMP_TIME_EXCEEDED = 11


def trace(destination: str) -> list[Hop]:

    hops = []

    for ttl in range(1, 31):

        print(f"Discovering hop {ttl}...")

        hop = discover_hop(destination, ttl)

        if hop is None:
            continue

        hops.append(hop)

        if hop.icmp_type == ICMP_ECHO_REPLY:
            break

    return hops


def discover_hop(destination: str, ttl: int) -> Hop | None:
    """
    Sends one ICMP Echo Request with a given TTL.

    Returns:
        Hop if a device replied.
        None if no reply was received.
    """

    packet = IP(
        dst=destination,
        ttl=ttl,
    ) / ICMP()

    start = time.perf_counter()

    reply = sr1(
        packet,
        timeout=1,
        verbose=False,
    )

    end = time.perf_counter()

    if reply is None:
        return None

    return Hop(
        ttl=ttl,
        responder_ip=reply.src,
        rtt_ms=(end - start) * 1000,
        icmp_type=reply.getlayer(ICMP).type,
    )