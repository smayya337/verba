import json
import re


def noun_handler(parts, data, tags, definitions):
    return {
        "first principal part": "" if parts[0] == "zzz" else parts[0],
        "second principal part": ""
        if len(parts) <= 1 or parts[1] == "zzz"
        else parts[1],
        "third principal part": ""
        if len(parts) <= 2 or parts[2] == "zzz"
        else parts[2],
        "fourth principal part": ""
        if len(parts) <= 3 or parts[3] == "zzz"
        else parts[3],
        "part of speech": data[0],
        "which": data[1],
        "variation": data[2],
        "gender": data[3],
        "type": data[4],
        "age": tags[0],
        "area": tags[1],
        "geo": tags[2],
        "freq": tags[3],
        "source": tags[4],
        "definitions": definitions,
    }


def verb_handler(parts, data, tags, definitions):
    return {
        "first principal part": "" if parts[0] == "zzz" else parts[0],
        "second principal part": ""
        if len(parts) <= 1 or parts[1] == "zzz"
        else parts[1],
        "third principal part": ""
        if len(parts) <= 2 or parts[2] == "zzz"
        else parts[2],
        "fourth principal part": ""
        if len(parts) <= 3 or parts[3] == "zzz"
        else parts[3],
        "part of speech": data[0],
        "which": data[1],
        "variation": data[2],
        "type": data[3],
        "age": tags[0],
        "area": tags[1],
        "geo": tags[2],
        "freq": tags[3],
        "source": tags[4],
        "definitions": definitions,
    }


# and pron
def adj_handler(parts, data, tags, definitions):
    return {
        "first principal part": "" if parts[0] == "zzz" else parts[0],
        "second principal part": ""
        if len(parts) <= 1 or parts[1] == "zzz"
        else parts[1],
        "third principal part": ""
        if len(parts) <= 2 or parts[2] == "zzz"
        else parts[2],
        "fourth principal part": ""
        if len(parts) <= 3 or parts[3] == "zzz"
        else parts[3],
        "part of speech": data[0],
        "which": data[1],
        "variation": data[2],
        "type": data[3],
        "age": tags[0],
        "area": tags[1],
        "geo": tags[2],
        "freq": tags[3],
        "source": tags[4],
        "definitions": definitions,
    }


# and prep
def adv_handler(parts, data, tags, definitions):
    return {
        "first principal part": "" if parts[0] == "zzz" else parts[0],
        "second principal part": ""
        if len(parts) <= 1 or parts[1] == "zzz"
        else parts[1],
        "third principal part": ""
        if len(parts) <= 2 or parts[2] == "zzz"
        else parts[2],
        "fourth principal part": ""
        if len(parts) <= 3 or parts[3] == "zzz"
        else parts[3],
        "part of speech": data[0],
        "type": data[1],
        "age": tags[0],
        "area": tags[1],
        "geo": tags[2],
        "freq": tags[3],
        "source": tags[4],
        "definitions": definitions,
    }


# and conj
def interj_handler(parts, data, tags, definitions):
    return {
        "first principal part": "" if parts[0] == "zzz" else parts[0],
        "second principal part": ""
        if len(parts) <= 1 or parts[1] == "zzz"
        else parts[1],
        "third principal part": ""
        if len(parts) <= 2 or parts[2] == "zzz"
        else parts[2],
        "fourth principal part": ""
        if len(parts) <= 3 or parts[3] == "zzz"
        else parts[3],
        "part of speech": data[0],
        "age": tags[0],
        "area": tags[1],
        "geo": tags[2],
        "freq": tags[3],
        "source": tags[4],
        "definitions": definitions,
    }


def num_handler(parts, data, tags, definitions):
    return {
        "first principal part": parts[0],
        "second principal part": parts[1] if len(parts) > 1 else "",
        "third principal part": parts[2] if len(parts) > 2 else "",
        "fourth principal part": parts[3] if len(parts) > 3 else "",
        "part of speech": data[0],
        "which": data[1],
        "variation": data[2],
        "type": data[3],
        "number": tags[0],
        "age": tags[1],
        "area": tags[2],
        "geo": tags[3],
        "freq": tags[4],
        "source": tags[5],
        "definitions": definitions,
    }


with open("data/DICTLINE.GEN") as f:
    lines = [
        line.strip()
        for line in f
        if len(line.strip()) > 0 and not line.startswith("--")
    ]

lines = [line.split("--")[0].strip() for line in lines]
lines = [line for line in lines if line]

# words = [(lines[i], lines[i+1], lines[i+2]) for i in range(0, len(lines), 3)]
output = []
types = set()

for item in lines:
    word_parts = item[:76].split()
    word_data = item[76:96].split()
    word_tags = item[96:110].split()
    definition_list = item[110:].split(";")
    definition_list = [re.sub(r"\(.*\)", "", d.strip()) for d in definition_list]
    definition_list = [d.strip() for d in definition_list if d]
    for _ in range(len(definition_list)):
        first_item = definition_list.pop(0)
        if first_item.startswith("+"):
            continue
        first_item_broken = [d.strip() for d in first_item.split(",")]
        definition_list.extend(first_item_broken)
    if definition_list and definition_list[0].startswith("|"):
        definition_list[0] = definition_list[0][1:]
    part_of_speech = word_data[0]
    types.add(part_of_speech)
    functions_to_use = {
        "V": verb_handler,
        "N": noun_handler,
        "PRON": adj_handler,
        "ADJ": adj_handler,
        "CONJ": interj_handler,
        "INTERJ": interj_handler,
        "PREP": adv_handler,
        "ADV": adv_handler,
        "NUM": num_handler,
        "PACK": adj_handler,
    }
    if part_of_speech in functions_to_use:
        # print(word_parts)
        word_info_for_json = functions_to_use[part_of_speech](
            word_parts, word_data, word_tags, definition_list
        )
        output.append(word_info_for_json)

print(types)
assert len(lines) == len(output)
# print(output)
# print(types)
with open("data/dictline.json", "w") as f:
    json.dump(output, f, indent=2)