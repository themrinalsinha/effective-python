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
print()
# =======================================================================================

"""
4.13. Creating Data Processing Pipelines

Problem: You want to process data iteratively in the style of a data processing pipeline
         (similar to unix pipe). For instance, you have a huge amount of data that needs
         to be processed, but it can't fit entirely into memory.
"""
import os
import fnmatch
import gzip
import bz2
import re

def gen_find(filepat, top):
    """
    Find all filenames in a directory tree that match a shell wildcard pattern
    """
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path, name)


def gen_opener(filenames):
    """
    Open a sequence of filename one at a time producing a file object. The file is
    closed immediately when proceeding to the next iteration.
    """
    for filename in filenames:
        if filename.endswith('.gz'):
            f = gzip.open(filename, 'rt')
        elif filename.endswith('.bz2'):
            f = bz2.open(filename, 'rt')
        else:
            f = open(filename, 'rt')
        yield f
        f.close()


def gen_concatenate(iterators):
    """
    Chain a sequence of iterators together into a single sequence
    """
    for it in iterators:
        yield from it


def gen_grep(pattern, lines):
    """
    Look for regrex pattern is a sequence of lines
    """
    pat = re.compile(pattern)
    for line in lines:
        if pat.search(line):
            yield line


# You can now easily stack these functions together to make a processing pipeline.
# Eg: to find all log lines that contain the word python, you would just do this.
lognames = gen_find('access-log*', 'www')
files = gen_opener(lognames)
lines = gen_concatenate(files)
pylines = gen_grep('(?i)python', lines)
for line in pylines:
    print(line)

# if you want to extend the pipeline further, you can even feed the data in generator
# expressions. Eg: the version finds the number of bytes transferred and sums the total
lognames = gen_find('access-log*', 'www')
files = gen_opener(lognames)
lines = gen_concatenate(files)
pylines = gen_grep('(?i)python', lines)
bytecolumn = (line.rsplit(None, 1)[1] for line in pylines)
bytes = (int(x) for x in bytecolumn if x != '-')
print('Total: ', sum(bytes))
