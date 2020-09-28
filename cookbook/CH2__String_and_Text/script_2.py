"""
2.4. matching and searching for text patterns

problem: you want to match or search text for a specific pattern.
"""

import re

text = 'yeah, but no, but yeah, but no, but yeah'

# exact match
print(f"Exact match: {text == 'yeah'}")

# starts or ends with
print(f"Starts with: {text.startswith('yeah')}\nEnds with: {text.endswith('no')}")

# searching for the location of first occurrence
print(f"First occurrence (give index): {text.find('no')}")


# for more complicated matching, use regular expression and the re-module
text1 = '11/27/2012'
text2 = 'Nov 27, 2012'

if re.match(r'\d+/\d+/\d+', text1):
    print(f"RE MATCH ('\d+/\d+/\d+') to {text1} : Yes")
else:
    print("No")


if re.match(r'\d+/\d+/\d+', text2):
    print("Yes")
else:
    print("No")


# if you're going to perform a lot of matches using the same pattern, it usually pays
# to precompile the regular expression pattern into a pattern object first.
datepat = re.compile(r"\d+/\d+/\d+")
if datepat.match(text1):
    print('Match')
else:
    print("Not Match")

if datepat.match(text2):
    print("Match")
else:
    print("Not Match")


# match() always tries to find the match at the start of a string. If you want to
# search text for all occurrences of a pattern, use the findall() method instead.
text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
print(f"Finding all matching pattern: {datepat.findall(text)}")


# IMPORTANT:
# when defining regular expression, it is common to introduce capture groups by enclosing
# parts of the pattern in parentheses. Eg:
datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
m = datepat.match("11/27/2012")
print(f"Match object: {m}")

# now extract the content of each group
print(f"Group(0): {m.group(0)}")
print(f"Group(1): {m.group(1)}")
print(f"Group(2): {m.group(2)}")
print(f"Group(3): {m.group(3)}")
print('- ' * 50)
# =======================================================================================

"""
2.5. Searching and Replacing Text

Problem: You want to search for and replace a text patterns in a string.
"""

text = 'yeah, but no, but yeah, but no, but yeah'
print(f"Replacing word: {text.replace('yeah', 'yep')}")

# for more complicated patterns, use the sub() functions/method in the re module.
text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
resu = re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text)
print(f"Using sub: {resu}")

# The first argument to sub() is the pattern to match and the second argument is the
# replacement pattern. Backslashed digits such as \3 refer to capture group numbers in
# the pattern

# If you’re going to perform repeated substitutions of the same pattern, consider compil‐
# ing it first for better performance.
datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
print(datepat.sub(r'\3-\1-\2', text))
print('- ' * 50)
# ====================================================================================

"""
2.6. Searching and Replacing case-Insensitive text
"""

text = 'UPPER PYTHON, lower python, Mixed Python'
resu = re.findall('python', text, flags=re.IGNORECASE)
print(f"case insensitive match: {resu}")

resu = re.sub('python', 'snake', text, flags=re.IGNORECASE)
print(f"Replacing value: {resu}")

