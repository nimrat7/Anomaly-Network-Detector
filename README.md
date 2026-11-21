# Anomaly-Network-Detector
# 🛡️ Network Anomaly Detector

### Real-Time Network Monitoring and Anomaly Detection System

A Linux-based network anomaly detection project built using Python, Scapy and Machine Learning. The system captures live network traffic, analyzes network flows, identifies potentially anomalous behaviour using an Isolation Forest model, and sends instant security alerts through a Telegram bot.

---

## 🚀 Project Overview

**Network Anomaly Detector** is designed to monitor live network traffic and identify unusual communication patterns that may indicate suspicious network activity.

The system captures packets, extracts network-flow features, analyzes traffic using a trained machine learning model, and notifies the user whenever an anomaly is detected.

The project aims to provide lightweight, real-time network monitoring and security awareness on Linux systems.

## ✨ Key Features

- **Live Packet Capture:** Captures network packets using Scapy.
- **Network Flow Analysis:** Groups traffic using source IP, destination IP, protocol and port information.
- **Machine Learning Detection:** Uses an Isolation Forest model to identify potentially anomalous network flows.
- **Feature Extraction:** Analyzes packet count, total bytes, average packet size, minimum and maximum packet size, duration and traffic rates.
- **Anomaly Scoring:** Generates anomaly scores for analyzed network flows.
- **Telegram Notifications:** Sends instant alerts when anomalous activity is detected.
- **Alert Cooldown:** Helps prevent repeated notifications for the same network flow.
- **CSV Logging:** Saves live detection results for later inspection.

## 🧠 How It Works

1. Scapy captures live network packets.
2. The system extracts source and destination IP addresses, protocols and port numbers.
3. Packets are grouped into network flows.
4. Network-flow features are calculated.
5. The trained Isolation Forest model analyzes each flow.
6. Potential anomalies are identified.
7. A Telegram notification is sent when an anomaly is detected.
8. Detection results are saved in a CSV file.

## 🏗️ System Architecture

```text
       Live Network Traffic
                |
                v
        Scapy Packet Capture
                |
                v
       Network Flow Processing
                |
                v
        Feature Extraction
                |
                v
       Isolation Forest Model
                |
                v
       Anomaly Classification
                |
          +-----+-----+
          |           |
          v           v
       NORMAL      ANOMALY
                      |
               +------+------+
               |             |
               v             v
          CSV Logging   Telegram Bot
                              |
                              v
                       Phone Notification
```

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Kali Linux | Operating environment |
| Scapy | Live packet capture |
| Pandas | Network data processing |
| Scikit-learn | Machine learning |
| Isolation Forest | Anomaly detection |
| Joblib | Saving and loading the trained model |
| CSV | Dataset and detection-result storage |
| Telegram Bot API | Security notifications |

## 📂 Project Structure

```text
Network-Anomaly-Detector/
│
├── live_detector.py
├── packet_capture.py
├── packet_capture_csv.py
├── feature_extraction.py
├── prepare_dataset.py
├── train_model.py
├── evaluate_model.py
├── verification_engine.py
├── telegram_alert.py
│
├── flow_features.csv
├── ml_features.csv
├── ml_features_day2.csv
├── normal_flow_features_day1.csv
├── normal_flow_features_day2.csv
├── normal_traffic_day1.csv
├── normal_traffic_day2.csv
│
├── training_results.csv
├── testing_results.csv
│
├── LICENSE
└── README.md
```

Additional runtime files, including the trained model and Telegram configuration, are generated or configured locally.

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/nimrat7/Anomaly-Network-Detector.git
```

### 2. Enter the project directory

```bash
cd Anomaly-Network-Detector
```

### 3. Create a virtual environment

```bash
python3 -m venv .venv
```

### 4. Activate the environment

```bash
source .venv/bin/activate
```

### 5. Install required Python libraries

```bash
pip install scapy pandas numpy scikit-learn joblib
```

### 6. Configure Telegram

Create a Telegram bot using BotFather and configure your bot credentials locally.

The Telegram configuration file must not be uploaded to GitHub.

### 7. Train the machine learning model

Ensure the prepared dataset `ml_features.csv` is available, then run:

```bash
python train_model.py
```

This generates the trained model:

```text
network_anomaly_model.pkl
```

## ▶️ Running the Detector

Start the live network monitoring system using:

```bash
sudo .venv/bin/python live_detector.py
```

The detector will begin capturing live network traffic and analyzing supported TCP and UDP network flows.

Press `CTRL + C` to stop monitoring.

## 📩 Telegram Security Alerts

When a potentially anomalous network flow is identified, the system sends a Telegram notification containing information such as:

- Source IP address
- Destination IP address
- Protocol
- Source port
- Destination port
- Total packets
- Total bytes
- Anomaly score

## 📊 Detection Results

Live detection results are stored in:

```text
live_detection_results.csv
```

The results include timestamps, network-flow details, anomaly scores and detection status.

## 🔐 Security and Privacy

- Never upload Telegram bot tokens or private credentials.
- Keep sensitive configuration files outside version control.
- Use the detector only on networks you own or have permission to monitor.
- Network traffic records may contain sensitive information.

## 🎯 Project Objectives

- Monitor live network traffic.
- Understand normal network communication patterns.
- Identify potentially anomalous network behaviour.
- Apply machine learning to network-flow analysis.
- Provide immediate security notifications.
- Maintain records for further investigation.

## 🔮 Future Improvements

- Web-based monitoring dashboard.
- Advanced anomaly visualization.
- Improved detection accuracy.
- More network protocol support.
- Historical traffic analysis.

## 👨‍💻 Project

**Project Name:** Network Anomaly Detector

**Platform:** Linux / Kali Linux

**Language:** Python

**Detection Algorithm:** Isolation Forest

**Notification System:** Telegram Bot API

---

⭐ If you find this project interesting, consider starring the repository!

**Repository:** https://github.com/nimrat7/Anomaly-Network-Detector
