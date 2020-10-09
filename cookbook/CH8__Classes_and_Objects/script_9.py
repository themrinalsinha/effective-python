"""
8.12. Defining an interface or abstract base class

Problem: you want to define a class that serves as an interface or abstract base class
         which you can perform type checking and ensure that certain methods are implemented
         in subclass.

Solution: To define an abstract base class, use the abc module
"""
from abc import ABCMeta, abstractmethod

class IStream(metaclass=ABCMeta):
    @abstractmethod
    def read(self, maxbytes=-1):
        pass

    @abstractmethod
    def write(self, data):
        pass

# A central feature of an abstract class is that it cannot be instantiated directly.
# eg: a = IStream() // will throw TypeError

class SocketStream(IStream):
    def read(self, maxbytes=-1):
        pass

    def write(self, data):
        pass

"""
A major use of abstract base classes is in code that wants to enforce an expected pro‐
gramming interface. For example, one way to view the IStream base class is as a high-
level specification for an interface that allows reading and writing of data.
"""

def serialize(obj, stream):
    if not isinstance(stream, IStream):
        raise TypeError("Expected an IStream")

# It should be noted that @abstractmethod can also be applied to static methods, class
# methods, and properties. You just need to make sure you apply it in the proper sequence
# where @abstractmethod appears immediately before the function definition
