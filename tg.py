import sys
from itertools import chain
import pickle
from tqdm import tqdm

# s = sys.argv[1]

all_numbers = [str(x).zfill(4) for x in list(range(10000))]
target = 10
dictionary = {}

for s in tqdm(all_numbers):
    # target = int(sys.argv[2])
    numbers = [int(x) for x in list(s)]

    op_chars = list('+-/*') + ['/-','*-']

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
    # print('\n'.join(results))
    dictionary[s] = results

with open('all_solns.pkl','wb') as f:
    pickle.dump(dictionary,f)