# type: ignore

from verba.words import *
from thefuzz import fuzz, process
import json
import os
import time


class Solver:
    parts_of_speech_to_classes = {
        "N": Noun,
        "V": Verb,
        "ADJ": Adjective,
        "ADV": Adverb,
        "PRON": Pronoun,
        "CONJ": Conjunction,
        "INTERJ": Interjection,
        "PREP": Preposition,
        "NUM": Number,
        "PACK": Pack,
        "SUPINE": Supine,
    }

    def __init__(self):
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        with open(os.path.join(data_dir, "addons.json")) as f:
            self.prefixes = {}
            self.suffixes = {}
            self.tackons = {}
            for a in json.load(f):
                addon = a["word"]
                if a["type"] == "prefix":
                    if addon not in self.prefixes:
                        self.prefixes[addon] = []
                    self.prefixes[addon].append(a)
                elif a["type"] == "suffix":
                    if addon not in self.suffixes:
                        self.suffixes[addon] = []
                    self.suffixes[addon].append(a)
                elif a["type"] == "tackon":
                    if addon not in self.tackons:
                        self.tackons[addon] = []
                    self.tackons[addon].append(a)
        with open(os.path.join(data_dir, "dictline.json")) as f:
            dictline = json.load(f)
            self.dictline = {}
            for d in dictline:
                for p in d["principal parts"]:
                    if p:
                        if p not in self.dictline:
                            self.dictline[p] = []
                        self.dictline[p].append(d)
        with open(os.path.join(data_dir, "inflections.json")) as f:
            self.inflections = {}
            for i in json.load(f):
                if i["ending"] not in self.inflections:
                    self.inflections[i["ending"]] = []
                self.inflections[i["ending"]].append(i)
        with open(os.path.join(data_dir, "uniques.json")) as f:
            self.uniques = {}
            for u in json.load(f):
                if u["word"] not in self.uniques:
                    self.uniques[u["word"]] = []
                self.uniques[u["word"]].append(u)

    @staticmethod
    def _part_of_speech(stem, suffix=None):
        if suffix:
            return suffix["to"]
        return stem["part of speech"]

    def solve(self, target_word: str) -> list[Word]:
        output_words = []
        # something goes here
        return output_words
