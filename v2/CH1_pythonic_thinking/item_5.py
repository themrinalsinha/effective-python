"""
Item 5: Write helper functions instead of complex expressions

Python's pithy syntax makes makes it easy to write single-line expressions that
implement a lot of logic. Ex: say that I want to decode the query string from a
URL. Here, each query string parameter represents an integer value
"""

from urllib.parse import parse_qs

my_values = parse_qs('red=5&blue=0&green=', keep_blank_values=True)
print(repr(my_values))

red = my_values.get('red', [''])[0] or 0
green = my_values.get('green', [''])[0] or 0
opacity = my_values.get('opacity', [''])[0] or 0
print(red, green, opacity)
