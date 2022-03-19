from glob import glob
import re

files = [a for a in glob("data/us_census/**/*", recursive=True)if a.endswith(".csv") or a.endswith(".txt") and "last" in a]

unique_names = set()

for file in files:
    pattern = re.compile(r"(^\w+)(,|\s)")
    with open(file, "r") as f:
        lines = f.readlines()
        for line in lines:
            name = pattern.search(line).group(1)
            if name not in unique_names:
                unique_names.add(name)

#write names to file
with open("usa_last_names.txt", "w") as f:
    for name in unique_names:
        f.write(name + "\n")