"""
1.12. determining the most frequent occurring items in a sequence

Problem: you have a sequence of items, and you'd like to determine the most frequent
         occuring items in the sequence.

Solution: The collections.Counter class is designed for just such a problem. It even
          comes with a handy most_common() method that will give you the answer.
"""

from collections import Counter

words = [
    'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
    'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
    'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
    'my', 'eyes', "you're", 'under'
]

morewords = ['why', 'are', 'you', 'not', 'looking', 'in', 'my', 'eyes']


word_counts = Counter(words)
print(f"Word count: {word_counts}")

# to get top 3 most counts
top_three = word_counts.most_common(3)
print(f"\nTop 3 counts: {top_three}\n\n")

# A little-known feature of Counter instances is that they can be easily combined using
# various mathematical operations.
a = Counter(words)
b = Counter(morewords)
print(f"Counter (A): {a}\n")
print(f"Counter (B): {b}\n")

# combine counts
c = a + b
print(f"Combine counts: {c}\n")

# subtract counts
d = a - b
print(f"Subtract counts: {d}\n")
print("- " * 50)
# =======================================================================================

"""
1.13. sorting a list of dictionary by a common key

Problem: you have a list of dictionaries and you would like to sort the entries
         according to one or more of the dictionary values.

Solution: sorting this type of structure is easy using the operator module's
          itemgetter function. Let's say you've queried a database table to get
          a listing of the members on your website, and you receive the following
          data structure in return.
"""

from operator import itemgetter

rows = [{'fname':'Brian', 'lname': 'Jones', 'uid': 1003},
        {'fname':'David', 'lname': 'Beazley', 'uid': 1002},
        {'fname':'John', 'lname': 'Cleese', 'uid': 1001},
        {'fname':'Big', 'lname': 'Jones', 'uid': 1004}]

rows_by_uid   = sorted(rows, key=itemgetter('uid'))
rows_by_fname = sorted(rows, key=itemgetter('fname'))
print(f"Rows by UID: {rows_by_uid}\n")
print(f"Rows by fname: {rows_by_fname}\n")

# the itemgetter() function can also accept multiple keys.
rows_by_lfname = sorted(rows, key=itemgetter('lname', 'fname'))
print(f'Rows by last then first name: {rows_by_lfname}\n')

# The operator.itemgetter() function takes as arguments the lookup indices used to
# extract the desired values from the records in rows . It can be a dictionary key name, a
# numeric list element, or any value that can be fed to an object’s __getitem__() method.
# If you give multiple indices to itemgetter() , the callable it produces will return a tuple
# with all of the elements in it, and sorted() will order the output according to the sorted
# order of the tuples. This can be useful if you want to simultaneously sort on multiple
# fields (such as last and first name, as shown in the example).

# the problem can be solved using lambda keys aswell, but itemgetter is bit faster
rows_by_fname = sorted(rows, key=lambda r: r['fname'])
rows_by_lfname = sorted(rows, key=lambda r: (r['lname'],r['fname']))

# it works with min and max function aswell
min(rows, key=itemgetter('uid'))
max(rows, key=itemgetter('uid'))
print("- " * 50)
# =======================================================================================


"""
1.14. Sorting objects without native comparison support

Problem: you want to sort objects of the same class, but they don't natively support
         comparison operation
"""

from operator import attrgetter

class User:
    def __init__(self, user_id) -> None:
        self.user_id = user_id

    def __repr__(self) -> str:
        return f'User({self.user_id})'

users = [User(23), User(3), User(99)]
print(f"Users: {users}")

# sorting objects using lambda
print(f"sorting using lambda: {sorted(users, key=lambda u: u.user_id)}")

# instead of using lambda, an alternative approach is to use operator.attrgetter()
print(f"sorted using attrgetter: {sorted(users, key=attrgetter('user_id'))}")

# The choice of whether or not to use lambda or attrgetter() may be one of personal
# preference. However, attrgetter() is often a tad bit faster and also has the added
# feature of allowing multiple fields to be extracted simultaneously. This is analogous to
# the use of operator.itemgetter() for dictionaries
