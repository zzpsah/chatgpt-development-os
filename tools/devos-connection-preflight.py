#!/usr/bin/env python3
"""Bounded, read-only preflight diagnostics for DevOS connections."""
from __future__ import annotations
import argparse
import socket
import ssl
from urllib.parse import urlparse

LAYERS = ("CONFIGURATION", "CREDENTIAL_SHAPE", "ENDPOINT_DNS", "NETWORK_REACHABILITY", "TLS_TRANSPORT")


def diagnose(endpoint: str, credential_present: bool = False, timeout: float = 2.0) -> dict:
    parsed = urlparse(endpoint if "://" in endpoint else "tcp://" + endpoint)
    host = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    if not host:
        return {"status": "DIAGNOSED", "failed_layer": "CONFIGURATION", "evidence": "endpoint host missing"}
    if credential_present:
        credential_state = "PRESENT_SHAPE_ONLY"
    else:
        credential_state = "NOT_PROVIDED"
    try:
        infos = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        return {"status": "DIAGNOSED", "failed_layer": "ENDPOINT_DNS", "evidence": f"dns_error={type(exc).__name__}"}
    addresses = {item[4][0] for item in infos}
    try:
        with socket.create_connection((host, port), timeout=timeout):
            pass
    except OSError as exc:
        return {"status": "DIAGNOSED", "failed_layer": "NETWORK_REACHABILITY", "evidence": f"network_error={type(exc).__name__}", "credential_state": credential_state, "resolved_addresses": len(addresses)}
    if parsed.scheme == "https":
        context = ssl.create_default_context()
        try:
            with socket.create_connection((host, port), timeout=timeout) as raw:
                with context.wrap_socket(raw, server_hostname=host):
                    pass
        except (OSError, ssl.SSLError) as exc:
            return {"status": "DIAGNOSED", "failed_layer": "TLS_TRANSPORT", "evidence": f"tls_error={type(exc).__name__}", "credential_state": credential_state}
    return {"status": "PASS", "failed_layer": None, "credential_state": credential_state, "resolved_addresses": len(addresses)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("endpoint")
    parser.add_argument("--credential-present", action="store_true", help="record presence/shape only; never accepts or prints secret values")
    parser.add_argument("--timeout", type=float, default=2.0)
    args = parser.parse_args()
    if args.timeout <= 0:
        raise SystemExit("timeout must be positive")
    result = diagnose(args.endpoint, args.credential_present, args.timeout)
    print(f"status={result['status']}")
    print(f"failed_layer={result['failed_layer']}")
    for key in ("credential_state", "resolved_addresses", "evidence"):
        if key in result:
            print(f"{key}={result[key]}")


if __name__ == "__main__":
    main()
