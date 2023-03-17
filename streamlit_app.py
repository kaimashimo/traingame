import streamlit as st
import re
from itertools import chain

def validate_input(s):
    return len(s) == 4 and re.match(r'^\d{4}$',s)

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

st.write('# Train Game Solver')

s = st.text_input('Write your four digit number here:')

if validate_input(s):
    target = 10
    op_chars = list('+-/*') + ['/-','*-']

    numbers = [int(x) for x in list(s)]

    

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
    if results:
        st.success('it is solvable!')
        go = st.button('see answers')
        if go:
            st.write(results)
    else:
        st.error('not solvable :(')