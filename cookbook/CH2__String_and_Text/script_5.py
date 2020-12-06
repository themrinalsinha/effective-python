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
print('- ' * 50)
# ===================================================================================

"""
2.17. Handling HTML and XML entities in Text

Problem: You want to replace HTML or XML entities such as &entity; or &#code; with
         their corresponding text. Alternatively, you need to produce text, but escape
         certain characters (<, >, or &)
"""
import html
s = 'Elements are written as "<tag>text</tag>".'
print(s)
print(html.escape(s))

# disable escaping of quotes
print(html.escape(s, quote=False))

# if you're trying to emit text as ASCII and want to embed character code entities for
# non-ASCII characters, you can use the errors='xmlcharrefreplace' argument to various
# I/O-related functions to do it.
s = 'Spicy Jalapeño'
print(s.encode('ascii', errors='xmlcharrefreplace'))

# To replace entities in text, a different approach is needed. If you're actually processing HTML or XML, try using proper HTML or XML parser first.
from html.parser import HTMLParser
s = 'Spicy &quot;Jalape&#241;o&quot.'
p = HTMLParser()
print(p.unescape(s))

from xml.sax.saxutils import unescape
t = 'The prompt is &gt;&gt;&gt;'
print(unescape(t))
