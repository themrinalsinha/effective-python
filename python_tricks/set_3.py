# Functions are objects
def yell(text):
    return text.upper() + '!'
bark = yell
del yell
# You can delete the function's original name (yell).
# Since another name bark still points to the underlying function
print(bark('Hello'))


