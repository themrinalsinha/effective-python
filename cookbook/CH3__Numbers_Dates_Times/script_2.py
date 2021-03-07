"""
3.5. Packing and Unpacking large integers from bytes

Problem: You have a byte string you need to unpack it into an integer value, Alternatively,
         You need to convert large integer back into a byte string.

Solution: Suppose your program needs to work with a 16-element byte string that holds a
          128 bit integer value.
"""

data = b'\x00\x124V\x00x\x90\xab\x00\xcd\xef\x01\x00#\x004'
print(len(data))
print(int.from_bytes(data, 'little'))
print(int.from_bytes(data, 'big'))

x = 94522842520747284487117727783387188
print(x.to_bytes(16, 'big'))
print(x.to_bytes(16, 'little'))

# Converting large integer values to and from byte strings is not a common operation.
# However, it sometimes arises in certain application domains, such as cryptography or
# networking. For instance, IPv6 network addresses are represented as 128-bit integers.
# If you are writing code that needs to pull such values out of a data record, you might
# face this problem.
print()
# =====================================================================================
