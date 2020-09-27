"""
1.17. extracting a subset of a dictionary

problem: you want to make a dictionary that is a subset of another dictionary
"""

prices = {
    'ACME': 45.23,
    'AAPL': 612.78,
    'IBM': 205.55,
    'HPQ': 37.20,
    'FB': 10.75
}

p1 = { key:value for key, value in prices.items() if value > 200 }
print(f"making dictionary of price over 200: {p1}")

# make a dictionary of tech stocks
tech_names = ['AAPL', 'IBM', 'HPQ', 'MSFT']
p2 = { key:value for key, value in prices.items() if key in tech_names }
print(f"filtering tech stocks: {p2}")
# or another way to do the same thing
p3 = { key:prices[key] for key in prices.keys() & tech_names }
print(f"filtering tech stock (method2): {p3}")
print('- ' * 50)
# ===============================================================================

"""
1.18. mapping names to sequence elements

problem: You have code that accesses list or tuple elements by position, but this makes the code
somewhat difficult to read at times. You’d also like to be less dependent on position in
the structure, by accessing the elements by name.

solution: collections.namedtuple() provides these benefits, while adding minimal overhead
over using a normal tuple object. collections.namedtuple() is actually a factory
method that returns a subclass of the standard Python tuple type. You feed it a type
name, and the fields it should have, and it returns a class that you can instantiate, passing
in values for the fields you’ve defined, and so on.
"""

from collections import namedtuple

Subscriber = namedtuple('Subscriber', ['addr', 'joined'])
sub = Subscriber('mrinal@advarisk.com', '2017-01-01')
print(f'Subscriber object: {sub}\naddr: {sub.addr}\njoined: {sub.joined}')

# Although an instance of a namedtuple looks like a normal class instance, it is inter‐
# changeable with a tuple and supports all of the usual tuple operations such as indexing
# and unpacking.
addr, joined = sub
print(addr, joined)

# A major use case for named tuples is decoupling your code from the position of the
# elements it manipulates. So, if you get back a large list of tuples from a database call,
# then manipulate them by accessing the positional elements, your code could break if,
# say, you added a new column to your table. Not so if you first cast the returned tuples
# to namedtuples.

# IMPORTANT: One possible use of a namedtuple is as a replacement for a dictionary, which requires
# more space to store. Thus, if you are building large data structures involving dictionaries,
# use of a namedtuple will be more efficient. However, be aware that unlike a dictionary,
# a namedtuple is immutable.

Stock = namedtuple('Stock', ['name', 'shares', 'price'])
stock = Stock(name='ACME', shares=100, price=123.45)
# stock.shares = 75 # cannot do that coz it is immutable

# If you need to change any of the attributes, it can be done using the _replace() method
# of a namedtuple instance, which makes an entirely new namedtuple with specified val‐
# ues replaced.
stock = stock._replace(shares=75)
print(f'Stock: {stock}')
print('- ' * 50)
# =====================================================================================

"""
1.19. Transforming and Reducing data at the same time

Problem: you need to execute a reduction function (eg: sum(), min(), max()) but first
         need to transform or filter the data.

Solution: A very elegant way to combine a data reduction and transformation is to use a
          generator-expression argument. eg: if you want to calculate the sum of squares
"""

nums = [1, 2, 3, 4, 5]
s = sum(x * x for x in nums)
print(f"Sum: {s}")

# determine if any .py file exists in a directory
import os
files = os.listdir('./')
if any(name.endswith('.py') for name in files):
    print("There be python!")
else:
    print("There is no python!")

# output a tuple as CSV
s = ('ACME', 50, 123.45)
print(','.join(str(x) for x in s))

# Using a generator argument is often a more efficient and elegant approach than first
# creating a temporary list
nums = [1, 2, 3, 4, 5]
s = sum(x * x for x in nums)
print(f"sum (more elegant): {s}")
