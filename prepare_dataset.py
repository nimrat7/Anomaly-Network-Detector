
import pandas as pd
import numpy as np

# Load extracted network flow dataset
input_file = "normal_flow_features_day2.csv"

df = pd.read_csv(input_file)

print("Original dataset shape:", df.shape)

# Select useful numerical features
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

# Check whether all required columns exist
missing = [col for col in features if col not in df.columns]

if missing:
    raise ValueError(f"Missing columns: {missing}")

# Keep only selected features
data = df[features].copy()

# Convert values to numeric
for col in features:
    data[col] = pd.to_numeric(data[col], errors="coerce")

# Replace infinite values with missing values
data.replace([np.inf, -np.inf], np.nan, inplace=True)

# Remove incomplete rows
data.dropna(inplace=True)

# Remove invalid network flow records
data = data[
    (data["Total Packets"] > 0) &
    (data["Total Bytes"] > 0)
]

# Save prepared dataset
output_file = "ml_features_day2.csv"

data.to_csv(output_file, index=False)

print("\nDataset preparation completed!")
print("Original flows:", len(df))
print("Prepared flows:", len(data))
print("Removed rows:", len(df) - len(data))
print("Selected features:", len(features))
print("Saved as:", output_file)

print("\nPrepared dataset preview:")
print(data.head(10).to_string(index=False))
