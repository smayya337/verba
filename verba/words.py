# type: ignore

class Word:
    """A Latin word."""

    classical_latin = {
        "A": "A",
        "a": "a",
        "B": "B",
        "b": "b",
        "C": "C",
        "c": "c",
        "D": "D",
        "d": "d",
        "E": "E",
        "e": "e",
        "F": "F",
        "f": "f",
        "G": "G",
        "g": "g",
        "H": "H",
        "h": "h",
        "I": "I",
        "i": "i",
        "J": "I",
        "j": "i",
        "K": "K",
        "k": "k",
        "L": "L",
        "l": "l",
        "M": "M",
        "m": "m",
        "N": "N",
        "n": "n",
        "O": "O",
        "o": "o",
        "P": "P",
        "p": "p",
        "Q": "Q",
        "q": "q",
        "R": "R",
        "r": "r",
        "S": "S",
        "s": "s",
        "T": "T",
        "t": "t",
        "U": "U",
        "u": "u",
        "V": "V",
        "v": "v",
        "W": "W",
        "w": "w",
        "X": "X",
        "x": "x",
        "Y": "Y",
        "y": "y",
        "Z": "Z",
        "z": "z",
        "Ā": "A",
        "Ē": "E",
        "Ī": "I",
        "Ō": "O",
        "Ū": "U",
        "Ȳ": "Y",
        "ā": "a",
        "ē": "e",
        "ī": "i",
        "ō": "o",
        "ū": "u",
        "ȳ": "y",
    }

    def __init__(self, target, stem, ending, prefix=None, suffix=None, tackon=None):
        self.prefix = prefix
        self.stem = stem
        self.ending = ending
        self.suffix = suffix
        self.tackon = tackon
        self.target = target
        if ending:
            assert (
                Word.part_of_speech_matches(
                    self.stem["part of speech"], self.ending["part of speech"]
                )
                or (
                    self.stem["part of speech"] == "V"
                    and self.ending["part of speech"] == "SUPINE"
                )
                or (
                    self.stem["part of speech"] == "PACK"
                    and self.ending["part of speech"] == "PRON"
                )
                or (
                    self.stem["part of speech"] == "V"
                    and self.ending["part of speech"] == "VPAR"
                )
            ), "The stem and ending of this word are incompatible!"
        if prefix:
            assert Word.part_of_speech_matches(
                self.stem["part of speech"], self.prefix["from"]
            ), "The stem and prefix of this word are incompatible!"
        if suffix:
            assert Word.part_of_speech_matches(
                self.stem["part of speech"], self.suffix["from"]
            ), "The stem and suffix of this word are incompatible!"
        if tackon:
            assert Word.part_of_speech_matches(
                self.stem["part of speech"], self.tackon["with"]
            ), "The stem and tackon of this word are incompatible!"
            if "with_type" in self.tackon:
                assert (
                    self.stem["type"] == self.tackon["with_type"]
                ), "The stem and tackon of this word are incompatible!"
        self.which, self.variation = Word.which_and_variation(
            self.stem, self.ending, self.prefix, self.suffix, self.tackon
        )
        self.gender = Word.gender(
            self.stem, self.ending, self.prefix, self.suffix, self.tackon
        )
        self.create_word()

    def create_word(self):
        if "principal parts" in self.stem:
            if self.suffix and "from_part" in self.suffix:
                self.word = self.stem["principal parts"][self.suffix["from_part"] - 1]
            elif self.ending:
                self.word = self.stem["principal parts"][self.ending.get("key", 1) - 1]
            else:
                self.word = self.stem["principal parts"][0]
        else:
            self.word = self.stem["word"]
        if self.prefix:
            self.word = self.prefix["word"] + self.prefix.get("connect", "") + self.word
        if self.suffix:
            self.word = self.word + self.suffix.get("connect", "") + self.suffix["word"]
        if self.ending:
            self.word += self.ending["ending"]
        if self.tackon:
            self.word += self.tackon["word"]
        self.word = Word.convert_to_classical_latin(self.word)
        assert (
            self.word.lower() == self.target.lower()
        ), "The constructed word does not match the target!"

    @staticmethod
    def gender_matches(gender_1: str, gender_2: str) -> bool:
        if gender_1 == gender_2:
            return True
        gender_list = {gender_1, gender_2}
        if "X" in gender_list:
            return True
        if "C" in gender_list and "N" not in gender_list:
            return True
        return False

    @staticmethod
    def part_of_speech_matches(part_of_speech_1: str, part_of_speech_2: str) -> bool:
        if part_of_speech_1 == part_of_speech_2:
            return True
        part_of_speech_set = {part_of_speech_1, part_of_speech_2}
        if "X" in part_of_speech_set:
            return True
        return False

    @staticmethod
    def category_matches(cat_1: tuple, cat_2: tuple) -> bool:
        booleans = []
        zipped_categories = zip(cat_1, cat_2)
        for category in zipped_categories:
            val_1, val_2 = category
            if 0 in category:
                booleans.append(True)
            elif val_1 == val_2:
                booleans.append(True)
            else:
                booleans.append(False)
        return False not in booleans

    @staticmethod
    def part_of_speech(stem=None, ending=None, prefix=None, suffix=None, tackon=None):
        if stem:
            part_of_speech = stem["part of speech"]
        else:
            part_of_speech = "X"
        if ending and ending["part of speech"] != "X":
            if part_of_speech == "X":
                part_of_speech = ending["part of speech"]
            elif ending["part of speech"] == "SUPINE":
                part_of_speech = "SUPINE"
            elif ending["part of speech"] == "VPAR":
                part_of_speech = "VPAR"
            assert Word.part_of_speech_matches(
                part_of_speech, ending["part of speech"]
            ) or (part_of_speech == "PACK" and ending["part of speech"] == "PRON")
        if prefix:
            assert (
                Word.part_of_speech_matches(part_of_speech, prefix["from"])
                or part_of_speech == "X"
            )
            if prefix["to"] != "X":
                part_of_speech = prefix["to"]
        if suffix:
            assert (
                Word.part_of_speech_matches(part_of_speech, suffix["from"])
                or part_of_speech == "X"
            )
            if suffix["to"] != "X":
                part_of_speech = suffix["to"]
        if tackon:
            assert (
                Word.part_of_speech_matches(part_of_speech, tackon["with"])
                or part_of_speech == "X"
                or tackon["with"] == "X"
            )
        return part_of_speech

    @staticmethod
    def which_and_variation(
        stem=None, ending=None, prefix=None, suffix=None, tackon=None
    ):
        which = 0
        variation = 0
        if stem and "which" in stem and "variation" in stem:
            which = stem["which"]
            variation = stem["variation"]
        if ending and "which" in ending and "variation" in ending:
            assert Word.category_matches(
                (which, variation),
                (
                    ending["which"],
                    ending["variation"],
                ),
            ), "The parts of this word cannot be reconciled!"
        if (
            suffix
            and "from_which" in suffix
            and "from_variation" in suffix
            and "to_which" in suffix
            and "to_variation" in suffix
        ):
            assert Word.category_matches(
                (which, variation),
                (
                    suffix["from_which"],
                    suffix["from_variation"],
                ),
            ), "The parts of this word cannot be reconciled!"
            which = suffix["to_which"]
            variation = suffix["to_variation"]
        if (
            prefix
            and "from_which" in prefix
            and "from_variation" in prefix
            and "to_which" in prefix
            and "to_variation" in prefix
        ):
            assert Word.category_matches(
                (which, variation),
                (
                    prefix["from_which"],
                    prefix["from_variation"],
                ),
            ), "The parts of this word cannot be reconciled!"
            which = prefix["to_which"]
            variation = prefix["to_variation"]
        if tackon and "with_which" in tackon and "with_variation" in tackon:
            assert Word.category_matches(
                (which, variation),
                (
                    tackon["with_which"],
                    tackon["with_variation"],
                ),
            ), "The parts of this word cannot be reconciled!"
        return which, variation

    @staticmethod
    def gender(stem=None, ending=None, prefix=None, suffix=None, tackon=None):
        gender = "X"
        if stem and "gender" in stem:
            gender = stem["gender"]
        else:
            return "X"
        if ending and "gender" in ending:
            assert Word.gender_matches(
                gender, ending["gender"]
            ), "The parts of this word cannot be reconciled!"
        if suffix:
            if "from_gender" in suffix:
                assert Word.gender_matches(
                    gender, suffix["from_gender"]
                ), "The parts of this word cannot be reconciled!"
            if "to_gender" in suffix:
                gender = suffix["to_gender"]
        if prefix:
            if "from_gender" in prefix:
                assert Word.gender_matches(
                    gender, prefix["from_gender"]
                ), "The parts of this word cannot be reconciled!"
            if "to_gender" in prefix:
                gender = prefix["to_gender"]
        if tackon:
            if "from_gender" in tackon:
                assert Word.gender_matches(
                    gender, tackon["from_gender"]
                ), "The parts of this word cannot be reconciled!"
            if "to_gender" in tackon:
                gender = tackon["to_gender"]
        return gender

    @staticmethod
    def valid(stem=None, ending=None, prefix=None, suffix=None, tackon=None):
        try:
            Word.part_of_speech(stem, ending, prefix, suffix, tackon)
            Word.which_and_variation(stem, ending, prefix, suffix, tackon)
            Word.gender(stem, ending, prefix, suffix, tackon)
        except AssertionError:
            return False
        return True

    @staticmethod
    def convert_to_classical_latin(word):
        return "".join([Word.classical_latin.get(c, c) for c in word])

    def __eq__(self, other):
        return (
            self.stem == other.stem
            and self.ending == other.ending
            and self.prefix == other.prefix
            and self.suffix == other.suffix
            and self.tackon == other.tackon
        )

    def __repr__(self):
        return f"{type(self).__name__} {self.word}"

    def __str__(self):
        return f"{type(self).__name__} {self.word}"


class Noun(Word):
    def __init__(
        self, target, stem, ending=None, prefix=None, suffix=None, tackon=None
    ):
        super().__init__(target, stem, ending, prefix, suffix, tackon)
        if self.ending:
            assert Word.category_matches(
                (self.stem["which"], self.stem["variation"]),
                (
                    self.ending["which"],
                    self.ending["variation"],
                ),
            ), "The stem and ending of this word are incompatible!"
            if "gender" in self.stem and "gender" in self.ending:
                assert Word.gender_matches(
                    self.stem["gender"], self.ending["gender"]
                ), "The stem and ending of this word are incompatible!"


class Verb(Word):
    def __init__(
        self, target, stem, ending=None, prefix=None, suffix=None, tackon=None
    ):
        super().__init__(target, stem, ending, prefix, suffix, tackon)
        if self.ending:
            assert Word.category_matches(
                (self.stem["which"], self.stem["variation"]),
                (
                    self.ending["which"],
                    self.ending["variation"],
                ),
            ), "The stem and ending of this word are incompatible!"
            if "gender" in self.stem and "gender" in self.ending:
                assert Word.gender_matches(
                    self.stem["gender"], self.ending["gender"]
                ), "The stem and ending of this word are incompatible!"


class Adjective(Word):
    def __init__(
        self, target, stem, ending=None, prefix=None, suffix=None, tackon=None
    ):
        super().__init__(target, stem, ending, prefix, suffix, tackon)
        if self.ending:
            assert Word.category_matches(
                (self.stem["which"], self.stem["variation"]),
                (
                    self.ending["which"],
                    self.ending["variation"],
                ),
            ), "The stem and ending of this word are incompatible!"
            if "gender" in self.stem and "gender" in self.ending:
                assert Word.gender_matches(
                    self.stem["gender"], self.ending["gender"]
                ), "The stem and ending of this word are incompatible!"


class Adverb(Word):
    def __init__(
        self, target, stem, ending=None, prefix=None, suffix=None, tackon=None
    ):
        super().__init__(target, stem, ending, prefix, suffix, tackon)


class Preposition(Word):
    def __init__(
        self, target, stem, ending=None, prefix=None, suffix=None, tackon=None
    ):
        super().__init__(target, stem, ending, prefix, suffix, tackon)


class Conjunction(Word):
    def __init__(
        self, target, stem, ending=None, prefix=None, suffix=None, tackon=None
    ):
        super().__init__(target, stem, ending, prefix, suffix, tackon)


class Interjection(Word):
    def __init__(
        self, target, stem, ending=None, prefix=None, suffix=None, tackon=None
    ):
        super().__init__(target, stem, ending, prefix, suffix, tackon)


class Pronoun(Word):
    def __init__(
        self, target, stem, ending=None, prefix=None, suffix=None, tackon=None
    ):
        super().__init__(target, stem, ending, prefix, suffix, tackon)
        if self.ending:
            assert (self.stem["which"], self.stem["variation"]) == (
                self.ending["which"],
                self.ending["variation"],
            ), "The stem and ending of this word are incompatible!"
            if "gender" in self.stem and "gender" in self.ending:
                assert Word.gender_matches(
                    self.stem["gender"], self.ending["gender"]
                ), "The stem and ending of this word are incompatible!"


class Number(Word):
    def __init__(
        self, target, stem, ending=None, prefix=None, suffix=None, tackon=None
    ):
        super().__init__(target, stem, ending, prefix, suffix, tackon)
        if self.ending:
            assert Word.category_matches(
                (self.stem["which"], self.stem["variation"]),
                (
                    self.ending["which"],
                    self.ending["variation"],
                ),
            ), "The stem and ending of this word are incompatible!"
            if "gender" in self.stem and "gender" in self.ending:
                assert Word.gender_matches(
                    self.stem["gender"], self.ending["gender"]
                ), "The stem and ending of this word are incompatible!"


class Supine(Word):
    def __init__(
        self, target, stem, ending=None, prefix=None, suffix=None, tackon=None
    ):
        super().__init__(target, stem, ending, prefix, suffix, tackon)


class Pack(Word):
    def __init__(
        self, target, stem, ending=None, prefix=None, suffix=None, tackon=None
    ):
        super().__init__(target, stem, ending, prefix, suffix, tackon)


class VerbParticiple(Word):
    def __init__(
        self, target, stem, ending=None, prefix=None, suffix=None, tackon=None
    ):
        super().__init__(target, stem, ending, prefix, suffix, tackon)
