import os
from collections import defaultdict

# Input AS relationships file
AS_FILE = "data/20240501.as-rel.txt"

# Output ROV sets
OUTPUT_DIR = "data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Percentages for high-degree ROV sets
HIGH_DEG_PERCENTS = [5, 10, 20]

# Threshold for filtering "true" Tier-1
TIER1_DEGREE_THRESHOLD = 50  # Can tweak based on dataset

# Read AS relationships
neighbors = defaultdict(set)
providers = defaultdict(set)
all_ASes = set()

with open(AS_FILE, "r") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("|")
        if len(parts) != 3:
            continue
        as1, as2, rel = parts
        as1 = int(as1)
        as2 = int(as2)
        rel = int(rel)
        all_ASes.update([as1, as2])
        neighbors[as1].add(as2)
        neighbors[as2].add(as1)
        if rel == -1:
            providers[as2].add(as1)
        elif rel == 1:
            providers[as1].add(as2)

# Compute Tier-1 ASes: no providers AND high-degree
tier1_ASes = []
for asn in all_ASes:
    if len(providers[asn]) == 0 and len(neighbors[asn]) >= TIER1_DEGREE_THRESHOLD:
        tier1_ASes.append(asn)

print("Total ASes:", len(all_ASes))
print("Tier-1 count:", len(tier1_ASes))

# Save Tier-1 ROV set
tier1_file = os.path.join(OUTPUT_DIR, "rov_tier1.txt")
with open(tier1_file, "w") as f:
    for asn in tier1_ASes:
        f.write(f"{asn}\n")

# Compute high-degree ASes
degree_list = [(asn, len(neighbors[asn])) for asn in all_ASes]
degree_list.sort(key=lambda x: x[1], reverse=True)

for percent in HIGH_DEG_PERCENTS:
    count = int(len(all_ASes) * percent / 100)
    high_deg_ASes = [asn for asn, _ in degree_list[:count]]
    file_path = os.path.join(OUTPUT_DIR, f"rov_highdeg_{percent}.txt")
    with open(file_path, "w") as f:
        for asn in high_deg_ASes:
            f.write(f"{asn}\n")
    print(f"{file_path} count:", len(high_deg_ASes))