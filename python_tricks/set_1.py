# If you miss a comma between two list items,
# list is going to join them, this is known as
# "string literal concatenation"
data_1 = ['Alice', 'Bob', 'Dilbert', 'Jane']
data_2 = [
    'Alice',
    'Bob'
    'Delbert',
    'Jane'
]
print(data_1)
print(data_2)

# ================================================
# Context Managers and the with statement.
# The with statement in python helps you write cleaner and more readable python code.
# eg:
with open('hello.txt', 'w') as f:
    f.write('Hello, world!')

# You can provide the same functionality in your own
# classes and functions by implementing so-called context managers.
class ManagedFile(object):
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.file = open(self.name, 'w')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

with ManagedFile('hello.txt') as f:
    f.write('Hello, world\n')
    f.write('How are you...?\n')

# Writing a class-based context manager isn't the only way to support the with
# statement in python. The contextlib utility module in the standard library provodes
# a few more abstractions built on top of the basic context manager protocol.

# Eg: You can use the contextlib.contextmanager decorator to define a generator-based
# format functions for a  resource that will then automatically support with the with statement.

from contextlib import contextmanager

@contextmanager
def manage_file(name):
    try:
        f = open(name, 'w')
        yield f
    finally:
        f.close()

with manage_file('hello.txt') as f:
    f.write('hello world...!\n')
    f.write('Bye for now..!! L:()')

# ================================================
print('-------------------------------------------')
class Indenter:
    def __init__(self):
        self.level = 0

    def __enter__(self):
        self.level += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.level -= 1

    def print(self, text):
        print('    ' * self.level + text)

with Indenter() as indent:
    indent.print('Hi...!')
    with indent:
        indent.print('Hello!')
        with indent:
            indent.print('Bonjour')
    indent.print('Hey')
# ================================================
# Keynote:
# _> The with statement simplifies exception handling by encapsulating standard uses of try/finally satemt is so-called context manager.
