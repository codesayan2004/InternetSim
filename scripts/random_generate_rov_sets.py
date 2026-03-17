import random

TOTAL_AS = 76802
levels = [0,5,10,20,50]

ases = list(range(1, TOTAL_AS+1))

for p in levels:

    k = int(TOTAL_AS * p / 100)

    selected = random.sample(ases, k)

    with open(f"data/rov_{p}.txt","w") as f:
        for asn in selected:
            f.write(str(asn) + "\n")