
from scapy.all import sniff, IP, TCP, UDP
import csv
from datetime import datetime

file = open("network_traffic.csv", "w", newline="")

writer = csv.writer(file)

writer.writerow([
    "Timestamp",
    "Source IP",
    "Destination IP",
    "Protocol",
    "Source Port",
    "Destination Port",
    "Packet Size"
])

def analyze_packet(packet):

    if IP in packet:

        source = packet[IP].src
        destination = packet[IP].dst
        protocol = packet[IP].proto
        size = len(packet)

        source_port = ""
        destination_port = ""

        if TCP in packet:
            source_port = packet[TCP].sport
            destination_port = packet[TCP].dport

        elif UDP in packet:
            source_port = packet[UDP].sport
            destination_port = packet[UDP].dport

        timestamp = datetime.now()

        writer.writerow([
            timestamp,
            source,
            destination,
            protocol,
            source_port,
            destination_port,
            size
        ])

        file.flush()

        print("Packet captured:", source, "->", destination)

print("Network Anomaly Detector Started")
print("Saving network traffic to CSV...")

try:
    sniff(prn=analyze_packet, store=False)

except KeyboardInterrupt:
    print("\nPacket capture stopped.")

finally:
    file.close()
    print("Dataset saved successfully.")
