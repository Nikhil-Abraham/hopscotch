from pathlib import Path

import geoip2.database

from models import Hop


DATA_DIR = Path(__file__).parent / "data"

CITY_DB = geoip2.database.Reader(DATA_DIR / "GeoLite2-City.mmdb")
ASN_DB = geoip2.database.Reader(DATA_DIR / "GeoLite2-ASN.mmdb")


def enrich_location(hop: Hop):
    if hop.responder_ip is None:
        return

    try:
        result = CITY_DB.city(hop.responder_ip)

        hop.geo.country = result.country.name
        hop.geo.city = result.city.name
        hop.geo.latitude = result.location.latitude
        hop.geo.longitude = result.location.longitude
        hop.geo.confidence = 0.4
        hop.geo.source = "GeoLite2"

    except Exception:
        pass


def enrich_asn(hop: Hop):
    if hop.responder_ip is None:
        return

    try:
        result = ASN_DB.asn(hop.responder_ip)

        hop.asn = str(result.autonomous_system_number)
        hop.organization = (
            result.autonomous_system_organization
        )

    except Exception:
        pass