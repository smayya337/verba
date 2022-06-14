import json
import re


def prefix_handler(word, data):
    word_type = word[0]
    word_name = word[1]
    word_connect = word[2] if len(word) > 2 else None
    output = {
        "type": word_type,
        "word": word_name,
        "from": data[0],
        "to": data[1],
    }
    if word_connect:
        output["connect"] = word_connect
    return output


def suffix_handler(word, data):
    word_type = word[0]
    word_name = word[1]
    word_connect = word[2] if len(word) > 2 else None
    output = {
        "type": word_type,
        "word": word_name,
        "from": data[0],
        "from_part": int(data[1]),
        "to": data[2],
    }
    if output["to"] == "V":
        output["to_which"] = int(data[3])
        output["to_variation"] = int(data[4])
    elif output["to"] == "N":
        output["to_which"] = int(data[3])
        output["to_variation"] = int(data[4])
        output["to_gender"] = data[5]
    elif output["to"] == "ADJ":
        output["to_which"] = int(data[3])
        output["to_variation"] = int(data[4])
    output["to_type"] = data[-2]
    output["to_key"] = int(data[-1])
    if word_connect:
        output["connect"] = word_connect
    return output


def tackon_handler(word, data):
    word_type = word[0]
    word_name = word[1]
    goes_with = data[0]
    output = {
        "type": word_type,
        "word": word_name,
        "with": goes_with,
    }
    if goes_with == "N":
        output["with_which"] = int(data[1])
        output["with_variation"] = int(data[2])
        output["with_gender"] = data[3]
        output["with_type"] = data[4]
    elif goes_with == "PRON":
        output["with_which"] = int(data[1])
        output["with_variation"] = int(data[2])
        output["with_type"] = data[3]
    elif goes_with == "ADJ":
        output["with_which"] = int(data[1])
        output["with_variation"] = int(data[2])
        output["with_type"] = data[3]
    elif goes_with == "PACK":
        output["with_which"] = int(data[1])
        output["with_variation"] = int(data[2])
        output["with_type"] = data[3]
    return output


with open("data/ADDONS.LAT") as f:
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
    word_overview = word.split()
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
    definition_list = [d.strip() for d in definition_list if d]
    functions_to_use = {
        "PREFIX": prefix_handler,
        "SUFFIX": suffix_handler,
        "TACKON": tackon_handler,
    }
    if word_overview[0] in functions_to_use:
        word_info_for_json = functions_to_use[word_overview[0]](
            word_overview, word_info
        )
        word_info_for_json["definitions"] = definition_list
        if word_overview[0] == "TACKON":
            word_info_for_json["tackon_type"] = definition_list[0].split(" ")[0]
            definition_list[0] = " ".join(definition_list[0].split(" ")[1:])
        output.append(word_info_for_json)
with open("data/addons.json", "w") as f:
    json.dump(output, f, indent=2)
