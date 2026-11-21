from collections import deque
from datetime import datetime, timezone


class VerificationEngine:

    def __init__(self, window_seconds=300):
        self.window_seconds = window_seconds
        self.history = deque()

    def verify(self, flow):

        now = datetime.now(timezone.utc)

        source = str(flow.get("source_ip", "unknown"))
        destination = str(flow.get("destination_ip", "unknown"))
        protocol = str(flow.get("protocol", "unknown"))

        source_port = str(flow.get("source_port", ""))
        destination_port = str(flow.get("destination_port", ""))

        packets = int(float(flow.get("packets", 0) or 0))
        byte_count = int(float(flow.get("bytes", 0) or 0))

        key = (
            source,
            destination,
            protocol,
            source_port,
            destination_port
        )

        self.history.append({
            "time": now,
            "source": source,
            "destination": destination,
            "destination_port": destination_port,
            "key": key,
            "packets": packets,
            "bytes": byte_count
        })

        while self.history:
            age = (now - self.history[0]["time"]).total_seconds()

            if age <= self.window_seconds:
                break

            self.history.popleft()

        source_history = [
            item for item in self.history
            if item["source"] == source
        ]

        destinations = {
            item["destination"] for item in source_history
        }

        ports = {
            item["destination_port"] for item in source_history
        }

        same_flow_count = sum(
            item["key"] == key for item in source_history
        )

        risk_score = 0
        reasons = []

        # Rule 1: Many destination ports
        if len(ports) >= 10:
            risk_score += 3
            reasons.append("Multiple destination ports observed")

        # Rule 2: Many destinations
        if len(destinations) >= 10:
            risk_score += 2
            reasons.append("Connections to many destinations")

        # Rule 3: Repeated connections
        if same_flow_count >= 10:
            risk_score += 2
            reasons.append("Repeated connections to the same flow")

        # Rule 4: Large traffic volume
        if packets >= 1000 and byte_count >= 1000000:
            risk_score += 1
            reasons.append("Large packet and byte volume")

        # Conservative initial classification
        if risk_score >= 5:
            verification = "HIGH_PRIORITY"
        elif risk_score >= 2:
            verification = "SUSPICIOUS_MONITOR"
        else:
            verification = "LIKELY_LEGITIMATE"

        return {
            "verification": verification,
            "risk_score": risk_score,
            "reasons": reasons,
            "destination_count": len(destinations),
            "port_count": len(ports),
            "repeated_count": same_flow_count
        }


if __name__ == "__main__":

    engine = VerificationEngine()

    sample = {
        "source_ip": "192.168.1.10",
        "destination_ip": "142.251.144.6",
        "protocol": "TCP",
        "source_port": 50000,
        "destination_port": 443,
        "packets": 20,
        "bytes": 12000
    }

    result = engine.verify(sample)

    print("\nVERIFICATION ENGINE TEST")
    print("-----------------------")
    print("Decision:", result["verification"])
    print("Risk score:", result["risk_score"])
    print("Reasons:", result["reasons"])
