from models import Probe
from probe import send_probe


def run_probe_batch(
    destination: str,
    max_ttl: int = 30,
    probes_per_ttl: int = 3,
) -> list[Probe]:
    """
    Runs a sequential traceroute.

    For each TTL:
      - Send `probes_per_ttl` probes.
      - Stop immediately if any probe reaches the destination.
    """

    probes: list[Probe] = []

    for ttl in range(1, max_ttl + 1):

        print(f"Discovering hop {ttl}...")

        destination_reached = False

        for probe_number in range(1, probes_per_ttl + 1):

            sequence = (
                (ttl - 1) * probes_per_ttl
            ) + probe_number

            probe = send_probe(
                destination=destination,
                ttl=ttl,
                sequence=sequence,
            )

            probes.append(probe)

            if probe.icmp_type == 0:
                destination_reached = True

        if destination_reached:
            break

    return probes