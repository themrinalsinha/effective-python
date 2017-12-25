# Item 14 : Prefer Exceptions to Return None

# Say you want a helper function that divides one number by another. In the case of dividing by zero, 
# returning None seems natural because the result is undefined.

def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

result = divide(5, 0)
if result is None:
    print('Invalid inputs')

# What happen when the numerator is zero? That will cause the return value to also be zero (if the denominator is non-zero).
# This can cause problems when you eveluate the result in a condition like an if statement

result = divide(0, 5)
if result is None:
    print('Invalid inputs') # This is wrong.

# This is a common mistake in Python code when None has special meaning. This is why returning None from a function is error prone. There are two ways to reduce chance of such error.

# The first way is to split the return value into a two-tuple. The first part of the tuple indicates that the operation was success or failure. The second part is the actual result that was computed.

def divide(a, b):
    try:
        return True, a/b
    except ZeroDivisionError:
        return False, None

success, result = divide(0, 5)
if not success:
    print('Invalid inputs')

success, result = divide(5, 0)
if not success:
    print('Invalid inputs')

# The second, better way to reduce these errors is to never return None at all. Instead, raise an exception up to the caller and make them deal with it.

# Here I turn a ZeroDivisionError into a ValueError to indicate to the caller that the input values are bad:

def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('Invalid inputs') from e

result = divide(5, 2)
print(result)

# Note:
# Function that return None to indicate special meaning are error prone because None and other values (eg: zero, the empty string) all evaluate to False in conditional expression.
# Raise exception to indicate special situations instead of returning None. Expect the calling code to handle exception properly when they're documented.


