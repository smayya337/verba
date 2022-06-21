from verba.solver import Solver
from verba.words import Word
import sys


target_words = sys.argv[1].strip().split()

solver: Solver = Solver()
for target_word in target_words:
    target_word = "".join([c for c in target_word if c in Word.classical_latin.keys()])
    word_to_process = Word.convert_to_classical_latin(target_word)
    matches: list[Word] = solver.solve(word_to_process)
    print(f"{len(matches)} matches for {target_word}.")
    # print()
    # for match in matches:
    #     print(match, match.stem, match.ending)
    #     print()
