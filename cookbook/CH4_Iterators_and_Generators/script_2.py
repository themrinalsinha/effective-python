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
from itertools import dropwhile

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
