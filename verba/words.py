class Word:
    def __init__(self, stem, ending, prefix=None, suffix=None, tackon=None):
        self.prefix = prefix
        self.stem = stem
        self.ending = ending
        self.suffix = suffix
        self.tackon = tackon
        if ending:
            assert (
                stem["part of speech"] == ending["part of speech"] or ending["part of speech"] == "X"
            ), "The stem and ending of this word are incompatible!"
        if prefix:
            assert (
                stem["part of speech"] == prefix["from"] or prefix["from"] == "X"
            ), "The stem and prefix of this word are incompatible!"
        if suffix:
            assert (
                stem["part of speech"] == suffix["from"] or suffix["from"] == "X"
            ), "The stem and suffix of this word are incompatible!"
        if tackon:
            assert (
                stem["part of speech"] == tackon["with"] or tackon["with"] == "X"
            ), "The stem and tackon of this word are incompatible!"


class Noun(Word):
    def __init__(self, stem, ending, prefix=None, suffix=None, tackon=None):
        super().__init__(stem, ending, prefix, suffix, tackon)
        assert (self.stem["which"], self.stem["variation"]) == (
            self.ending["which"],
            self.ending["variation"],
        ), "The stem and ending of this word are incompatible!"


class Verb(Word):
    def __init__(self, stem, ending, prefix=None, suffix=None, tackon=None):
        super().__init__(stem, ending, prefix, suffix, tackon)


class Adjective(Word):
    def __init__(self, stem, ending, prefix=None, suffix=None, tackon=None):
        super().__init__(stem, ending, prefix, suffix, tackon)


class Adverb(Word):
    def __init__(self, stem, ending, prefix=None, suffix=None, tackon=None):
        super().__init__(stem, ending, prefix, suffix, tackon)


class Preposition(Word):
    def __init__(self, stem, ending=None, prefix=None, suffix=None, tackon=None):
        super().__init__(stem, ending, prefix, suffix, tackon)


class Conjunction(Word):
    def __init__(self, stem, ending=None, prefix=None, suffix=None, tackon=None):
        super().__init__(stem, ending, prefix, suffix, tackon)


class Interjection(Word):
    def __init__(self, stem, ending=None, prefix=None, suffix=None, tackon=None):
        super().__init__(stem, ending, prefix, suffix, tackon)


class Pronoun(Word):
    def __init__(self, stem, ending, prefix=None, suffix=None, tackon=None):
        super().__init__(stem, ending, prefix, suffix, tackon)


class Number(Word):
    def __init__(self, stem, ending, prefix=None, suffix=None, tackon=None):
        super().__init__(stem, ending, prefix, suffix, tackon)


class Supine(Word):
    def __init__(self, stem, ending, prefix=None, suffix=None, tackon=None):
        super().__init__(stem, ending, prefix, suffix, tackon)


class Pack(Word):
    def __init__(self, stem, ending, prefix=None, suffix=None, tackon=None):
        super().__init__(stem, ending, prefix, suffix, tackon)
