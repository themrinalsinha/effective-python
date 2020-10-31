"""
2.7. Specifying a regular expression for the shortest match

Problem: you're trying to match a text pattern using regular expression, but it is
         identifying the longest possible matches of a pattern. Instead, you would
         like to change it to find the shortest possible match.
"""

import re

str_pattern = re.compile(r'\"(.*)\"')
text_1 = 'Computer says "no."'
print(str_pattern.findall(text_1))

text_2 = 'Computer says "no." Phone says "yes."'
print(str_pattern.findall(text_2))

# In this example, the pattern r'\"(.*)\"' is attempting to match text enclosed inside
# quotes. However, the * operator in a regular expression is greedy, so matching is based
# on finding the longest possible match.

# This makes matching nongreedy, and produces the shortest match instead.
str_pattern = re.compile(r'\"(.*?)\"')
print(str_pattern.findall(text_2))
print()
# ===================================================================================

"""
2.9. Normalizing Unicode Text to a Standard Representation

Problem: You're working with Unicode strings, but need to make sure that all of the
         strings have the same underlying representation.

Solution: In Unicode, certain characters can be represented by more than one valid
          sequence of code points.
"""
s1 = 'Spicy Jalape\u00f1o'
s2 = 'Spicy Jalapen\u0303o'
print(f"S1: {s1}\nS2: {s2}")
print(f"S1 == S2: {s1 == s2}")
# Here the text “Spicy Jalapeño” has been presented in two forms. The first uses the fully
# composed “ñ” character (U+00F1). The second uses the Latin letter “n” followed by a
# “~” combining character (U+0303).

# Having multiple representations is a problem for programs that compare strings. In
# order to fix this, you should first normalize the text into a standard representation using
# the unicodedata module
import unicodedata

t1 = unicodedata.normalize('NFC', s1)
t2 = unicodedata.normalize('NFC', s2)
print(f"\nNormalized data (using NFC)\nS1: {t1}\nS2: {t2}")
print(f"S1 == S2: {t1 == t2}")

t1 = unicodedata.normalize('NFD', s1)
t2 = unicodedata.normalize('NFD', s2)
print(f"\nNormalized data (using NFD)\nS1: {t1}\nS2: {t2}")
print(f"S1 == S2: {t1 == t2}")
print()

# ===================================================================================

"""
2.11. Stripping Unwanted Characters from Strings

Problem: You want to strip unwanted characters, such as whitespace, from the beginning
         end, or middle of a text string.

         strip(), lstrip(), rstrip()
"""

# whitespace stripping
s = "   hello world  \n"
print(f"strip(): {s.strip()}")
print(f"lstrip(): {s.lstrip()}")
print(f"rstrip(): {s.rstrip()}")

# character stripping
t = '-----hello====='
print(f"lstrip('-') -> {t.lstrip('-')}")
print(f"strip('-=') -> {t.strip('-=')}")
