# Usse @classmethod polymorphism to construct objects generically

# Ploymorphism: It is the ability to leverage the same interface for different
# underlying forms such as data types or classes. This permits functions to use entities of different types at different times.
# Eg: for OOP in python, this means that a particular object belonging to a particular class can be used in the same way ass if it werea different object belonging to different class.

# Eg. say you're writing , a MapReduce Implementation and you want a common class to rrepresent the input data. Here I define such a class with a read
# method that must be by subclass:

class InputData(object):
    def read(self):
        raise NotImplementedError

# Here I'vea concrete subclass of InputData that reads data from a file on disk:

class PathInputData(InputData):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        return open(self.path).read()

# You could hava any numberr of InputData sublcasses like PathInputData and each of the could implement the standard interface for read to return
# the bytes of data to process. Other InputData subclass could read from the network, decomposed data transparently, etc.,
#
# You'd want a similar abstract interface for the MapReduce worker that consumes the input data in a standard way.

class Worker(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.result     = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError

# Here, I define a concrete subclass of worker to implement the specific MapReduce function I want to apply: a simple newline counter:

class LineCountWorker(Worker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result

# The huge issue with the map reduce function is not generic at all.
# If you want to write another InputData or Worker sublcass, you ould also have to rewrite the generate_inputs, create_worker, and mapreduce functions to match.

# The best way to solve this problem is with @classmethod polymorphism.
# This is exactly liek the instance method polymorphism I used for InputData.read, except that it applies to whole classes instead of their constructed objects.
# Let me apply this idea to the MapReduce classes. Here, I extend the InputData class with a generic class method that's responsible for ccreating new INputData instance using a common interface:


class GenericInputData(object):
    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config):
        raise NotImplementedError

# I have generate_inputs take a dictionary with a set of configuration parameters that are up to the Inputdata concrete subclass to interpret.
# I use the config to find te directory to list for input files:
class PathInputData(GenericInputData):
    def read(self):
        return open(self.path).read()

    @classmethod
    def generate_inputs(cls, config):
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))


