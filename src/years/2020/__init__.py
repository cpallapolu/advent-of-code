import sys

from os import listdir
from os.path import abspath, dirname

puzzles_path = dirname(abspath(__file__))

solutions = [
    f'{f}.solution'
    for f in listdir(puzzles_path)
    if f.startswith('__') is False and f.startswith('settings') is False
]

for solution in solutions:
    mod = __import__('.'.join([__name__, solution]), fromlist=[solution])
    classes = [getattr(mod, x) for x in dir(mod) if isinstance(getattr(mod, x), type)]

    for cls in classes:
        if cls.__name__ != 'AoCPuzzle':
            setattr(sys.modules[__name__], cls.__name__, cls)
