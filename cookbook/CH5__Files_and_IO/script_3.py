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
print('- ' * 50)
# ----------------------------------------------------------------------------------------


"""
5.10. Memory Mapping Binary Files

Problem: You want to memory map a binary file into a mutable byte array, possibly for
         random access to its contents or to make in-place modifications

Solution: Use the mmap module to memory map files. Here is a utility function that shows
          how to open a file and memory map it in a portable manner.
"""
import os
import mmap

def memory_map(filename, access=mmap.ACCESS_WRITE):
    size = os.path.getsize(filename)
    fd = os.open(filename, os.O_RDWR)
    return mmap.mmap(fd, size, access=access)

# TO use this function, you would need to have a file already created and filled with data.
# Here is an example of how you could initially create a file and expand it to a desired size.

size = 1000000
with open('data', 'wb') as f:
    f.seek(size-1)
    f.write(b'\x00')

# example of memory mapping the content using the memory_map() function
m = memory_map('data')
print(len(m))
print(m[0:10])
print(m[0])

# reassign a slice
m[0:11] = b'Hello World'
m.close()

# verify that changes were made
with open("data", 'rb') as f:
    print(f.read(11))

# The mmap object returned by mmap() can also be used as a context manager, in which
# case the underlying file is closed automatically.
with memory_map('data') as m:
    print(len(m))
    print(m[0:10])
