"""
4.1. Manually Consuming an Iterator

Problem: You need to process items in an iterable, but for whatever reason, you can't
         or don't want to use a for loop

Solution: To manually consume an iterable, use the next() function and write you code
          to catch the StopIteration exception.
"""
with open("/etc/passwd") as f:
    try:
        while True:
            line = next(f)
            print(line, end="")
    except StopIteration:
        pass

# Or, without catching exception
with open('/etc/passwd') as f:
    while True:
        line = next(f, None)
        if line is None:
            break
        print(line, end="")

print('- ' * 50)
# ====================================================================================

