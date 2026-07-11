import socket


def reverse_dns(ip: str) -> str | None:

    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname

    except socket.herror:
        return None