from scapy.all import sniff, Ether, IP, TCP, UDP, ARP, DNS, DNSQR
import requests
from datetime import datetime
import time
import questionary

# -------------------------------
# MAC Vendor Lookup Function
# -------------------------------
def get_mac_vendor(mac):
    """
    Queries the macvendors.com API to retrieve the manufacturer of a given MAC address.
    """
    url = f"https://api.macvendors.com/{mac}"
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        pass
    return "Unknown Vendor"

# -------------------------------
# Packet Handler - Processes Packets for Sniffing Mode
# -------------------------------
def packet_handler(pkt):
    """
    Processes captured network packets and extracts key details including:
    - Source & Destination MAC/IP
    - Protocol (TCP, UDP, ARP, DNS)
    - Port number
    - DNS Query (if applicable)
    - Timestamp of the captured packet
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Add timestamp

    src_mac, dst_mac = "Unknown", "Unknown"
    src_ip, dst_ip = "Unknown", "Unknown"
    protocol, port = "Unknown", "N/A"
    dns_query = None

    # Extract Ethernet (MAC) Addresses
    if pkt.haslayer(Ether):
        src_mac = pkt[Ether].src
        dst_mac = pkt[Ether].dst

    # Extract IP Addresses
    if pkt.haslayer(IP):
        src_ip = pkt[IP].src
        dst_ip = pkt[IP].dst

    # Identify Transport Layer Protocols (TCP/UDP)
    if pkt.haslayer(TCP):
        protocol = "TCP"
        port = pkt[TCP].dport
    elif pkt.haslayer(UDP):
        protocol = "UDP"
        port = pkt[UDP].dport

    # Detect DNS Queries
    if pkt.haslayer(DNS) and pkt.haslayer(DNSQR):
        dns_query = pkt[DNSQR].qname.decode()

    # Handle ARP Packets
    elif pkt.haslayer(ARP):
        protocol = "ARP"
        src_ip = pkt[ARP].psrc
        dst_ip = pkt[ARP].pdst

    # Get MAC Vendors
    src_vendor = get_mac_vendor(src_mac)
    dst_vendor = get_mac_vendor(dst_mac)

    # Print Packet Details with Timestamp
    print(f"\n[📡] {timestamp} - Detected Traffic:")
    print(f"🔹 Source: {src_mac} ({src_vendor}) | {src_ip}")
    print(f"🔸 Destination: {dst_mac} ({dst_vendor}) | {dst_ip}")
    print(f"⚡ Protocol: {protocol} | Port: {port}")

    # Print DNS Query if detected
    if dns_query:
        print(f"🌐 DNS Query: {dns_query}")

# -------------------------------
# Network Summarizer
# -------------------------------
def network_summarizer(iface, duration):
    """
    Captures network traffic for the specified duration and lists unique devices detected.
    """
    print(f"[🕵️‍♂️] Listening for {duration} seconds on {iface}...")
    start_time = time.time()
    devices = {}

    def collect_devices(pkt):
        nonlocal devices
        if pkt.haslayer(Ether):
            mac = pkt[Ether].src
            if mac not in devices:
                devices[mac] = get_mac_vendor(mac)

    sniff(iface=iface, prn=collect_devices, store=0, timeout=duration)
    
    print("\n[📋] Summary of detected devices:")
    for mac, vendor in devices.items():
        print(f"🔹 {mac} - {vendor}")

# -------------------------------
# User Selection and Execution
# -------------------------------
def run_sniffer():
    mode = questionary.select(
        "Choose mode:",
        choices=["Live Sniffer", "Network Summarizer"]
    ).ask()
    
    iface = questionary.text("Enter network interface (e.g., Wi-Fi, eth0, wlan0):").ask()

    if mode == "Live Sniffer":
        print(f"[🔥] Sniffing on {iface}... Press CTRL+C to stop.")
        sniff(iface=iface, prn=packet_handler, store=0)
    elif mode == "Network Summarizer":
        duration = int(questionary.text("Enter duration for summarizer (seconds):").ask())
        network_summarizer(iface, duration)
    else:
        print("[❌] Invalid choice. Please restart and choose an option.")

if __name__ == "__main__":
    run_sniffer()
