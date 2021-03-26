"""
Item 8: Use zip to process iterators in parallel
"""

names  = ['cecilia', 'lise', 'marie']
counts = [len(n) for n in names]

for name, count in zip(names, counts):
    print(name, count)


"""
when the list are of irregular length
"""
from itertools import zip_longest

l1 = ['a', 'b', 'c', 'd']
l2 = [1, 2, 3, 4, 5, 6, 7]

for x, y in zip_longest(l1, l2):
    print(x, y)
