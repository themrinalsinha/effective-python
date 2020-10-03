"""
8.3. making objects support the context-management protocol

Problem: you want to make your object support the context-manager protocol (the with statement).

solution: In order to make an objects compatible with the with statement,
          you need to implement __enter__() and __exit__() methods. consider
          the following class, which provides a network connection.
"""

from socket import socket, AF_INET, SOCK_STREAM

class LazyConnection:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM) -> None:
        self.address = address
        self.family  = AF_INET
        self.type    = SOCK_STREAM
        self.sock    = None

    def __enter__(self):
        if self.sock is not None:
            raise RuntimeError("Already connected")
        self.sock = socket(self.family, self.type)
        self.sock.connect(self.address)
        return self.sock

    def __exit__(self, exc_ty, exc_val, tb):
        self.sock.close()
        self.sock = None

from functools import partial

conn = LazyConnection(('www.python.org', 80))

# connection closed
with conn as s:
    # conn.__enter__() executes: connection open
    s.send(b'GET /index.html HTTP/1.0\r\n')
    s.send(b'Host: www.python.org\r\n')
    s.send(b'\r\n')
    resp = b''.join(iter(partial(s.recv, 8192), b''))
    # conn.__exit__() executes: connection closed
