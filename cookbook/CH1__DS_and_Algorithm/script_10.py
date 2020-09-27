"""
1.15. grouping records together based on a field

Problem: you have a sequence of dictionaries or instance and you want to iterate
         over the data in groups based on the value of a particular field, such as date.

Solution: the itertools.groupby() function is particularly useful for grouping data together
          like this. To illustrate, suppose you have the following list of dictionaries.

The groupby() function works by scanning a sequence and finding sequential “runs”
of identical values (or values returned by the given key function). On each iteration, it
returns the value along with an iterator that produces all of the items in a group with
the same value.

An important preliminary step is sorting the data according to the field of interest. Since
groupby() only examines consecutive items, failing to sort first won’t group the records
as you want.
"""

from operator    import itemgetter
from itertools   import groupby
from collections import defaultdict

rows = [
    {'address': '5412 N CLARK', 'date': '07/01/2012'},
    {'address': '5148 N CLARK', 'date': '07/04/2012'},
    {'address': '5800 E 58TH', 'date': '07/02/2012'},
    {'address': '2122 N CLARK', 'date': '07/03/2012'},
    {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'},
    {'address': '1060 W ADDISON', 'date': '07/02/2012'},
    {'address': '4801 N BROADWAY', 'date': '07/01/2012'},
    {'address': '1039 W GRANVILLE', 'date': '07/04/2012'},
]

# sort by the desired field first
rows.sort(key=itemgetter('date'))

# iterate in group
for date, items in groupby(rows, key=itemgetter('date')):
    print(date)
    for item in items:
        print(f'\t{item}')

# If your goal is to simply group the data together by dates into a large data structure that
# allows random access, you may have better luck using defaultdict() to build a
# multidict
rows_by_date = defaultdict(list)
for row in rows:
    rows_by_date[row['date']].append(row)
print('- ' * 50)
# ======================================================================================

"""
1.16. Filtering sequence elements

Problems: you have data inside a sequence, and need to extract values or reduce the
          sequence using some criteria.
"""

# easy way
mylist = [1, 4, -5, 10, -7, 2, 3, -1]
print(f"no. > 0: {[n for n in mylist if n > 0]}")
print(f"no. < 0: {[n for n in mylist if n < 0]}")

# Sometimes, the filtering criteria cannot be easily expressed in a list comprehension or
# generator expression. For example, suppose that the filtering process involves exception
# handling or some other complicated detail. For this, put the filtering code into its own
# function and use the built-in filter() function.

values = ['1', '2', '-3', '-', '4', 'N/A', '5']

def is_int(val):
    try:
        x = int(val)
        return True
    except ValueError:
        return False

ivals = list(filter(is_int, values))
print(ivals)

# List comprehensions and generator expressions are often the easiest and most straight‐
# forward ways to filter simple data. They also have the added power to transform the
# data at the same time.

mylist = [1, 4, -5, 10, -7, 2, 3, -1]

import math
result = [math.sqrt(n) for n in mylist if n > 0]
print(f"\nPerforming mathematical operation: {result}")

clip_neg = [n if n > 0 else 0 for n in mylist]
clip_pos = [n if n < 0 else 0 for n in mylist]
print(f"{clip_neg} and {clip_pos}")

# Another notable filtering tool is itertools.compress() , which takes an iterable and
# an accompanying Boolean selector sequence as input. As output, it gives you all of the
# items in the iterable where the corresponding element in the selector is True . This can
# be useful if you’re trying to apply the results of filtering one sequence to another related
# sequence.

addresses = [
    '5412 N CLARK',
    '5148 N CLARK',
    '5800 E 58TH',
    '2122 N CLARK'
    '5645 N RAVENSWOOD',
    '1060 W ADDISON',
    '4801 N BROADWAY',
    '1039 W GRANVILLE',
]

counts = [ 0, 3, 10, 4, 1, 7, 6, 1]

# Now, suppose you want to make a list of all addresses where the corresponding
# count value was greater than 5. Here's how you could do it.

from itertools import compress
more5 = [n > 5 for n in counts]
print(f"\nmore5 --> {more5}")
print(f"using compress with more5: {list(compress(addresses, more5))}")

# The key here is to first create a sequence of Booleans that indicates which elements
# satisfy the desired condition. The compress() function then picks out the items corre‐
# sponding to True values.

# Like filter() , compress() normally returns an iterator. Thus, you need to use list()
# to turn the results into a list if desired
