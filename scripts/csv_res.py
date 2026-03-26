import csv

# Fill this list with your simulation data
data = [
    ["random_0%", 0, 529289, 76382, 0.870750, ""],
    ["random_5%", 3840, 323932, 71653, 0.782807, ""],
    ["random_10%", 7680, 302074, 70029, 0.744315, ""],
    ["random_20%", 15360, 193570, 65681, 0.415640, ""],
    ["random_50%", 38401, 55762, 35986, 0.143229, ""],
    ["tier1", 37, 307409, 66053, 0.752508, "Tier1 only deployment"],
    ["highdeg_5", 3840, 831, 831, 0.002242, "High-degree 5%"],
    ["highdeg_10", 7680, 823, 823, 0.002750, "High-degree 10%"],
    ["highdeg_20", 15360, 818, 824, 0.002179, "High-degree 20%"],
]

with open("rov_sim_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Deployment", "ROV ASes", "BGP Updates", "Affected ASes", "Convergence Time", "Notes"])
    writer.writerows(data)

print("CSV saved as rov_sim_results.csv")