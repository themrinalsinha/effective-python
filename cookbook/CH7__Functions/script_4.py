"""
7.10. carrying extra state with callback functions

Problem: you are writing code that relies on the use of callback functions, (eg: event
        handler, completion callbacks etc.) but you want to have the callback function
        carry extra state for use inside the callback function.

Solution: This recipe pertains to the use of callback functions that are found in many
          libraries and frameworks -- especially those related to asynchronous processing.
"""

def apply_async(func, args, *, callback):
    # compute the result
    result = func(*args)

    # invoke the callback with the result
    callback(result)

# in reality, such code might do all sorts of advanced processing involving threads,
# process and timers, but that's not the main focus here. Instead we'are simply focused
# on the invocation of the callback.

def print_result(result):
    print(f'GOT: {result}')

def add(x, y):
    return x + y

apply_async(add, (6, 9), callback=print_result)
apply_async(add, ('hello ', 'world'), callback=print_result)

# As you will notice, the print_result() function only accepts a single argument, which
# is the result. No other information is passed in. This lack of information can sometimes
# present problems when you want the callback to interact with other variables or parts
# of the environment.

# one way to carry extra information in a callback is to use a bound-method instead of
# a simple function. eg: the class keeps an internal sequence number that is increased
# everytime a result is received.

class ResultHandler:
    def __init__(self) -> None:
        self.sequence = 0
    def handler(self, result):
        self.sequence += 1
        print(f"[{self.sequence}] Got: {result}")

# TO use this class, you would create an instance and use the bounded handler as the callback
r = ResultHandler()
apply_async(add, (2, 3), callback=r.handler)
apply_async(add, (5, 6), callback=r.handler)
apply_async(add, ('D & ', 'G'), callback=r.handler)
apply_async(add, ("F ", "U\n"), callback=r.handler)

# As an alternative to a class, you can use a closure to capture state.
def make_handler():
    sequence = 0
    while True:
        result = yield
        sequence += 1
        print(f"[{sequence}] GOT: {result}")

handler = make_handler()
next(handler)
apply_async(add, (2, 3), callback=handler.send)
apply_async(add, (2, 3), callback=handler.send)
apply_async(add, (2, 3), callback=handler.send)
apply_async(add, (2, 3), callback=handler.send)
print()

# Last, but not least, you can also carry state into the callback using an extra argument
# and partial function application

class SequenceNo:
    def __init__(self) -> None:
        self.sequence = 0

def handler(result, seq):
    seq.sequence += 1
    print(f"[{seq.sequence}] GOT: {result}")

seq = SequenceNo()

from functools import partial

apply_async(add, (2, 5), callback=partial(handler, seq=seq))
apply_async(add, (2, 5), callback=partial(handler, seq=seq))
apply_async(add, (2, 5), callback=partial(handler, seq=seq))
apply_async(add, (2, 5), callback=partial(handler, seq=seq))
