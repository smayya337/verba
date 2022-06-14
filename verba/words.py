# type: ignore


class Word:
    """A Latin word."""

    def __init__(self, target, stem, ending, prefix=None, suffix=None, tackon=None):
        self.prefix = prefix
        self.stem = stem
        self.ending = ending
        self.suffix = suffix
        self.tackon = tackon
        self.target = target
        if ending:
            assert Word.part_of_speech_matches(
                stem["part of speech"], ending["part of speech"]
            ), "The stem and ending of this word are incompatible!"
        if prefix:
            assert Word.part_of_speech_matches(
                stem["part of speech"], prefix["from"]
            ), "The stem and prefix of this word are incompatible!"
        if suffix:
            assert Word.part_of_speech_matches(
                stem["part of speech"], suffix["from"]
            ), "The stem and suffix of this word are incompatible!"
        if tackon:
            assert Word.part_of_speech_matches(
                stem["part of speech"], tackon["with"]
            ), "The stem and tackon of this word are incompatible!"

    @classmethod
    def gender_matches(cls, gender_1: str, gender_2: str) -> bool:
        if gender_1 == gender_2:
            return True
        gender_list = {gender_1, gender_2}
        if "X" in gender_list:
            return True
        if "C" in gender_list and "N" not in gender_list:
            return True
        return False

    @classmethod
    def part_of_speech_matches(
        cls, part_of_speech_1: str, part_of_speech_2: str
    ) -> bool:
        if part_of_speech_1 == part_of_speech_2:
            return True
        part_of_speech_list = {part_of_speech_1, part_of_speech_2}
        if "X" in part_of_speech_list:
            return True
        return False


class Noun(Word):
    def __init__(self, target, stem, ending, prefix=None, suffix=None, tackon=None):
        super().__init__(target, stem, ending, prefix, suffix, tackon)
        assert (self.stem["which"], self.stem["variation"]) == (
            self.ending["which"],
            self.ending["variation"],
        ), "The stem and ending of this word are incompatible!"
        assert Word.gender_matches(
            self.stem["gender"], self.ending["gender"]
        ), "The stem and ending of this word are incompatible!"
        self.word = self.stem["principal parts"][self.ending["key"] - 1]
        self.word += self.ending["ending"]
        if self.prefix:
            self.word = self.prefix["word"] + self.prefix.get("connect", "") + self.word
        if self.suffix:
            self.word = self.word + self.suffix.get("connect", "") + self.suffix["word"]
        if self.tackon:
            self.word += self.tackon["word"]


class Verb(Word):
    def __init__(self, target, stem, ending, prefix=None, suffix=None, tackon=None):
        super().__init__(target, stem, ending, prefix, suffix, tackon)


class Adjective(Word):
    def __init__(self, target, stem, ending, prefix=None, suffix=None, tackon=None):
        super().__init__(target, stem, ending, prefix, suffix, tackon)


class Adverb(Word):
    def __init__(self, target, stem, ending, prefix=None, suffix=None, tackon=None):
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
    def __init__(self, target, stem, ending, prefix=None, suffix=None, tackon=None):
        super().__init__(target, stem, ending, prefix, suffix, tackon)


class Number(Word):
    def __init__(self, target, stem, ending, prefix=None, suffix=None, tackon=None):
        super().__init__(target, stem, ending, prefix, suffix, tackon)


class Supine(Word):
    def __init__(self, target, stem, ending, prefix=None, suffix=None, tackon=None):
        super().__init__(target, stem, ending, prefix, suffix, tackon)


class Pack(Word):
    def __init__(self, target, stem, ending, prefix=None, suffix=None, tackon=None):
        super().__init__(target, stem, ending, prefix, suffix, tackon)
