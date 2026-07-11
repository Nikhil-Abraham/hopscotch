import os
import time

from scapy.all import ICMP, IP, sr1

from models import Probe


ICMP_IDENTIFIER = os.getpid() & 0xFFFF


def send_probe(
    destination: str,
    ttl: int,
    sequence: int,
    timeout: float = 1.0,
) -> Probe:
    """
    Sends a single ICMP Echo Request.

    Returns a Probe containing the result.
    """

    packet = (
        IP(dst=destination, ttl=ttl)
        / ICMP(
            id=ICMP_IDENTIFIER,
            seq=sequence,
        )
    )

    start = time.perf_counter()

    try:
        reply = sr1(
            packet,
            timeout=timeout,
            verbose=False,
        )

    except Exception:
        return Probe(
            ttl=ttl,
            sequence=sequence,
            responder_ip=None,
            rtt_ms=None,
            icmp_type=None,
            success=False,
        )

    end = time.perf_counter()

    if reply is None:
        return Probe(
            ttl=ttl,
            sequence=sequence,
            responder_ip=None,
            rtt_ms=None,
            icmp_type=None,
            success=False,
        )

    icmp = reply.getlayer(ICMP)

    return Probe(
        ttl=ttl,
        sequence=sequence,
        responder_ip=reply.src,
        rtt_ms=(end - start) * 1000,
        icmp_type=icmp.type if icmp else None,
        success=True,
    )