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
        pass

# The records object in this example is an iterable that will produce fixed-sized
# chunks until end of the file is reached. However, be aware that the last item may
# have fewer bytes than expected if the file size is not an exact multiple of the
# record size.

# In the solution, the functools.partial is used to create a callable that reads a fixed
# number of bytes from a file each time it’s called. The sentinel of b'' is what gets returned
# when a file is read but the end of file has been reached.
print('- ' * 50)
# ------------------------------------------------------------------------------------
