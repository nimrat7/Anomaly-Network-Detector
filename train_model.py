
import pandas as pd
import joblib

from sklearn.ensemble import IsolationForest

# Load prepared network dataset
data = pd.read_csv("ml_features.csv")

print("Dataset loaded successfully!")
print("Total network flows:", len(data))

# Check dataset
if len(data) < 10:
    raise ValueError("Not enough network flows to train the model.")

# Select machine learning features
features = [
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

X = data[features]

# Create Isolation Forest model
model = IsolationForest(
    n_estimators=200,
    contamination=0.02,
    random_state=42
)

# Train the model
print("\nTraining Isolation Forest...")

model.fit(X)

# Predict anomalies
predictions = model.predict(X)

# Calculate anomaly scores
scores = model.decision_function(X)

# Add results to dataset
results = data.copy()

results["Anomaly Score"] = scores
results["Prediction"] = predictions

results["Status"] = results["Prediction"].map({
    1: "Normal",
    -1: "Anomaly"
})

# Save results
results.to_csv("training_results.csv", index=False)

# Save trained model and feature information
joblib.dump({
    "model": model,
    "features": features
}, "network_anomaly_model.pkl")

# Display results
normal_count = (predictions == 1).sum()
anomaly_count = (predictions == -1).sum()

print("\nMODEL TRAINING COMPLETED!")

print("Normal flows:", normal_count)
print("Anomalous flows:", anomaly_count)

print("\nModel saved as network_anomaly_model.pkl")
print("Results saved as training_results.csv")
