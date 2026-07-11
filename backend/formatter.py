from models import Hop, JourneyEvent


def _value(value):
    return value if value is not None else "-"


def print_hop(hop: Hop) -> None:
    print(f"\nHop {hop.ttl}")
    print("─" * 50)

    print(f"IP           : {_value(hop.responder_ip)}")
    print(f"Hostname     : {_value(hop.hostname)}")

    print(f"ASN          : {_value(hop.asn)}")
    print(f"Provider     : {_value(hop.organization)}")

    location = "-"

    if hop.geo.city and hop.geo.country:
        location = f"{hop.geo.city}, {hop.geo.country}"
    elif hop.geo.country:
        location = hop.geo.country

    print(f"Location     : {location}")

    if hop.rtt_ms is not None:
        print(f"RTT Avg      : {hop.rtt_ms:.2f} ms")
        print(f"RTT Min      : {hop.min_rtt_ms:.2f} ms")
        print(f"RTT Max      : {hop.max_rtt_ms:.2f} ms")

        if hop.jitter_ms is not None:
            print(f"Jitter       : {hop.jitter_ms:.2f} ms")

    else:
        print("RTT          : -")

    print(f"Packet Loss  : {hop.packet_loss:.0f}%")
    print(f"ICMP Type    : {_value(hop.icmp_type)}")


def print_events(events: list[JourneyEvent]) -> None:

    print("\n")
    print("=" * 50)
    print("Journey Events")
    print("=" * 50)

    for event in events:
        print(f"[Hop {event.hop}] {event.message}")