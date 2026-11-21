
from scapy.all import sniff, IP, TCP, UDP
import pandas as pd
import joblib
import csv
import os
import time

from telegram_alert import send_telegram_alert

# Load trained model
saved = joblib.load("network_anomaly_model.pkl")

model = saved["model"]
features = saved["features"]

# Flow inactivity timeout in seconds
FLOW_TIMEOUT = 10
ALERT_COOLDOWN = 300

last_alert_times = {}

# Store active network flows
flows = {}

# Output file
OUTPUT_FILE = "live_detection_results.csv"

# Create output file if it does not exist
if not os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Timestamp",
            "Source IP",
            "Destination IP",
            "Protocol",
            "Source Port",
            "Destination Port",
            "Total Packets",
            "Total Bytes",
            "Anomaly Score",
            "Status"
        ])


def process_flow(key, flow):

    source, destination, protocol, sport, dport = key

    duration = flow["last_seen"] - flow["first_seen"]

    packet_rate = (
        flow["packets"] / duration if duration > 0 else 0
    )

    byte_rate = (
        flow["total_bytes"] / duration if duration > 0 else 0
    )

    avg_size = flow["total_bytes"] / flow["packets"]

    row = {
        "Protocol": protocol,
        "Source Port": sport,
        "Destination Port": dport,
        "Total Packets": flow["packets"],
        "Total Bytes": flow["total_bytes"],
        "Average Packet Size": avg_size,
        "Minimum Packet Size": flow["min_size"],
        "Maximum Packet Size": flow["max_size"],
        "Duration": duration,
        "Packets Per Second": packet_rate,
        "Bytes Per Second": byte_rate
    }

    # Use the exact training feature order
    X = pd.DataFrame([row])[features]

    prediction = model.predict(X)[0]
    score = model.decision_function(X)[0]
    print(
    "DEBUG | Prediction:", prediction,
    "| Decision Score:", round(float(score), 6)
)
    # Determine detection status
    if prediction == -1:
        status = "ANOMALY"
    else:
        status = "NORMAL"

    # Send Telegram alert for anomalies
    if prediction == -1:

        alert_key = (
            source,
            destination,
            protocol,
            sport,
            dport
        )

        current_time = time.time()
        last_sent = last_alert_times.get(alert_key, 0)

        if current_time - last_sent >= ALERT_COOLDOWN:

            message = f"""
🚨 NETWORK ANOMALY DETECTED!

Source IP: {source}
Destination IP: {destination}

Protocol: {protocol}
Source Port: {sport}
Destination Port: {dport}

Total Packets: {flow["packets"]}
Total Bytes: {flow["total_bytes"]}

Anomaly Score: {score:.5f}

Status: ANOMALOUS

Please investigate this connection.
"""

            sent = send_telegram_alert(message)

            if sent:
                last_alert_times[alert_key] = current_time

    print("\n-------------------------------")
    print("Source IP:", source)
    print("Destination IP:", destination)
    print("Protocol:", protocol)
    print("Total Packets:", flow["packets"])
    print("Anomaly Score:", round(score, 5))
    print("Detection:", status)

    # Save detection result
    with open(OUTPUT_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            time.strftime("%Y-%m-%d %H:%M:%S"),
            source,
            destination,
            protocol,
            sport,
            dport,
            flow["packets"],
            flow["total_bytes"],
            score,
            status
        ])


def analyze_packet(packet):

    if IP not in packet:
        return

    # Initial model supports TCP and UDP flows
    if TCP in packet:
        sport = packet[TCP].sport
        dport = packet[TCP].dport

    elif UDP in packet:
        sport = packet[UDP].sport
        dport = packet[UDP].dport

    else:
        return

    source = packet[IP].src
    destination = packet[IP].dst
    protocol = packet[IP].proto

    size = len(packet)
    now = time.time()

    key = (
        source,
        destination,
        protocol,
        sport,
        dport
    )

    if key not in flows:

        flows[key] = {
            "packets": 0,
            "total_bytes": 0,
            "first_seen": now,
            "last_seen": now,
            "min_size": float("inf"),
            "max_size": 0
        }

    flow = flows[key]

    flow["packets"] += 1
    flow["total_bytes"] += size
    flow["last_seen"] = now

    flow["min_size"] = min(flow["min_size"], size)
    flow["max_size"] = max(flow["max_size"], size)

    # Process inactive flows
    expired = [
        k for k, v in flows.items()
        if now - v["last_seen"] >= FLOW_TIMEOUT
    ]

    for expired_key in expired:
        process_flow(expired_key, flows.pop(expired_key))


print("================================")
print("NETWORK ANOMALY DETECTOR")
print("Live monitoring started...")
print("Flow timeout:", FLOW_TIMEOUT, "seconds")
print("Press CTRL+C to stop.")
print("================================")

try:
    sniff(prn=analyze_packet, store=False)

except KeyboardInterrupt:
    print("\nStopping live monitoring...")

finally:

    # Process remaining flows
    for key, flow in list(flows.items()):
        process_flow(key, flow)

    flows.clear()

    print("\nMonitoring stopped.")
    print("Results saved in:", OUTPUT_FILE)
