"""
6.11 Reading and Writing Binary Arrays of Structures

Problem: You want to read or write data encoded as a binary array of uniform structures
         into Python tuples.

Solution: To work with binary data, use the struct module. Here is an example of code that writes
          a list of python tuples out of a binary file.
"""
# Encoding each tuple as a structure using struct:

from struct import Struct


def write_records(records, format, f):
    """
    write a sequence of tuples to a binary file of structures
    """
    record_struct = Struct(format)
    for r in records:
        f.write(record_struct.pack(*r))

records = [
    (1, 2.3, 4.5),
    (5, 7.8, 9.0),
    (8, 1.3, 5.6)
]

with open("data.b", "wb") as f:
    write_records(records, '<idd', f)

# There are several approaches for reading this file back into a list of tuples. First
# if you're going to read this file incrementally in chunks, you can write code such as:

from struct import Struct

def read_records(format, f):
    record_struct = Struct(format)
    chunks = iter(lambda: f.read(record_struct.size), b'')
    return (record_struct.unpack(chunk) for chunk in chunks)

with open("data.b", "rb") as f:
    for rec in read_records('<idd', f):
        print(rec)

# If you want to read the file entirely into a byte string with a single read and convert
# it piece by piece.
from struct import Struct

def unpack_records(format, data):
    record_struct = Struct(format)
    return (record_struct.unpack_from(data, offset) for offset in range(0, len(data), record_struct.size))

with open("data.b", "rb") as f:
    data = f.read()

for rec in unpack_records('<idd', data):
    print(rec)

# For programs that must encode and decode binary data, it is common to use the struct
# module. To declare a new structure, simply create an instance of Struct such as:

# # Little endian 32-bit integer, two double precision floats
# record_struct = Struct('<idd')
print('- ' * 50)
# =======================================================================================

"""
6.12. Reading Nested and Variable-Sized Binary Structures

Problem: You need to read complicated binary-encoded data that contains a collection of
         nested and/or variable-size records. Such data might include images, video,
         shapefiles, and so on...
"""
