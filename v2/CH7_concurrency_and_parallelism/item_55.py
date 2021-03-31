"""
Item 55: Use Queue to coordinate work between threads


Python program that do many things concurrently often need to coordinate their work.
one of the most useful arrangements for concurrent work is a pipeline of functions.
"""

# Eg: I want to build a system that will take a constant stream of images from my
# digital camera, resize them, and then add them to a photo gallery online. Such a
# program could be split into three phases of a pipeline. New images are retrieved
# in the first phase. The downloaded images are passed through the resize function
# in the second phase. The resized images are consumed by the upload function in
# the final phase.


def download(item):
    # print(f'[download] - {item}')
    pass

def resize(item):
    # print(f'[resize] - {item}')
    pass

def upload(item):
    # print(f'[upload] - {item}')
    pass


# The first thing i need is a way to hand off work between the pipeline phases. This
# can be modeled as a thread-safe producer-consumer queue
from collections import deque
from threading import Lock

class MyQueue:
    def __init__(self) -> None:
        self.items = deque()
        self.lock  = Lock()

    # The producer, my digital camera, adds new images to the end
    # of the deque of pending items:
    def put(self, item):
        with self.lock:
            self.items.append(item)

    # The consumer, the first phase of the processing pipeline,
    # removes images from the front of the deque of pending items:
    def get(self):
        with self.lock:
            return self.items.popleft()

# Here, I represent each phase of the pipeline as a python thread that takes work from
# one queue like this, runs a function on it, and puts the result on another queue. I
# also track how many times the worker has checked for new input and how much work
# it has completed:
from threading import Thread
import time

class Worker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func         = func
        self.in_queue     = in_queue
        self.out_queue    = out_queue
        self.work_done    = 0
        self.polled_count = 0

    # The trickiest part is that the worker thread must properly handle the case where
    # the input queue is empty because the previous phase hasn't completed its work yet.
    # This happens where I catch the IndexError exception below. You can think of this
    # as a holdup in the assembly line:
    def run(self):
        while True:
            self.polled_count += 1
            try:
                item = self.in_queue.get()
            except IndexError:
                time.sleep(0.01) # No work to do
            else:
                result = self.func(item)
                self.out_queue.put(result)
                self.work_done += 1

# Now, i can connect the three phases together by creating the queues for their
# coordination points and the corresponding worker threads:
download_queue = MyQueue()
resize_queue   = MyQueue()
upload_queue   = MyQueue()
done_queue     = MyQueue()

threads = [
    Worker(download, download_queue, resize_queue),
    Worker(resize, resize_queue, upload_queue),
    Worker(upload, upload_queue, done_queue)
]

# i can start the threads and then inject a bunch of work into the first phase of the
# pipeline. Here i use a plain object instance as a proxy for the real data required by
# the download function.
for thread in threads:
    thread.start()

for _ in range(1000):
    download_queue.put(object())

# Now, i wait for all the items to be processed by the pipeline and end up in the done_queue.
while len(done_queue.items) < 1000:
    # do something useful while waiting
    pass

# This runs properly, but there’s an interesting side effect caused by
# the threads polling their input queues for new work. The tricky part,
# where I catch IndexError exceptions in the run method, executes a
# large number of times:
processed = len(done_queue.items)
polled = sum(t.polled_count for t in threads)
print(f"processed {processed} items after polling {polled} times...")
# =========================================================================================

# Queue to the Rescue
# -------------------
from queue import Queue

my_queue = Queue()

def consumer():
    print('---- consumer waiting ----')
    my_queue.get() # Runs after put() below
    print('---- consumer done ----')

thread = Thread(target=consumer)
thread.start()

# even tough the thread is running first, it won't finish until an item is put on the
# Queue instance and the get method has something to return:
print('producer putting...')
my_queue.put(object()) # runs before get() above
print('producer done...')
thread.join()

# to solve the pipeline backup issue, the Queue lets you specify the maximum amount
# of pending work to allow between two phases. this buffer size causes call to put
# to block when the queue is already full.
# Eg: Here i define that waits for a while before consuming a queue:
my_queue = Queue(1) # Buffer size of 1

def consumer():
    time.sleep(0.1) # wait
    my_queue.get()  # runs second
    print('consumer got 1')
    my_queue.get()  # runs fourth
    print('consumer got 2')
    print('consumer done...')

thread = Thread(target=consumer)
thread.start()

# The wait should allow the producer thread to put both objects on the
# queue before the consumer thread ever calls get . But the Queue size
# is one. This means the producer adding items to the queue will have
# to wait for the consumer thread to call get at least once before the
# second call to put will stop blocking and add the second item to the
# queue

my_queue.put(object())  # runs first
print('producer put 1')

my_queue.put(object()) # runs third
print('producer put 2')
print('producer done')
thread.join()

# The Queue class can also track the progress of work using the task_done method.
# This lets you wait for a phase's input queue to drain and eliminates the need to
# poll the last phase of a pipeline (as with the done_queue above) Ex: here I define
# a consumer thread that calls task_done when it finishes working on an item.

in_queue = Queue()

def consumer():
    print("consumer waiting...")
    work = in_queue.get() # runs second
    print('consumer working')
    # doing work
    print('consumer done')
    in_queue.task_done() # runs third

thread = Thread(target=consumer)
thread.start()

# Now, the producer code doesn't have to join the consumer thread or poll. The producer
# can just wait for the in_queue to finish by calling join on the Queue instance. Even
# once it's empty, the in_queue won't be joinable until after task_done is call for every
# item that was ever enqueued:

print("Producer putting")
in_queue.put(object()) # runs first
print("producer awaiting")
in_queue.join() # runs fourth
print('producer done')
thread.join()
