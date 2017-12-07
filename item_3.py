# Item 3 : Know the difference between bytes, str, and unicode

# NOTES:
# Python 3 - two types that represent sequence of characters: bytes and str (instances of bytes contain raw 8-bit values, instance of str contain Unicode characters.)
# Python 2 - there is str and unicode (str = raw 8-byte, unicode = unicode character)

# The split between character types leads to two common situations in python code.
#   -> you want to operate on raw 8-bit values that are UTF-8 encoded characters (or some other type)
#   -> you want to operate on Unicode characters that have no specific encoding.
# if you want to read or write binary data to/from a file, always open the file using a binary mode (like 'rb' or 'wb')

# One method: take str or bytes and always return str
def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value # Instance of str

# One method: take str or bytes and always return bytes.
def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return value # Instance of bytes

print(to_bytes('Hello there...'))
print(to_str(b'Hello there...'))