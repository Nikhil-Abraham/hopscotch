from dns_lookup import reverse_dns
from geoip import enrich_asn, enrich_location
from models import Hop


def enrich_ptr(hop: Hop):
    if hop.responder_ip is None:
        return

    hop.hostname = reverse_dns(
        hop.responder_ip
    )


def enrich_hop(hop: Hop):

    if hop.responder_ip is None:
        return

    enrich_ptr(hop)

    enrich_asn(hop)

    enrich_location(hop)