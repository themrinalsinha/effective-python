# Item 19 : Provide optional behavior with keyword arguments.

# All positional arguments to Python functions can also be passed by keyword, where the name of the argument is used in an assignment within the parentheses of a function call.

def flow_rate(weight_diff, time_diff):
    return weight_diff / time_diff

weight_diff = 0.5
time_diff   = 3
flow = flow_rate(weight_diff, time_diff)
print('%.3f Kg per second.' % flow)

# It would be helpful to use the last sensor measurements larger time scales, like hours or days. You can provide this behariour in the same function by adding an argument for the time  period scaling factor.
def flow_rate1(weight_diff, time_diff, period):
    return (weight_diff / time_diff) * period
flow = flow_rate1(weight_diff, time_diff, 2)
print('%.3f Kg per second.' % flow)

# To make this less noisy, I can give the period argument a default value.
def flow_rate2(weight_diff, time_diff, period = 3):
    return (weight_diff / time_diff) * period
flow = flow_rate2(weight_diff, time_diff)
print('%.3f Kg per second.' % flow)

# It provide a powerful way to extend a function's parameters while remaining backwards compatible with existing callers. This lets you provide additional functionality without having to migrate a lot of code, reducing the chance of introducing bugs. 

# Note:
# -> Function arguments can be specified by position or by keyword.
# -> Keywords make it clear what the purpose of each argument is when it would be confusing with only positional arguments.
# -> Keyword arguments with default values make it easy to add new behaviors to a function, especially when the funciton has existing callers.
# -> Optional keyword arguments should always be passed by keyword instead of by position. 