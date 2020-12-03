"""
9.23. Executing code with local side effects

Problem: You are using exec() to execute a fragment of code in the scope of the caller,
         but after execution, none of its results seem to be visible.

Solution: To better understand the problem, try a little experiment. First, execute a fragment
          of code in the globe namespace.
"""

a = 13
exec("b = a + 1")
print(a, exec("b = a + 1"))

def test():
    a = 13
    exec('b = a + 1')
    print(b)

test()
# ---------------------------

def test():
    a = 13
    loc = locals()
    exec("b = a + 1")
    b = loc["b"]
    print(b)

test()
# ---------------------------

def test2():
    x = 0
    loc = locals()
    print(f"Before: {loc}")
    exec("x += 1")
    print(f"After: {loc}")
    print(f"x = {x}")

test2()
# ---------------------------

def test3():
    x = 0
    loc = locals()
    print(loc)
    exec('x += 1')
    print(loc)
    locals()
    print(loc)

test3()
# ---------------------------
