from verba.words import Word
import json
import re


def verb_handler(data):
    return {
        "part of speech": data[0],
        "which": int(data[1]),
        "variation": int(data[2]),
        "tense": data[3],
        "voice": data[4],
        "mood": data[5],
        "person": int(data[6]),
        "number": data[7],
        "type": data[8],
        "age": data[9],
        "area": data[10],
        "geo": data[11],
        "freq": data[12],
        "source": data[13],
    }


def noun_handler(data):
    return {
        "part of speech": data[0],
        "which": int(data[1]),
        "variation": int(data[2]),
        "case": data[3],
        "number": data[4],
        "gender": data[5],
        "type": data[6],
        "age": data[7],
        "area": data[8],
        "geo": data[9],
        "freq": data[10],
        "source": data[11],
    }


with open("../data/UNIQUES.DATA") as f:
    lines = [
        line.strip()
        for line in f
        if len(line.strip()) > 0 and not line.startswith("--")
    ]

lines = [line.split("--")[0].strip() for line in lines]
lines = [line for line in lines if line]

words = [(lines[i], lines[i + 1], lines[i + 2]) for i in range(0, len(lines), 3)]
output = []
types = set()

for word, data, definitions in words:
    word_info = data.split()
    definition_list = definitions.split(";")
    definition_list = [re.sub(r"\(.*\)", "", d.strip()) for d in definition_list]
    definition_list = [d.strip() for d in definition_list if d]
    for _ in range(len(definition_list)):
        first_item = definition_list.pop(0)
        if first_item.startswith("+"):
            continue
        first_item_broken = [d.strip() for d in first_item.split(",")]
        definition_list.extend(first_item_broken)
    part_of_speech = word_info[0]
    types.add(part_of_speech)
    functions_to_use = {
        "V": verb_handler,
        "N": noun_handler,
        "PRON": noun_handler,
        "ADJ": noun_handler,
    }
    if part_of_speech in functions_to_use:
        # print(word, word_info)
        word_info_for_json = functions_to_use[part_of_speech](word_info)
        word_info_for_json["word"] = Word.convert_to_classical_latin(word)
        word_info_for_json["definitions"] = definition_list
        output.append(word_info_for_json)

# print(output)
# print(types)
with open("../data/uniques.json", "w") as f:
    json.dump(output, f, indent=2)
