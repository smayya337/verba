from verba.solver import Solver
from verba.words import Word
import sys


target_word = sys.argv[1].strip()

solver: Solver = Solver()
matches: list[Word] = solver.solve(target_word)
