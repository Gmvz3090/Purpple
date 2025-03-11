# tls_scanner_python.py (or wherever your function is)

import socket
import ssl
from datetime import datetime

def get_certificate_info(hostname: str, port: int = 443) -> dict:
    """
    Connects via TLS to hostname:port using Python's ssl/socket.
    Returns a dict with either cert info or an "error" key.
    """
    context = ssl.create_default_context()
    results = {}

    try:
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as tls:
                cert_dict = tls.getpeercert()
                cipher_tuple = tls.cipher()  # (cipher_name, proto_version, bits)

                subject = dict(item[0] for item in cert_dict["subject"])
                issuer = dict(item[0] for item in cert_dict["issuer"])

                not_before_str = cert_dict["notBefore"]
                not_after_str = cert_dict["notAfter"]
                fmt = "%b %d %H:%M:%S %Y %Z"
                not_before = datetime.strptime(not_before_str, fmt)
                not_after = datetime.strptime(not_after_str, fmt)

                results["subject_common_name"] = subject.get("commonName")
                results["issuer_common_name"] = issuer.get("commonName")
                results["valid_from"] = not_before
                results["valid_to"] = not_after
                results["cipher"] = cipher_tuple[0]
                results["protocol"] = cipher_tuple[1]

        return results  # <-- Always return dict here

    except Exception as e:
        # Return a dictionary with an "error" key instead of None
        return {"error": str(e)}
