"""
5.2. Printing to file
"""
with open("somefile.txt", "w") as f:
    print("Hello world !", file=f)
# ----------------------------------------------------------------------------------


"""
5.3. Printing with a different separator or line ending
"""
print("ACME", 50, 90.5)
print("ACME", 50, 90.5, sep=',')
print("ACME", 50, 90.5, sep=',', end="!!\n")
print()
# ----------------------------------------------------------------------------------


"""
5.6 Performing I/O Operations on a string

Problem: You want to feed a text or binary string to code that's been written to operate
         on a file like objects instead.

Solution: Use the io.StringIO() or io.BytesIO() classes to create file-like objects that
          operate on string data.
"""
from io import StringIO, BytesIO

s = StringIO()
s.write("Hello World\n")
print("this is a test\n", file=s)

# getting all the data written so far
print(s.getvalue())

# wrap a file interface around an existing string
s = StringIO("hello\nworld\nhow are you\n")
print("TILL 8   : ", s.read(8))
print("REMAINING: ", s.read())

s = BytesIO()
s.write(b'binary data')
print(s.getvalue())
print('- ' * 50)
# ------------------------------------------------------------------------------------

