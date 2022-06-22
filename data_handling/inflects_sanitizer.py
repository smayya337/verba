with open("../data/INFLECTS.DATA") as f:
    lines = [line[:-1] if line.endswith("\n") else line for line in f]
    lines = [line for line in lines if not line.startswith("--")]

for i, line in enumerate(lines):
    lines[i] = line.split("--")[0].strip()

with open("../data/INFLECTS.DATA", "w") as f:
    for line in lines:
        if not line:
            continue
        f.write(line)
        f.write("\n")
