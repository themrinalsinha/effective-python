"""
5.1. Reading and Writing Text Data

Problem: You need to read or write text data, possibly in different text encoding
         such as ASCII, UTF-8, or UTF-16
"""

# Use the open() function with mode rt to read a text file

# Read the entire file as a single string
with open('somefile.txt', 'rt') as f:
    data = f.read()

# Iterate over the lines of file
with open("somefile.txt", 'rt') as f:
    for line in f:
        # process line
        pass


# similarly use open() with wt to write a file, clearing and overwriting the
# previous contents.

# write chunks of text data
with open("somefile.txt", 'wt') as f:
    text1 = 'hello world.'
    f.write(text1)

# redirecting print statements
with open('somefile.txt', 'wt') as f:
    line_1 = 'hello world...'
    line_2 = 'how are you ??'

    print(line_1, file=f)
    print(line_2, file=f)

# to append use `at` modifier

# By default, files are read/written using the system default text encoding, as can be found
# in sys.getdefaultencoding() . On most machines, this is set to utf-8 . If you know
# that the text you are reading or writing is in a different encoding, supply the optional
# encoding parameter to open() .

with open("somefile.txt", 'rt', encoding='latin-1') as f:
    pass

# Another minor complication concerns the recognition of newlines, which are different
# on Unix and Windows (i.e., \n versus \r\n). By default, Python operates in what's known
# as "universal newline" mode.
# By default the newline character \n is converted to the system default newline character
# on output. If you don't want this translation, supply the newline="" argument to open(), like this

with open("somefile.txt", 'rt', newline='') as f:
    pass

# >>> # Replace bad chars with Unicode U+fffd replacement char
# >>> f = open('sample.txt', 'rt', encoding='ascii', errors='replace')
# >>> f.read()
# 'Spicy Jalape?o!'
# >>> # Ignore bad chars entirely
# >>> g = open('sample.txt', 'rt', encoding='ascii', errors='ignore')
# >>> g.read()
# 'Spicy Jalapeo!'
# >>>
