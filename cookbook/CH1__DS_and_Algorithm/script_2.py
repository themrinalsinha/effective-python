"""
1.3. keeping the last N items

Problem: you want to keep a limited history of the last few items seen during iteration
         or during some other kind of processing.

Solution: keeping a limited history is a perfect use for a collection.deque
"""

from collections import deque


q = deque(maxlen=3)
q.append(1)
q.append(2)
q.append(3)
print(q)

# now the queue is full, if you append anymore value it will start poping out the older value
q.append(4)
print(q)
q.append(5)
print(q)

# more generally, a deque can be used whenever you need a simple queue structure,
# if you don't give it a maximum size, you get an unbounded queue that lets you append
# and pop items on either end.
print("\nwithout maxlen")
q = deque()
q.append(1)
q.append(2)
q.append(3)
q.append(4)
q.append(5)
print(q)
print(f"q.pop() --> {q.pop()}")
print(q)
print(f"q.popleft() --> {q.popleft()}")
print(q)
print(f"q.appendleft(4) --> {q.appendleft(4)}")
print(q)


def search(lines, pattern, history=5):
    previous_lines = deque(maxlen=history)
    for line in lines:
        if pattern in line:
            yield line, previous_lines
        previous_lines.append(line)

with open('script_2.txt') as f:
    for line, prevlines in search(f, 'python', 5):
        for pline in prevlines:
            print(pline, end="")

        print(line, end="")
        print('-' * 20)
