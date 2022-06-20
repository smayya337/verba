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


    def remove_suffixes(self, target_word, tackon, prefix, ending):
        all_words = []
        for suffix_key, suffix_values in self.suffixes.items():
            if target_word.endswith(suffix_key):
                for suffix_data in suffix_values:
                    suffix = suffix_data.get("connect", "") + suffix_key
                    if target_word.endswith(suffix):
                        pass
        return all_words


    def remove_endings(self, target_word, tackon, prefix):
        all_words = []
        for ending_key, ending_values in self.inflections.items():
            if target_word.endswith(ending_key):
                for ending_data in ending_values:
                    pass
        return all_words


    def remove_prefixes(self, target_word, tackon):
        all_words = []
        for prefix_key, prefix_values in self.prefixes.items():
            if target_word.startswith(prefix_key):
                for prefix_data in prefix_values:
                    prefix = prefix_key + prefix_data.get("connect", "")
                    if target_word.startswith(prefix):
                        # step 3 needs to be added here
                        all_words.append(self.remove_endings(target_word[len(prefix):], tackon, prefix_data))
        all_words.append(self.remove_endings(target_word, tackon, None))
        return all_words


    def remove_tackons(self, target_word):
        all_words = []
        for tackon_key, tackon_values in self.tackons.items():
            target_word = original
            if target_word.endswith(tackon_key):
                for tackon_data in tackon_values:
                    all_words.extend(self.remove_prefixes(target_word[:-len(tackon_key)], tackon_data))
        all_words.extend(self.remove_prefixes(target_word, None))
        return all_words


    def solve(self, target_word: str) -> list[Word]:
        """
        The meat of the solver system goes here.
        How do we organize this?

        1. Check if the word is an unique to begin with.
        2. Split the word up.
            a. Find the tackons (e.g. -que) at the end of the word. If they exist, separate them from the rest of the word.
            b. Find the prefixes (e.g. ad-) at the beginning of the word. If they exist, separate them from the rest of the word.
        3. This will leave a stem, suffix, and ending (or at least some combination of the three). Let's check if the word is in the list of uniques. If so, add it to the list.
        4. Now, we want to go through the general list of words.
            a. First, let's remove the ending from the whole bunch. Check if it's a valid ending. If not, we're probably done.
            b. If it is a valid ending, let's remove it from everything else and see if we have a suffix here.
            c. Let's figure out what stem we have.
                1. If we have a suffix (e.g. -an-), let's remove it from the stem and check what kind of stem we have here. We can filter by part of speech (using the suffix's "from" key).
                2. If we don't have a suffix, let's just check the stem normally. We filter by part of speech of the ending.
        5. If we manage to get valid items for all of these, we did it! Let's add every valid combination of the items to the list.
        A combination is valid if it does not fail during creation (we'll need a try-except block here) and the constructed word matches the target (checked during creation).
        6. Once we're done, we return the list of potential words.

        Some notes:
        * Runtime will suck. This could very well be O(n^5).
        * We will need to filter by part of speech extensively. Doing this for many words in sequence will take a lot of time. Can we refactor at some point to categorize everything during load?
        * Valid keys for part-of-speech filtering:
            * prefix: from
            * stem: part of speech
            * suffix: from
            * ending: part of speech
            * tackon: with
        """
        output_words = []
        # # step 1
        if target_word in self.uniques:
            for u in self.uniques[target_word]:
                output_words.append(self.parts_of_speech_to_classes[u["part of speech"]](u))
        # # step 2a
        # for tackon_key, tackon_values in self.tackons.items():
        #     target_word = original
        #     if target_word.endswith(tackon_key):
        #         target_word_no_tackon = target_word[:-len(tackon_key)]
        #         # step 2b
        #         for prefix_key, prefix_values in self.prefixes.items():
        #             for prefix_data in prefix_values:
        #                 prefix = prefix_key + prefix_data.get("connect", "")
        #                 if target_word_no_tackon.startswith(prefix):
        #                     target_word_no_tackon = target_word_no_tackon[len(prefix):]
        #                 # step 3
        #                 if target_word in self.uniques:
        #                     for u in self.uniques[target_word]:
        #                         output_words.append(self.parts_of_speech_to_classes[u["part of speech"]](u))
        #                 # step 4a
        #                 for ending_key, ending_values in self.inflections.items():
        #                     if target_word.endswith(ending_key):
        output_words.extend(self.remove_tackons(target_word))
        return output_words
