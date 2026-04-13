# split_highdeg.py
with open("data/rov_highdeg_5.txt") as f:
    ases = [line.strip() for line in f]

step = 50  # increment
for k in range(0, 500, step):
    with open(f"experiments/rov_{k}.txt", "w") as out:
        for asn in ases[:k]:  # take top k ASes
            out.write(f"{asn}\n")