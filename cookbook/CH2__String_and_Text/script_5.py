"""
2.16. Reformatting text to a fixed number of columns

Problem: You have long strings that you want to reformat so that they fill a user
         specified number of columns
"""

import textwrap

s = "Look into my eyes, look into my eyes, the eyes, the eyes, \
the eyes, not around the eyes, don't look around the eyes, \
look into my eyes, you're under."

print(textwrap.fill(s, 70))
print()
print(textwrap.fill(s, 40))
print()
print(textwrap.fill(s, 40, initial_indent="    "))
print()
print(textwrap.fill(s, 40, subsequent_indent="    "))

# The textwrap module is a straightforward way to clean up text for printing - especially if you want the output to fit nicely on the terminal. On the subject of the terminal size, you can obtain using
import os
cols = os.get_terminal_size().columns
print(cols)
