# Item 13 : Take advantage of each block in try/except/else/finally

# There are four distinct times that you may want to take action during exception handling in python.

# Finally Block
# One common usage of try/finally is for reliably closing file handles.
handle = open('test_9.txt') # May raise IOError
try:
    data = handle.read() # May run UnicodeDecodeError
finally:
    handle.close() # Always runs after try

# Else Block
# Use try/catch/except to make it clear which exception will be handled by your code and which exceptions will propagate up.
# When the try block doesn't raise an exception, the else block will run. Then else block helps you minimize the amount of code in the try block and improves readability.
# you want to load JSON dictionary dta from a string an dreturn the value of a key in contains.
def load_json_key(data, key):
    try:
        result_dict = json.loads(data)
    except ValueError as e:
        raise KeyError from e
    else:
        return result_dict[key]
    # If the data isn't valid.JSON, then decoding with json.loads will raise a ValueError. The exception is caught by the except block and handled.
    # If the decoding is successful, then the key lookup will occur in the else block.