from collections import defaultdict

from models import Hop, Probe


def build_hops(
    probes: list[Probe],
) -> list[Hop]:
    """
    Groups probes by TTL and builds Hop objects.
    """

    grouped = defaultdict(list)

    for probe in probes:
        grouped[probe.ttl].append(probe)

    hops = []

    for ttl in sorted(grouped):

        hop = Hop(
            ttl=ttl,
            probes=grouped[ttl],
        )

        hops.append(hop)

    return hops