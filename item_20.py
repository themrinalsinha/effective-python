# Item 20 : Use None and Docstrings to specify dynamic default arguments.

# Sometimes you need to use a non-static type as a keyword argument's default value. Eg: You want to print logging messages that are marked with the time of the logged event.
# In the default case you want the message to include the time when the function was called. You might try the following  approaches, assuming the default arguments are reevaluated each time the function is called.

from datetime import datetime
from time     import sleep
import json

def log(message, when = datetime.now()):
    print('%s : %s' % (when, message))

log('Hi there...')
sleep(1)
log('Hi again...\n')
# Note: the timestamps are the same because datetime.now is only executed a single time: when the function is defined. Default argument values are evaluated only once per module load, which usually happens when a programs starts up After the module containing the code is loaded, the datetime.now() default argument will never be evaluated again.
# The convention for achieving the desired result is to provide a default value of None and to document the acutal behavior in the docstring. When your code sees an argument value of None, you allocate the default value accordingly.

def log(message, when = None):
    """Log a message with a timestamp"""
    when = datetime.now() if when is None else when
    print('%s : %s' % (when, message))

log('Hi there...')
sleep(1)
log('Hi again...')

# Using None for default argument values is especially important when the arguments are mutable, say you want to load value encoded as JSON data. If decoding the data fails, you want an empty dictionary to be returned by default.
def decode(data, default = {}):
    try:
        return json.loads(data)
    except ValueError:
        return default
# The problem here is same as the datetime.now() example above. The dictonary specified for default will be shared by all calls to decode because default argument values are only evaluated once (at module load time). This can cause extremely surprising behavior.
foo = decode('bad data')
foo['stuff'] = 5
bar = decode('also bad')
bar['meep'] = 1

print('Foo', foo)
print('Bar', bar)
# Here you'd expect two different dictonaries, each with a single key and value. But modifying one seems to also modify the other. The culprit is that foo and bar are both equal to the default parameter. The were the same dictonary object
assert foo is bar

# This fix is to set the keyword argument default value to None and then  document the behavior in the function's docstring.
def decode1(data, default = None):
    """
        Load json data from a string
        Args:
            data    : JSON data to decode.
            default : value to return if decoding fails. Default to an empty dictonary.
    """
    if default is None:
        default = {}
    try:
        return json.loads(data)
    except ValueError:
        return default

foo = decode1('bad data')
foo['stuff'] = 5
bar = decode1('also bad')
bar['meep'] = 1

print('Foo', foo)
print('Bar', bar)

# Note:
# -> Default arguments are only evaluated once: during function definition at module load time. This can cause odd behaviors for dynamic values like {} or []
# -> Use None as the default value for keyword arguments that have a dynamic value. Document the actual behavior in the funcions docstring. 