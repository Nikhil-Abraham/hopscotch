import socket

from analyzer import build_hops
from analysis import analyze_journey
from engine import run_probe_batch
from enrichment import enrich_hop
from formatter import print_events, print_hop


def main():

    host = input("Enter hostname: ")

    destination = socket.gethostbyname(host)

    probes = run_probe_batch(
        destination,
        max_ttl=16,
        probes_per_ttl=3,
    )

    hops = build_hops(probes)

    for hop in hops:
        enrich_hop(hop)

    events = analyze_journey(hops)

    print("\n")
    print("=" * 50)
    print("Journey")
    print("=" * 50)

    for hop in hops:
        print_hop(hop)

    print_events(events)


if __name__ == "__main__":
    main()