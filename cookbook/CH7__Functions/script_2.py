"""
7.5. Defining functions with default arguments

Problem: You want to define a function or method where one or more of the arguments
         are optional and have a default value
"""

def spam(a, b=42):
    print(a, b)

spam(11)
spam(11, 22)

# If, instead of providing a default value, you want to write code that merely tests whether
# an optional argument was given an interesting value or not, use this idiom:
_no_value = object()

def spam(a, b=_no_value):
    if b is _no_value:
        print("No value supplied")
    print(a, b)

spam(1)
spam(1, 2)
print('- ' * 50)
# ===================================================================================

"""
7.6. Defining anonymous or inline functions

Problem: You need to supply a short callback function for use with an operation such as sort() ,
but you don’t want to write a separate one-line function using the def statement. Instead,
you’d like a shortcut that allows you to specify the function “in line.”

Solution: use lambda function
"""
add = lambda x, y: x + y
print(add(2, 4))
print(add('Hello', ' world'))

names = ['mrinal', 'manan', 'kunal', 'aaditya', 'aviral', 'sanu', 'manu']
print(names)
sorted(names, key=lambda n: n.lower())
print('- ' * 50)
# ===================================================================================

"""
7.7. Capturing variables in anonymous functions

Problem: you've defined an anonymous function using lambda, but you need to capture
the values fo certain vairable at the time of definition.
"""
x = 10
a = lambda y: x + y
x = 20
b = lambda y: x + y

# Now ask yourself a question. What are the values of a(10) and b(10) ? If you think the
# results might be 20 and 30, you would be wrong:
print(a(10))
print(b(10))

# If you want an anonymous function to capture a value at the point of definition and
# keep it, include the value as a default value, like this:
x = 10
a = lambda y, x=x: x + y
x = 20
b = lambda y, x=x: x + y
print(a(10))
print(b(10))

funcs = [lambda x: x+n for n in range(5)]
for f in funcs:
    print(f(0))

funcs = [lambda x, n=n: x+n for n in range(5)]
for f in funcs:
    print(f(0))
print('- ' * 50)
# ===================================================================================

"""
7.8. Making an N-Argument callable work as a callable with fewer arguments

Problem: You have a callback that you would like to use with some other Python code,
         possibly as a callback function or handler, but it takes too many arguments
         and causes an exception when called.

Solution: If you need to reduce the number of arguments to a function, you should use
          functools.partial(). The partial() function allows you to assign fixed values
          to one or more arguments, thus reducing the numberr of arguments that need to
          be supplied to subsequent calls.
"""

def spam(a, b, c, d):
    print(a, b, c, d)

# Now, consider that use of partial() to fix certain argument values:
from functools import partial

s1 = partial(spam, 1) # a = 1
s1(2, 3, 4)
s1(4, 5, 6)

s2 = partial(spam, d=42) # d = 42
s2(1, 2, 3)
s2(4, 5, 6)

s3 = partial(spam, 1, 2, d=69) # a = 1, b = 2, d = 42
s3(3)
s3(4)
# Observe that partial() fixes the values for certain arguments and return a new callable
# as a result. The new callable accepts the still unassigned arguments, combines them
# with the arguments given to partial(), and passes everything to the original function.

points = [ (1, 2), (3, 4), (5, 6), (7, 8) ]

import math
def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x2 - x1, y2 - y1)

# Now suppose you want to sort all the points according to their distance from some other point.
# The sort() method of lists accepts a key argument that can be used to customize sorting,
# but it only works with functions that take a single argument (thus, distance()) is not suitable.

pt = (4, 3)
points.sort(key=partial(distance, pt))
print(points)
print()

# As an extension of this idea, partial() can often be used to tweak the argument signatures of
# callback functions used in other libraries. Eg: here's a bit of code that uses multiprocessing
# to asynchronously compute a result which is handed to a callback function that accepts both the
# result and on optional logging argument.

def output_result(result, log=None):
    if log is not None:
        log.debug(f"Got: {result}")

def add(x, y):
    return x + y

import logging
from functools       import partial
from multiprocessing import Pool

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("test")

p = Pool()
p.apply_async(add, (3, 4), callback=partial(output_result, log=log))
p.close()
p.join()
