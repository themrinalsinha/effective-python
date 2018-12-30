# Concurrency and Parallelism

# Concurrency is when a computer does many different things seemingly at the same time.
# Parallelism is actually doing many different things at the same time.

# The key difference between parallelism and concurrency is speedup. When two distinct paths of execution in a program make forward progress in parallel,
# the time it takes to do the total work is cut in half, the speed of execution is faster by a factor of two. In contrast, concurrent programs may run
# thousand of seperate aths of execution seemingly in parallel but provide no speedup for the total work.

# Python makes it easy to write concurrent programs. Python can also by used to do parallel work through system calls, subprocesses, and C-extension.
# But it can be very difficult to make concurrent python code truly run in parallel. It's important to understand how to beest utilize Python in these
# subtly different situations.
# ==========================================================================

# Item 36: Use subprocess to manage child processes.
# -------------------------------------------------
# Python has battle-hardened libraries for running and managing child processes. This makes Python a great language for
# gluing other tools together, such as command-line utilities.
#
# Child processes started by Python are able to run in parallel, enabling you to use Python to consume all the CPU cores
# of your machine and maximize the throughput of your programs. Although Python itself may be CPU bound, it's easy to use
# python to drive and coordinate CPU-intensive workloads.
#
# Python has had many ways to run subprocesses over the years including popen, popen2, and os.exec*. With the Python of today,
# the best and simplest choice for managing child processes is to use the subprocess build-in module.
#
# Runnig a child process with subprocess is simple. Here the Popen constructor starts the process. The communicate method reads
# the child processes output and waits for termination

from subprocess import Popen, PIPE
proc = Popen(['echo', 'Hello from the child!'], stdout=PIPE)
out, err = proc.communicate()
print(out, err)
print(out.decode('utf-8'))

# Child process will run independently from their parent process, the Python interpreter. Their status can be polled periodically
# while python does other work.
proc = Popen(['sleep', '0.3'])
while proc.poll() is None:
    print('Working...')
print('Exit status ', proc.poll())

# Decoupling the child process from the parent means that the parent process is free to run many child process in parallel. You can do
# this by starting all the child processes together upfront.

from time import time
def run_sleep(period):
    proc = Popen(['sleep', str(period)])
    return proc

start = time()
procs = []
for _ in range(10):
    proc = run_sleep(0.1)
    procs.append(proc)
    # Later you can write for them to finish their I/O and terminate with the communicate method.
for proc in procs:
    proc.communicate()
end = time()
print('Finished in %.3f seconds' % (end-start))
# Note, If these processes ran in sequence, the total delay would be 1 second, not the ~0.1 second I measured.
# -----------------------------------------------------------------------------------------------------------


# You can also pip data from your Python program into a subprocess and retrive its output. This allow you to utilize
# other programs to do work in parallel, Eg: say you want to use the openssl command-line tools to encrypt some data.
# starting the child process with command-line arguments and I/O pipes is easy.
import os

def run_openssl(data):
    env = os.environ.copy()
