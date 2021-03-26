"""
Item 10: Prevent Repetition with assignment expressions


An assignment expression - also know as walrus operator - is a new syntax introduced
in python 3.8 to solve a long-standing problem with the language that can cause code
duplication.
"""

fresh_fruits = {
    'apple': 10,
    'banana': 8,
    'lemon': 5,
}

if count := fresh_fruits.get('lemon', 0):
    print('count....', count)
else:
    print(count)

"""
Things to Remember
✦ Assignment expressions use the walrus operator ( := ) to both assign
and evaluate variable names in a single expression, thus reducing
repetition.
✦ When an assignment expression is a subexpression of a larger
expression, it must be surrounded with parentheses.
✦ Although switch/case statements and do/while loops are not avail-
able in Python, their functionality can be emulated much more
clearly by using assignment expressions.
"""
