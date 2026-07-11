import ipaddress

from models import EventType, Hop, JourneyEvent


def detect_private_network_exit(
    hops: list[Hop],
) -> list[JourneyEvent]:

    events = []

    previous_public_state = None

    for hop in hops:

        if hop.responder_ip is None:
            continue

        is_private = ipaddress.ip_address(
            hop.responder_ip
        ).is_private

        if (
            previous_public_state is True
            and is_private is False
        ):
            events.append(
                JourneyEvent(
                    event_type=EventType.PRIVATE_NETWORK_EXIT,
                    message="Exited the private network.",
                    hop=hop.ttl,
                )
            )

        previous_public_state = is_private

    return events


def detect_asn_changes(
    hops: list[Hop],
) -> list[JourneyEvent]:

    events = []

    last_known_asn = None

    for hop in hops:

        if hop.asn is None:
            continue

        if hop.asn != last_known_asn:

            events.append(
                JourneyEvent(
                    event_type=EventType.ASN_CHANGE,
                    message=f"Entered {hop.organization}",
                    hop=hop.ttl,
                )
            )

            last_known_asn = hop.asn

    return events


def detect_destination(
    hops: list[Hop],
) -> list[JourneyEvent]:

    for hop in hops:

        if hop.icmp_type == 0:

            return [
                JourneyEvent(
                    event_type=EventType.DESTINATION,
                    message="Destination reached.",
                    hop=hop.ttl,
                )
            ]

    return []


def analyze_journey(
    hops: list[Hop],
) -> list[JourneyEvent]:

    events = []

    events.extend(
        detect_private_network_exit(hops)
    )

    events.extend(
        detect_asn_changes(hops)
    )

    events.extend(
        detect_destination(hops)
    )

    return events