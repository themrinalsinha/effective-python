
"""
7.11. Inlining callback functions

Problem: You’re writing code that uses callback functions, but you’re concerned about the pro‐
         liferation of small functions and mind boggling control flow. You would like some way
         to make the code look more like a normal sequence of procedural steps.

Solution: callback functions can be inlined into a function using generator and coroutine.
          to illustrate, suppose you have a function that performs work and invokes a callback
          as follows.
"""

def apply_async(func, args, *, callback):
    result = func(*args)
    callback(result)

# Now take a look at the following supporting code, which involves an Async class and
# an inline_async decorator.

from queue     import Queue
from functools import wraps

class Async:
    def __init__(self, func, args) -> None:
        self.func = func
        self.args = args

def inlined_async(func):
    @wraps(func)
    def wrapper(*args):
        f = func(*args)
        result_queue = Queue()
        result_queue.put(None)

        while True:
            result = result_queue.get()
            try:
                a = f.send(result)
                apply_async(a.func, a.args, callback=result_queue.put)
            except StopIteration:
                break
    return wrapper

# these two fragments of code will allow you to inline the callback steps using yield
# statement. eg:
def add(x, y):
    return x + y

@inlined_async
def test():
    r = yield Async(add, (2, 3))
    print(r)

    r = yield Async(add, ('hello', 'world'))
    print(r)

    for n in range(10):
        r = yield Async(add, (n, n))
        print(r)

    print('Goodbye')

test()

# Aside from the special decorator and use of yield , you will notice that no callback
# functions appear anywhere (except behind the scenes).
print('- ' * 50)
# ===================================================================================


