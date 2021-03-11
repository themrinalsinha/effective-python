"""
5.20. Communicating with Serial Ports

Problem: You want to read and write data over a serial port, typically to interact with
         some kind of hardware device (eg: robot or sensor)

Solution: Altough you can probably do this directly using Python's built-in I/O primitives,
          you best bet for serial communication is to use the pySerial package.
"""
import serial
ser = serial.Serial('/dev/tty.usbmodem641',
            baudrate=9600,
            bytesize=8,
            parity='N',
            stopbits=1
        )
