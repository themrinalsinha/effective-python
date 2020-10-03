"""
7.1. Writing functions that accepts any number of arguments

Problem: you want to write a function that accepts any number of arguments or
         to accept any number of keyword arguments
Solution: use * for argument and ** for keyword arguments
"""

# Arguments
def avg(first, *rest):
    return (first + sum(rest)) / (1 + len(rest))

print(f"Avg: (1, 2) --> {avg(1, 2)}")
print(f"Avg: (1, 2, 3, 4, 5) --> {avg(1, 2, 3, 4, 5)}")

# rest is a tuple of all the extra positional arguments passed

# Keyword arguments
import html

def make_element(name, value, **attrs):
    keyvals  = [f"{key}={value}" for key, value in attrs.items()]
    attr_str = ' '.join(keyvals)
    element  = f'<{name} {attr_str}><{html.escape(value)}</{name}>'
    return element

print(make_element('item', 'Albatross', size='large', quantity=6))
print(make_element('p', '<span>'))
# Here, attrs is a dictionary that holds the passed keyword arguments (if any)

def anyargs(*args, **kwargs):
    print(args)   # a tuple
    print(kwargs) # a dict
print('- ' * 50)
# =============================================================================

"""
7.2. Writing functions that only accepts keyword arguments

Problem: You want a function to only accept certain arguments by keyword
"""

def recv(maxsize, *, block):
    pass

# recv(1024, True)      # TypeError
recv(1024, block=True)  # OK

# Keyword-only arguments are often a good way to enforce greater code clarity when
# specifying optional function arguments.
# msg = recv(1024, False)
print('- ' * 50)
# ============================================================================

"""
7.3. Attaching Informational Metadata to Function Arguments

Problem: You've written a function, but would like to attach some additional
         information to the arguments so that others know more about how the function
         is supposed to be used.

"""

def add(x: int, y: int) -> int:
    return x + y

# The Python interpreter does not attach any semantic meaning to the attached annota‐
# tions. They are not type checks, nor do they make Python behave any differently than
# it did before. However, they might give useful hints to others reading the source code
# about what you had in mind. Third-party tools and frameworks might also attach se‐
# mantic meaning to the annotations. They also appear in documentation:
"""
    >>> help(add)
    Help on function add in module __main__:
    add(x: int, y: int) -> int
    >>>
"""
print('- ' * 50)
# ===============================================================================

"""
7.4. Returning Multiple Values from a Function

Problem: you want to return multiple values from a function
"""
def myfunc():
    return 1, 2, 3

a, b, c = myfunc()
# Although it looks like myfun() returns multiple values, a tuple is actually being created.
# It looks a bit peculiar, but it’s actually the comma that forms a tuple, not the parentheses.
print('- ' * 50)
# ===============================================================================
