"""
4.12. Iterating on Items in separate containers

Problem: You need to perform the same operation on many objects, but the objects are
         contained in different containers, and you'd like to avoid nested loops while
         without losing the readability of your code

Solution: itertools.chain()
"""

from itertools import chain

a = [1, 2, 3, 4]
b = ['x', 'y', 'z']

for x in chain(a, b):
    print(x)

# A common use of chain() is in programs where you would like to perform certain
# operations on all of the items at once but the items are pooled into different working
# sets.

# # Inefficent
# for x in a + b:
# ...
# # Better
# for x in chain(a, b):
# ...
