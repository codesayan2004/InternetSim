import matplotlib.pyplot as plt
import pandas as pd

# --- Data ---
data = {
    "ROV": [0, 50, 100, 150, 200, 250, 300, 350, 400, 450],
    "BGP_updates": [341452, 212932, 173321, 87441, 65199, 47842, 40981, 36616, 9874, 8339],
    "Affected_ASes": [72435, 53582, 49016, 37907, 31108, 26666, 24850, 22085, 8344, 7284]
}

df = pd.DataFrame(data)

total_AS = 76382

# --- Compute percentages ---
df["Affected_ASes_pct"] = df["Affected_ASes"] / total_AS * 100
df["Network_Protected_pct"] = 100 - df["Affected_ASes_pct"]  # Inverse for "protected"

# --- Thresholds ---
threshold_50 = 50  # 50% of network protected corresponds to 50% affected
threshold_90 = 90  # 90% protected corresponds to 10% affected

rov_50 = df[df["Network_Protected_pct"] >= threshold_50]["ROV"].iloc[0]
rov_90 = df[df["Network_Protected_pct"] >= threshold_90]["ROV"].iloc[0]

print(f"ROV required for ~50% network protected: {rov_50} ({df[df['ROV']==rov_50]['Network_Protected_pct'].values[0]:.1f}%)")
print(f"ROV required for ~90% network protected: {rov_90} ({df[df['ROV']==rov_90]['Network_Protected_pct'].values[0]:.1f}%)")

# --- Plot ---
fig, ax1 = plt.subplots(figsize=(10,6))

# Plot Network Protected %
color1 = 'tab:blue'
ax1.set_xlabel('Number of High-Degree ASes with ROV')
ax1.set_ylabel('% Network Secured', color=color1)
ax1.plot(df["ROV"], df["Network_Protected_pct"], marker='o', color=color1, label="% Network Protected")
ax1.tick_params(axis='y', labelcolor=color1)

# Plot BGP updates
ax2 = ax1.twinx()
color2 = 'tab:red'
ax2.set_ylabel('BGP Updates', color=color2)
ax2.plot(df["ROV"], df["BGP_updates"], marker='s', color=color2, label="BGP Updates")
ax2.tick_params(axis='y', labelcolor=color2)

# Set x-axis ticks
ax1.set_xticks(df["ROV"])

# Add grid and title
fig.tight_layout()
plt.title('Impact of ROV Deployment on BGP Updates and Network Protection')

# Combine legends
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc='upper center')

plt.show()