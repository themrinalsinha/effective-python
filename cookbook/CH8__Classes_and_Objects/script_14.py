"""
8.19. Implementing Stateful Objects or State Machines

Problem: You want to implement a state machine or an object that operates in a number
         of different states, but don't want to litter your code with a lot of conditionals.
"""

# you might have objects that operate differently according to some kind of internal
# state. For example, consider a simple class representing a connection
class Connection:
    def __init__(self) -> None:
        self.state = 'CLOSED'

    def read(self):
        if self.state != 'OPEN':
            raise RuntimeError("Not open")
        print('reading')

    def write(self, data):
        if self.state != 'OPEN':
            raise RuntimeError("Not open")
        print('writing')

    def open(self):
        if self.state == 'OPEN':
            raise RuntimeError("Already open")
        self.state = 'OPEN'

    def close(self):
        if self.state == 'CLOSED':
            raise RuntimeError("Already closed")
        self.state = 'CLOSED'

# This implementation presents a couple of difficulties. First, the code is complicated
# by the introduction of many conditional checks for the state. Second, the performance is
# degraded because common operations (eg: read() & write()) always check the state before
# proceeding.

# a more elegant approach is to encode each operational state as a separate class and
# arrange for the Connection class to delegate to the state class.
class Connection:
    def __init__(self) -> None:
        self.new_state(ClosedConnectionState)

    def new_state(self, newstate):
        self._state = newstate

    # delegate to the state class
    def read(self):
        return self._state.read(self)

    def write(self, data):
        return self._state.write(self, data)

    def open(self):
        return self._state.open(self)

    def close(self):
        return self._state.close(self)

# connection state base class
class ConnectionState:
    @staticmethod
    def read(conn):
        raise NotImplementedError()

    @staticmethod
    def write(conn, data):
        raise NotImplementedError()

    @staticmethod
    def open(conn):
        raise NotImplementedError()

    @staticmethod
    def close(conn):
        raise NotImplementedError()

# implementation of different states
class ClosedConnectionState(ConnectionState):
    @staticmethod
    def read(conn):
        raise RuntimeError('Not open')

    @staticmethod
    def write(conn, data):
        raise RuntimeError('Not open')

    @staticmethod
    def open(conn):
        conn.new_state(OpenConnectionState)

    @staticmethod
    def close(conn):
        raise RuntimeError('Already closed')

class OpenConnectionState(ConnectionState):
    @staticmethod
    def read(conn):
        print('reading')

    @staticmethod
    def write(conn, data):
        print('writing')

    @staticmethod
    def open(conn):
        raise RuntimeError('Already open')

    @staticmethod
    def close(conn):
        conn.new_state(ClosedConnectionState)

c = Connection()
print(c._state)

c.open()
print(c._state)

c.write('hello')

c.close()
print(c._state)
