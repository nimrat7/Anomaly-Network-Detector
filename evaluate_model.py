
import pandas as pd
import joblib

# Load trained model
saved = joblib.load("network_anomaly_model.pkl")

model = saved["model"]
features = saved["features"]

# Load fresh testing dataset
data = pd.read_csv("ml_features_day2.csv")

if data.empty:
    raise ValueError("Testing dataset is empty!")

# Use exactly the same features as training
X_test = data[features]

# Predict normal and anomalous flows
predictions = model.predict(X_test)

# Calculate anomaly scores
scores = model.decision_function(X_test)

# Store results
results = data.copy()

results["Anomaly Score"] = scores
results["Prediction"] = predictions

results["Status"] = results["Prediction"].map({
    1: "Normal",
    -1: "Anomaly"
})

# Count results
normal = (predictions == 1).sum()
anomalies = (predictions == -1).sum()

print("\nMODEL TESTING COMPLETED!")

print("Total testing flows:", len(data))
print("Normal flows:", normal)
print("Anomalous flows:", anomalies)

percentage = (anomalies / len(data)) * 100

print("Anomaly percentage:", round(percentage, 2), "%")

# Save testing results
results.to_csv("testing_results.csv", index=False)

print("\nResults saved as testing_results.csv")
