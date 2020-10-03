"""
8.1. changing the string representation of instances

Problem: You want to change the output produced by printing or viewing instance
         to something more sensible.

Solution: To change the string representation of an instance, define the
          __str__() and __repr__() methods.
"""

class Pair:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return 'Pair({0.x!r}, {0.y!r})'.format(self)

    def __str__(self) -> str:
        return '({0.x!s}, {0.y!s})'.format(self)

# The __repr__() method returns the code representation of an instance, and is usually
# the text you would type to re-create the instance. The built-in repr() function returns
# this text, as does the interactive interpreter when inspecting values. The __str__()
# method converts the instance to a string, and is the output produced by the str() and
# print() functions.

p = Pair(3, 5)
p # __repr__() output
print(p) # __str__()  output

# The implementation of this recipe also shows how different string representations
# may be used during formatting. Specifically, the special !r formatting code indicates
# that the output of __repr__() should be used insted of __str__(), the default.

p = Pair(3, 4)
print("p is {!r}".format(p))
print("p is {}".format(p))
print("- " * 50)
# =====================================================================================

"""
8.2. customizing string formatting

Problem: you want an object to support customized formatting through the format()
         function and string method.

Solution: To customize string formatting, define the __format__() method on a class.
"""

_formats = {
    'ymd' : '{d.year}-{d.month}-{d.day}',
    'mdy' : '{d.month}/{d.day}/{d.year}',
    'dmy' : '{d.day}/{d.month}/{d.year}',
}

class Date:
    def __init__(self, year, month, day) -> None:
        self.year  = year
        self.month = month
        self.day   = day

    def __format__(self, format_spec: str) -> str:
        if format_spec == '':
            format_spec = 'ymd'
        fmt = _formats[format_spec]
        return fmt.format(d=self)

# instances of the date class now support formatting operations such as the following
d = Date(2012, 12, 21)
print(format(d))
print(format(d, 'mdy'))
print(f'The date is {d:ymd}')
print(f'The date is {d:mdy}')

# The __format__() method provides a hook into Python's string formatting
# functionality. It's important to emphasize that the interpretation of format
# codes is entirely up to the class itself.

from datetime import date
d = date(2012, 12, 12)
print(format(d))
print(format(d, '%A, %B %d, %Y'))
print('The end is {:%d %b %Y}. Goodbye'.format(d))
