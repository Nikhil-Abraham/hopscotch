from dataclasses import dataclass, field
from enum import Enum
from collections import Counter


class EventType(Enum):
    PRIVATE_NETWORK_EXIT = "PRIVATE_NETWORK_EXIT"
    ASN_CHANGE = "ASN_CHANGE"
    DESTINATION = "DESTINATION"


@dataclass
class Probe:
    """
    Represents the result of sending one probe.
    """

    ttl: int
    sequence: int

    responder_ip: str | None
    rtt_ms: float | None
    icmp_type: int | None

    success: bool


@dataclass
class GeoInfo:
    """
    Geographic information inferred for a hop.
    """

    country: str | None = None
    city: str | None = None

    latitude: float | None = None
    longitude: float | None = None

    confidence: float = 0.0
    source: str | None = None


@dataclass
class Hop:
    """
    Represents one hop in the network path.
    """

    ttl: int

    probes: list[Probe] = field(default_factory=list)

    hostname: str | None = None

    asn: str | None = None
    organization: str | None = None

    geo: GeoInfo = field(default_factory=GeoInfo)

    @property
    def responder_ip(self) -> str | None:
        """
        Returns the most common responding IP.
        """

        responders = [
            probe.responder_ip
            for probe in self.probes
            if probe.success and probe.responder_ip is not None
        ]

        if not responders:
            return None

        return Counter(responders).most_common(1)[0][0]

    @property
    def rtt_ms(self) -> float | None:
        values = [
            probe.rtt_ms
            for probe in self.probes
            if probe.rtt_ms is not None
        ]

        if not values:
            return None

        return sum(values) / len(values)

    @property
    def icmp_type(self) -> int | None:
        for probe in self.probes:
            if probe.success:
                return probe.icmp_type
        return None

    @property
    def packet_loss(self) -> float:
        if not self.probes:
            return 100.0

        lost = sum(not probe.success for probe in self.probes)

        return (lost / len(self.probes)) * 100
    
    @property
    def min_rtt_ms(self) -> float | None:
        values = [
            probe.rtt_ms
            for probe in self.probes
            if probe.rtt_ms is not None
        ]

        return min(values) if values else None


    @property
    def max_rtt_ms(self) -> float | None:
        values = [
            probe.rtt_ms
            for probe in self.probes
            if probe.rtt_ms is not None
        ]

        return max(values) if values else None


    @property
    def jitter_ms(self) -> float | None:
        """
        Difference between the fastest and slowest successful probe.
        """

        if (
            self.min_rtt_ms is None
            or self.max_rtt_ms is None
        ):
            return None

        return self.max_rtt_ms - self.min_rtt_ms
    


@dataclass
class JourneyEvent:
    """
    High-level event inferred from the journey.
    """

    event_type: EventType
    message: str
    hop: int