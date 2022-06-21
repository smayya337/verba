import time

from verba.solver import Solver
from verba.words import Word
import sys


target_words = sys.argv[1].strip().split()

solver_start = time.perf_counter()
solver: Solver = Solver()
print(f"Solver initialized in {time.perf_counter() - solver_start} seconds.")
for target_word in target_words:
    start = time.perf_counter()
    target_word = "".join([c for c in target_word if c in Word.classical_latin.keys()])
    word_to_process = Word.convert_to_classical_latin(target_word)
    matches = solver.solve(word_to_process)
    print(
        f"{len(matches)} matches for {target_word} in {time.perf_counter() - start} seconds."
    )
    # print()
    # for match in matches:
    #     print(match, match.stem, match.ending)
    #     print()
print(f"Operation complete in {time.perf_counter() - solver_start} seconds.")
