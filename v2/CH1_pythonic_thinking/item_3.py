"""
Item 3: Know the difference between bytes and str
"""

# Instances of bytes contain raw, unsigned 8-bit
# values (often displayed in the ASCII encoding)
a = b'h\x65llo'
print(list(a))
print(a)

# Instances of str contain Unicode code points that
# represent textual characters from human languages
a = 'a\u0300 propos'
print(list(a))
print(a)

# str instances do not have an associated binary encoding, and bytes instances
# do not have an associated text encoding. To convert Unicode data to binary
# data, you must call the encode method of str & to convert binary data to unicode
# data, you must call the decode method of bytes.

def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value

print(repr(to_str(b'foo')))
print(repr(to_str('bar')))

# Things to remember
# - bytes contains sequences of 8-bit values, and str contains sequences of
#   unicode points
# - Use helper function to ensure that the inputs you operate on are the type
#   of character sequence that you expect (8-bit values, UTF-8-encoded strings)
# - bytes and str instances can't be used together with operate (like >, ==, + and %)
