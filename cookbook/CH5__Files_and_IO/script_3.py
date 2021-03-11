"""
5.8. Iterating over fixed-sized records

Problem: Instead of iterating over a file by lines, you want to iterate over a
         collection of fixed-sized records or chunks.
"""
from functools import partial

RECORD_SIZE = 32

with open("somefile.data", "rb") as f:
    records = iter(partial(f.read, RECORD_SIZE), b'')
    for r in records:
        print(r)

# The records object in this example is an iterable that will produce fixed-sized
# chunks until end of the file is reached. However, be aware that the last item may
# have fewer bytes than expected if the file size is not an exact multiple of the
# record size.

# In the solution, the functools.partial is used to create a callable that reads a fixed
# number of bytes from a file each time it’s called. The sentinel of b'' is what gets returned
# when a file is read but the end of file has been reached.
print('- ' * 50)
# ------------------------------------------------------------------------------------

"""
5.9. Reading Binary Data into a Mutable Buffer

Problem: You want to read binary data directly into a mutable buffer without any intermediate
         copying. Perhaps you want to mutate the data in-place and write it back out to a file.

Solution: To read data into a mutable array, use the readinto() method of files
"""
import os

def read_into_buffer(filename):
    buf = bytearray(os.path.getsize(filename))
    with open(filename, 'rb') as f:
        f.readinto(buf)
    return buf

# here is an example of illustrating the usage
with open("sample.bin", 'wb') as f:
    f.write(b'Hello world')

buf = read_into_buffer('sample.bin')
print(buf)
print(buf[0:5])

with open('somefile.data', 'wb') as f:
    f.write(buf)
