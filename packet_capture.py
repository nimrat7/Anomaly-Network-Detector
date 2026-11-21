from scapy.all import sniff, IP, TCP, UDP

def analyze_packet(packet):

    if IP in packet:
        source = packet[IP].src
        destination = packet[IP].dst
        protocol = packet[IP].proto
        size = len(packet)

        print("--------------------------------")
        print("Source IP:", source)
        print("Destination IP:", destination)
        print("Protocol:", protocol)
        print("Packet Size:", size, "bytes")

        if TCP in packet:
            print("Source Port:", packet[TCP].sport)
            print("Destination Port:", packet[TCP].dport)

        elif UDP in packet:
            print("Source Port:", packet[UDP].sport)
            print("Destination Port:", packet[UDP].dport)


print("Network Anomaly Detector - Packet Capture Started")

sniff(prn=analyze_packet, count=20, store=False)

