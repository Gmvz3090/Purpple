import subprocess

SKIP_KEYWORDS = [
    "notice",
    "abuse",
    "privacy",
    ">>>",
    "wdprs.internic",
    "icann.org",
    "tieredaccess.com",
    "terms of use",
    "redacted",
    "inaccuracy complaint form",
    "purposes and that, under no circumstances will you use this data to: (1)",
    "to: (1) allow, enable, or otherwise support the transmission of mass"
]

def clean_whois_line(line: str) -> str:
    """
    Optional custom transformations on certain lines.
    e.g., removing extra data from 'Domain Status:' lines.
    """
    if line.startswith("Domain Status:") and "clientTransferProhibited" in line:
        # Example transformation: remove everything after "clientTransferProhibited"
        idx = line.find("clientTransferProhibited")
        if idx != -1:
            space_idx = line.find(" ", idx)
            if space_idx != -1:
                line = line[:space_idx]
            else:
                line = line[:idx + len("clientTransferProhibited")]
    return line

def whois_lookup_windows(domain: str) -> str:
    """
    Runs 'whois.exe {domain}' on Windows and returns a filtered WHOIS output:
      1) Only lines containing a colon (':')
      2) No lines with SKIP_KEYWORDS (disclaimers, references to abuse/privacy, etc.)
      3) Removes duplicates and empty lines
      4) Optionally trims certain lines (e.g., Domain Status)
    
    Requires whois.exe installed & in PATH.
    """
    try:
        raw_output = subprocess.check_output(
            ["whois", domain],
            text=True,
            timeout=10
        )
    except subprocess.CalledProcessError as cpe:
        return f"[Error] Non-zero exit code: {cpe.returncode}\nOutput:\n{cpe.output}"
    except FileNotFoundError:
        return "[Error] whois.exe not found. Make sure it's installed and in your PATH."
    except Exception as e:
        return f"[Error] {str(e)}"

    lines = raw_output.splitlines()
    seen = set()
    cleaned = []

    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue  # skip empty lines

        # Must contain ":" AND not contain any SKIP_KEYWORDS
        if ":" in line_stripped:
            lower_line = line_stripped.lower()
            if any(keyword in lower_line for keyword in SKIP_KEYWORDS):
                continue

            # Custom transform (e.g., strip trailing disclaimers in Domain Status lines)
            line_stripped = clean_whois_line(line_stripped)

            # Deduplicate
            if line_stripped not in seen:
                cleaned.append(line_stripped)
                seen.add(line_stripped)

    return "\n".join(cleaned)

if __name__ == "__main__":
    domain = input("Enter domain to WHOIS: ")
    result = whois_lookup_windows(domain)
    print("\n=== WHOIS Output ===")
    print(result)
