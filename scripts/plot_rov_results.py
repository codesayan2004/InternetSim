import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load CSV
df = pd.read_csv("scripts/rov_sim_results.csv")

# Separate datasets
random_df = df[df["Deployment"].str.contains("random")]
tier1_df = df[df["Deployment"] == "tier1"]
highdeg10_df = df[df["Deployment"] == "highdeg_10"]

# Extract X values (ROV %)
x = [int(d.split("_")[1].replace("%", "")) for d in random_df["Deployment"]]

affected = random_df["Affected ASes"].values
updates = random_df["BGP Updates"].values
time_vals = random_df["Convergence Time"].values

# Create figure
plt.figure(figsize=(14, 10))

# -------------------------------
# Plot 1: Affected ASes
# -------------------------------
plt.subplot(2, 2, 1)
plt.plot(x, affected, marker='o')
plt.title("Affected ASes vs Random ROV %")
plt.xlabel("Random ROV Deployment (%)")
plt.ylabel("Affected ASes")
plt.grid(True)

# -------------------------------
# Plot 2: BGP Updates
# -------------------------------
plt.subplot(2, 2, 2)
plt.plot(x, updates, marker='s')
plt.title("BGP Updates vs Random ROV %")
plt.xlabel("Random ROV Deployment (%)")
plt.ylabel("BGP Updates")
plt.grid(True)

# -------------------------------
# Plot 3: Convergence Time
# -------------------------------
plt.subplot(2, 2, 3)
plt.plot(x, time_vals, marker='^')
plt.title("Convergence Time vs Random ROV %")
plt.xlabel("Random ROV Deployment (%)")
plt.ylabel("Time (seconds)")
plt.ylim(0, max(time_vals) * 1.1)  # auto-scale nicely
plt.grid(True)

# -------------------------------
# Plot 4: Log-scale Bar (Tier1 vs Highdeg_10)
# -------------------------------
plt.subplot(2, 2, 4)

labels = ["Tier1", "HighDeg_10"]

tier1_vals = [
    tier1_df["Affected ASes"].values[0],
    tier1_df["BGP Updates"].values[0],
    tier1_df["Convergence Time"].values[0]
]

highdeg_vals = [
    highdeg10_df["Affected ASes"].values[0],
    highdeg10_df["BGP Updates"].values[0],
    highdeg10_df["Convergence Time"].values[0]
]

x_pos = np.arange(len(labels))
width = 0.25

plt.bar(x_pos - width, [tier1_vals[0], highdeg_vals[0]], width, label="Affected ASes")
plt.bar(x_pos, [tier1_vals[1], highdeg_vals[1]], width, label="BGP Updates")
plt.bar(x_pos + width, [tier1_vals[2], highdeg_vals[2]], width, label="Convergence Time")

plt.yscale("log")
plt.xticks(x_pos, labels)
plt.title("Tier-1 vs High-Degree (Log Scale)")
plt.ylabel("Log Scale Values")
plt.legend()
plt.grid(True, which="both", linestyle="--", linewidth=0.5)

# -------------------------------
# Final layout + save
# -------------------------------
plt.tight_layout()
plt.savefig("rov_analysis.png", dpi=300)
plt.show()