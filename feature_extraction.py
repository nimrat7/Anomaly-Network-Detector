
import csv
from collections import defaultdict
from datetime import datetime

input_file = "normal_traffic_day2.csv"
output_file = "normal_flow_features_day2.csv"

flows = defaultdict(lambda: {
    "packets": 0,
    "total_bytes": 0,
    "first_seen": None,
    "last_seen": None,
    "min_size": float("inf"),
    "max_size": 0
})

# Read captured packet data
with open(input_file, "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        timestamp = datetime.fromisoformat(row["Timestamp"])
        source = row["Source IP"]
        destination = row["Destination IP"]
        protocol = row["Protocol"]
        source_port = row["Source Port"]
        destination_port = row["Destination Port"]
        size = int(row["Packet Size"])

        # Identify a network flow
        key = (
            source,
            destination,
            protocol,
            source_port,
            destination_port
        )

        flow = flows[key]

        flow["packets"] += 1
        flow["total_bytes"] += size

        if flow["first_seen"] is None:
            flow["first_seen"] = timestamp

        flow["last_seen"] = timestamp

        flow["min_size"] = min(flow["min_size"], size)
        flow["max_size"] = max(flow["max_size"], size)


# Save extracted features
with open(output_file, "w", newline="") as file:

    fields = [
        "Source IP",
        "Destination IP",
        "Protocol",
        "Source Port",
        "Destination Port",
        "Total Packets",
        "Total Bytes",
        "Average Packet Size",
        "Minimum Packet Size",
        "Maximum Packet Size",
        "Duration",
        "Packets Per Second",
        "Bytes Per Second"
    ]

    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()

    for key, flow in flows.items():

        source, destination, protocol, sport, dport = key

        duration = (
            flow["last_seen"] - flow["first_seen"]
        ).total_seconds()

        avg_size = (
            flow["total_bytes"] / flow["packets"]
        )

        packet_rate = (
            flow["packets"] / duration if duration > 0 else 0
        )

        byte_rate = (
            flow["total_bytes"] / duration if duration > 0 else 0
        )

        writer.writerow({
            "Source IP": source,
            "Destination IP": destination,
            "Protocol": protocol,
            "Source Port": sport,
            "Destination Port": dport,
            "Total Packets": flow["packets"],
            "Total Bytes": flow["total_bytes"],
            "Average Packet Size": round(avg_size, 2),
            "Minimum Packet Size": flow["min_size"],
            "Maximum Packet Size": flow["max_size"],
            "Duration": round(duration, 4),
            "Packets Per Second": round(packet_rate, 2),
            "Bytes Per Second": round(byte_rate, 2)
        })

print("Feature extraction completed!")
print("Total network flows:", len(flows))
print("Output saved in:", output_file)
