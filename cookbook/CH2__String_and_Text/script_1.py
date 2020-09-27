"""
2.1 - splitting strings on any of multiple delimiters

Problem: you need to split a string into fields, but the delimiters (and spacing
around them) aren't consists throughout the string.
"""

from re import split as re_split

line = 'asdf fjdk; afed, fjek,asdf,   foo'
_line = re_split(r'[;,\s]\s*', line)
print(f"After re.split: {_line}")

# The re.split() function is useful because you can specify multiple patterns for the
# separator. For example, as shown in the solution, the separator is either a comma (,),
# semicolon (;), or whitespace followed by any amount of extra whitespace. Whenever
# that pattern is found, the entire match becomes the delimiter between whatever fields
# lie on either side of the match. The result is a list of fields, just as with str.split() .

fields = re_split(r'(;|,|\s)\s*', line)
print(f"Fields: {fields}")

# If you don’t want the separator characters in the result, but still need to use parentheses
# to group parts of the regular expression pattern, make sure you use a noncapture group,
# specified as (?:...) .

res = re_split(r'(?:,|;|\s)\s*', line)
print(f"Result: {res}")
print('- ' * 50)
# =====================================================================================

"""
2.2. Matching text at the start or end of a string

Problem: you need to check the start or end of a string for specific text patterns,
         such as filename, extensions, URL schemas and so on.
"""

filename = 'span.txt'
print(f"startswith (sp): { filename.startswith('sp') }")
print(f"endswith (txt): { filename.endswith('txt') }")

# if you need to check against multiple choices, simply provide a tuple of possibilities
# to startswith() or endswith()
files = ['abc.txt', 'xyz.cpp', 'pqr.txt', 'cpp.py', 'temp.java']
for f in files:
    if f.startswith(('abc', 'cpp')):
        print(f"startswith: {f}")
    if f.endswith(('.cpp', '.py')):
        print(f"endswith: {f}")

print('- ' * 50)
# =====================================================================================

"""
2.3. Matching strings using shell wildcard patterns

Problem: you want to match text using the same wildcard patterns as are commonly used when
         working in Unix shells (eg: *.py, Dat[0-9]*.csv, etc)

Solution: the fnmatch module provides two functions - fnmatch() and fnmatchcase() - that can
          be used to perform such matching. The usage in simple
"""

from fnmatch import fnmatch, fnmatchcase
print(f"fnmatch -> (foo.txt, *.txt) ==> {fnmatch('foo.txt', '*.txt')}")
print(f"fnmatch -> (foo.txt, ?oo.txt) ==> {fnmatch('foo.txt', '?oo.txt')}")
print(f"fnmatch -> (Dat45.csv, 'Dat[0-9]*) ==> {fnmatch('Dat45.csv', 'Dat[0-9]*')}")

names = ['Dat1.csv', 'Dat2.csv', 'config.ini', 'foo.py']
print([name for name in names if fnmatch(name, 'Dat*.csv')])

print(f"match case: {fnmatchcase('foo.txt', '*.TXT')}")
