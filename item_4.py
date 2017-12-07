# Item 4 : Write Helper functions instead of complex expressions


from urllib.parse import parse_qs

my_value = parse_qs('red=5&blue=0&green=', keep_blank_values=True)
# my_value = repr(my_value)
print('RED',my_value.get('red'))
print('BLUE',my_value.get('blue'))
print('GREEN',my_value.get('green'))
print('OPACITY',my_value.get('opacity'))
print('--------------------------------')
# It'd be nice if a default value of 0 was assigned when a parameter supplied or is blank.
# You might choose to do this with boolean expression because it feels like this logic doesn't merit a whole if statement or helper function quite yet.

# Python's syntax makes this choice all too easy.

# The red case works because the key is present in the my_value dictionary. The value is a list with one member: the string '5'. This string implicitly evaluates to True, so red is assigned to the first part of the or expression.
print('RED', my_value.get('red', [''])[0] or 0)
print('BLUE', my_value.get('blue', [''])[0] or 0)

# The green case works because the value in the my_value dictionary is a lst with one member: an empty string. The empty string implicitly evaluated to False, causing the or expression to evaluate to 0.
print('GREEN', my_value.get('green', [''])[0] or 0)

# The opacity case works because  the value in my_values dictionary is altogether. The behavior of the get method is to return its second argument if the key doesn't exists in the dictonary. The default value in this case is a list with one member, an empty string. When opacity isn't found in the dictonary, this code does exactly the same thing as the green case.
print('OPACITY', my_value.get('opacity', [''])[0] or 0)

# Writing a helper function is the best way to go, especially if you need to use this logic repeatidly.
def get_first_int(values, key, default=0):
    found = values.get(key, [''])
    if found[0]:
        found = int(found[0])
    else:
        found = default
    return found
print('--------------------------------')
print(get_first_int(my_value, 'red'))
print(get_first_int(my_value, 'blue'))
print(get_first_int(my_value, 'green'))
print(get_first_int(my_value, 'opacity'))