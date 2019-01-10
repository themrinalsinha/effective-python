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
