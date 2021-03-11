"""
5.20. Communicating with Serial Ports

Problem: You want to read and write data over a serial port, typically to interact with
         some kind of hardware device (eg: robot or sensor)

Solution: Altough you can probably do this directly using Python's built-in I/O primitives,
          you best bet for serial communication is to use the pySerial package.
"""
# import serial
# ser = serial.Serial('/dev/tty.usbmodem641',
#             baudrate=9600,
#             bytesize=8,
#             parity='N',
#             stopbits=1
#         )
print('- '* 50)
# --------------------------------------------------------------------------------------

"""
5.21. Serializing Python Objects

Problem: You need to serialize a python object into a byte stream so that you can do things
         such as save it to a file, store it in a database, or transmit it over a network
         connection.

Solution: The most common approach for serializing data is to pickle module. To dump an object
          to a file, you do this.
"""

class A:
    def a(self):
        print("HELLO (AAA)")

import pickle

data = A()
f = open("somefile", "wb")
pickle.dump(data, f)

# to dump an object to a string, use pickle.dumps()
s = pickle.dumps(data)
print(s)

#  to re-create an object from a byte stream, use pickle.load() or pickle.loads() function.
f = open("somefile", 'rb')
data = pickle.load(f)
print(data)
print(data.a())
