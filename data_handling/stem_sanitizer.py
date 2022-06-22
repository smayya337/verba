from verba.words import Word

with open("../data/STEMLIST.DATA") as f:
    lines = [line[:-1] if line.endswith("\n") else line for line in f]

# for i, line in enumerate(lines):
# word = line[:20].replace("j", "i")
# lines[i] = word + line[20:]

with open("../data/STEMLIST.DATA", "w") as f:
    for line in lines:
        f.write(line)
        f.write("\n")
