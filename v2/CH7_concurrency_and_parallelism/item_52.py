"""
---------------- NOTE ----------------
`Concurrency`: It enables a computer to do many different things seemingly at the same time.
Eg: on a computer with one CPU core, the operating system rapidly changes which program is
    running on the single processor. In doing so, it interleaves execution of the programs,
    providing the illusion that the programs are running simultaneously.

`Parallelism`: It in contrast, involves actually doing many different things at the same time.
A computer with multiple CPU cores can execute multiple programs simultaneously. Each CPU core
core runs the instructions of a separate program, allowing each program to make forward progress
during the same instant.


Within a single program, concurrency is a tool that makes it easier for programmers to solve
certain types of problems. Concurrent programs enable many distinct paths of execution, including
separate streams of I/O, to make forward progress in a way that seems to be both simultaneous
and independent.

The key difference between parallelism and concurrency is speedup. When two distinct paths of
execution in a program make forward progress in parallel, the time it takes to do that total
work is cut in half; the speed of execution is faster by a factor of two. In contrast, concurrent
programs may run thousands of separate paths of execution seemingly in parallel but provide
no speedup for the total work.

Python makes it easy to write concurrent programs in a variety of styles. Threads support
a relatively small amount of concurrency while coroutines enable vast numbers of concurrent
functions. Python can also be used to do parallel work through system calls, subprocesses and
C extensions. But it can be very difficult to make concurrent python code truly in parallel.

It is important to understand how to best utilize Python in these different situations.
"""

"""
Item 52: Use subprocess to manage child process

python has battle-hardened libraries for running and managing child processes. This makes
it great language for gluing together other tools, such as command-line utilities. When existing
shell scripts get complicated, as they often do over time, graduating them to a rewrite in
Python for the sake of readability and maintainability is a natural choice.

child processes started bu python are able to run in parallel, enabling you to use python to
consume all the CPU cores of a machine and maximize the throughput of programs.

Although python itself may be CPU bound, it's easy to use python to drive and coordinate
CPU-intensive workloads.

Python has many way to run subprocesses (eg: os.popen, os.exec) but the best choice for
managing child processes is to use the subprocess built-in module. Running a child process
with subprocess is simple. Here, i use the module's run convenience function to start a
process, read its output, and verify that it terminated cleanly.
"""

import subprocess
from sys import stdin, stdout

result = subprocess.run(
    ['echo', 'hello from the other side!'],
    capture_output=True,
    encoding='utf-8',
)

result.check_returncode() # No exception means clean exit
print(result.stdout)

# child process run independently from their parent process, the python interpreter.
# If I create a subprocess using the Popen class instead of the run function. I can
# poll child process status periodically while Python does other work.

proc = subprocess.Popen(['sleep', '1'])
while proc.poll() is None:
    print('working...')

# decoupling the child process from the parent frees up the parent process to run
# many child processes in parallel. Here, i do this by starting all the child process
# together with Popen upfront.

import time

start = time.time()
sleep_procs = []
for _ in range(10):
    proc = subprocess.Popen(['sleep', '1'])
    sleep_procs.append(proc)

# Later i wait for them to finish their I/O and terminate with the communicate method:
for proc in sleep_procs:
    proc.communicate()

end = time.time()
delta = end - start
print(f'finished in {delta:.3} seconds')

# If these processes ran in sequence, the total delay would be 10 seconds
# or more rather than the ~1 second that I measured.

# You can also pipe data from a python program into a subprocess and retrieve its output.
# This allows you to utilize many other programs to do work in parallel.
# Ex: say that i want to use the openssl command line tool encryption some data. Starting
#     child process with command-line argument and I/O pipes is easy:

import os

def run_encrypt(data):
    env = os.environ.copy()

    env['password'] = 'zf7ShyBhZOraQDdE/FiZpm/m/8f9X+M1'
    proc = subprocess.Popen(
        ['openssl', 'enc', '-des3', '-pass', 'env:password'],
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )

    proc.stdin.write(data)
    proc.stdin.flush()
    return proc

# here, i pipe random bytes into the encryption function, but in practice this input
# pipe would be fed data from user input, a file handle, a network socket, and so on:

procs = []
for _ in range(3):
    data = os.urandom(10)
    proc = run_encrypt(data)
    procs.append(proc)

# The I/O between the child processes happens automatically once they are started. All
# i need to do is wait for them to finish and print the final output:

proc = subprocess.Popen(['sleep', '10'])
try:
    proc.communicate(timeout=0.1)
except subprocess.TimeoutExpired:
    proc.terminate()
    proc.wait()
print('Exit status: ', proc.poll())

"""
Things to Remember

✦ Use the subprocess module to run child processes and manage their
  input and output streams.

✦ Child processes run in parallel with the Python interpreter, enabling
  you to maximize your usage of CPU cores.

✦ Use the run convenience function for simple usage, and the Popen
  class for advanced usage like UNIX-style pipelines.

✦ Use the timeout parameter of the communicate method to avoid dead-
  locks and hanging child processes.
"""
