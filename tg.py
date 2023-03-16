import sys
from itertools import chain
import pickle
from tqdm import tqdm

s = sys.argv[1]
target = 10
dictionary = {}
op_chars = list('+-/*') + ['/-','*-']

numbers = [int(x) for x in list(s)]

def parenthesized (exprs):
    if len(exprs) == 1:
        yield exprs[0]
    else:
        first_exprs = []
        last_exprs = list(exprs)
        while 1 < len(last_exprs):
            first_exprs.append(last_exprs.pop(0))
            for x in parenthesized(first_exprs):
                if 1 < len(first_exprs):
                    x = '(%s)' % x
                for y in parenthesized(last_exprs):
                    if 1 < len(last_exprs):
                        y = '(%s)' % y
                    for op in op_chars:
                        yield '%s%s%s' % (x, op, y)

numbers_reflected = numbers[:]
numbers_reflected[0] = -numbers_reflected[0]

results = []

for x in chain(parenthesized(numbers), parenthesized(numbers_reflected)):
    try:
        if eval(x) == target:
            results.append(x)
        if -eval(x) == target:
            results.append('-('+x+')')
    except ZeroDivisionError:
        pass

results = sorted(list(set(results)))
print('\n'.join(results))