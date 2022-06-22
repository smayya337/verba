import json


def noun_handler(inflection):
    return {
        "part of speech": inflection[0],
        "which": int(inflection[1]),
        "variation": int(inflection[2]),
        "case": inflection[3],
        "number": inflection[4],
        "gender": inflection[5],
        "key": int(inflection[6]),
        "size": int(inflection[7]),
        "ending": inflection[8] if int(inflection[7]) > 0 else "",
        "age": inflection[-2],
        "frequency": inflection[-1],
    }


def verb_handler(inflection):
    return {
        "part of speech": inflection[0],
        "which": int(inflection[1]),
        "variation": int(inflection[2]),
        "tense": inflection[3],
        "voice": inflection[4],
        "mood": inflection[5],
        "person": int(inflection[6]),
        "number": inflection[7],
        "key": int(inflection[8]),
        "size": int(inflection[9]),
        "ending": inflection[10] if int(inflection[9]) > 0 else "",
        "age": inflection[-2],
        "frequency": inflection[-1],
    }


def number_handler(inflection):
    return {
        "part of speech": inflection[0],
        "which": int(inflection[1]),
        "variation": int(inflection[2]),
        "case": inflection[3],
        "number": inflection[4],
        "gender": inflection[5],
        "type": inflection[6],
        "key": int(inflection[7]),
        "size": int(inflection[8]),
        "ending": inflection[9] if int(inflection[8]) > 0 else "",
        "age": inflection[-2],
        "frequency": inflection[-1],
    }


def vpar_handler(inflection):
    return {
        "part of speech": inflection[0],
        "which": int(inflection[1]),
        "variation": int(inflection[2]),
        "case": inflection[3],
        "number": inflection[4],
        "gender": inflection[5],
        "tense": inflection[6],
        "voice": inflection[7],
        "mood": inflection[8],
        "key": int(inflection[9]),
        "size": int(inflection[10]),
        "ending": inflection[11] if int(inflection[10]) > 0 else "",
        "age": inflection[-2],
        "frequency": inflection[-1],
    }


def prep_handler(inflection):
    return {
        "part of speech": inflection[0],
        "case": inflection[1],
        "key": int(inflection[2]),
        "size": int(inflection[3]),
        "ending": inflection[4] if int(inflection[3]) > 0 else "",
        "age": inflection[-2],
        "frequency": inflection[-1],
    }


def adverb_handler(inflection):
    return {
        "part of speech": inflection[0],
        "level": inflection[1],
        "key": int(inflection[2]),
        "size": int(inflection[3]),
        "ending": inflection[4] if int(inflection[3]) > 0 else "",
        "age": inflection[-2],
        "frequency": inflection[-1],
    }


def conj_handler(inflection):
    return {
        "part of speech": inflection[0],
        "key": int(inflection[1]),
        "size": int(inflection[2]),
        "ending": inflection[3] if int(inflection[2]) > 0 else "",
        "age": inflection[-2],
        "frequency": inflection[-1],
    }


def adj_handler(inflection):
    return {
        "part of speech": inflection[0],
        "which": int(inflection[1]),
        "variation": int(inflection[2]),
        "case": inflection[3],
        "number": inflection[4],
        "gender": inflection[5],
        "level": inflection[6],
        "key": int(inflection[7]),
        "size": int(inflection[8]),
        "ending": inflection[9] if int(inflection[8]) > 0 else "",
        "age": inflection[-2],
        "frequency": inflection[-1],
    }


with open("../data/INFLECTS.DATA") as f:
    lines = [
        line.strip()
        for line in f
        if len(line.strip()) > 0 and not line.startswith("--")
    ]

lines = [line.split("--")[0].strip() for line in lines]
lines = [line for line in lines if line]

types = set()
for line in lines:
    # print(line)
    types.add(line.split(" ")[0])
# print(types)

inflections = [line.split() for line in lines]
output = []

for inflection in inflections:
    part_of_speech = inflection[0]
    functions_to_use = {
        "N": noun_handler,
        "V": verb_handler,
        "NUM": number_handler,
        "PRON": noun_handler,
        "SUPINE": noun_handler,
        "VPAR": vpar_handler,
        "PREP": prep_handler,
        "ADV": adverb_handler,
        "CONJ": conj_handler,
        "INTERJ": conj_handler,
        "ADJ": adj_handler,
    }
    if part_of_speech in functions_to_use:
        output.append(functions_to_use[part_of_speech](inflection))

# print(output)
with open("../data/inflections.json", "w") as f:
    json.dump(output, f, indent=2)
