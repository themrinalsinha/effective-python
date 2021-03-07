"""
4.8 Skipping the first part of an iterable

Problem: You want to iterate over items in an iterable, but the first few items aren't
         of interest and you just want to discard them.

Solution: The itertools module has a few functions that can be used to address this task.
          The first itertools.dropwhile() function. To use it, you supply a function and
          an iterable. The returned iterator discards the first items in the sequence as
          long as the supplied function returns True.
"""

with open('/etc/passwd') as f:
    for line in f:
        print(line, end='')


# --------------------------------------------------------------
from itertools import dropwhile, permutations

with open("/etc/passwd") as f:
    for line in dropwhile(lambda line: line.startswith('#'), f):
        print(line, end='')
print()


# --------------------------------------------------------------
from itertools import islice

items = ['a', 'b', 'c', 'd', 'e', 1, 2, 3, 4, 5]
for x in islice(items, 3, None):
    print(x)
print()

# --------------------------------------------------------------
print()
# ======================================================================================


"""
4.9 Iterating over all possible combinations or permutations

Problem: You want to iterate over all the possible combinations or permutations of a
         collection of items
"""
from itertools import permutations, combinations

items = ['a', 'b', 'c']

for p in permutations(items):
    print(p)

for p in permutations(items, 2):
    print(p)

for p in permutations(items, 1):
    print(p)


print()
for p in combinations(items, 3):
    print(p)

for p in combinations(items, 2):
    print(p)

for p in combinations(items, 1):
    print(p)

print()
# For combinations(), the actual order of the elements is not considered. That is, the
# combination('a', 'b') is considered to be the same as ('b', 'a').
from itertools import combinations_with_replacement

for p in combinations_with_replacement(items, 3):
    print(p)
print()
# =====================================================================================

"""
4.10. Iterating over the Index-Value pairs of a sequence

Problem: You want to iterate over a sequence, but would like to keep track of which element
         of the sequence is currently being processed.

Solution: the built-in enumerate() function handles this quite nicely
"""
my_list = ['a', 'b', 'c', 'd']
for idx, val in enumerate(my_list):
    print(idx, val)
print()

my_list = ['a', 'b', 'c', 'd']
for idx, val in enumerate(my_list, 1):
    print(idx, val)
print()
# ======================================================================================


