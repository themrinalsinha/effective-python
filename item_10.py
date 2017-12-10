# Item 10 : Prefer enumerate Over range.

# The range built in function is useful or loops that iterate over, like a list of string, you can loop directly over the sequence.

flavor_list = ['vanilla', 'chocolate', 'strawberry', 'pecan']
for flavor in flavor_list:
    print('%s is delicious !' % flavor)

# Often, you'll want to iterate over a list and also know the index of the current item in the list.
# Without enumerate.
for i in range(len(flavor_list)):
    flavor = flavor_list[i]
    print('%d : %s' % (i + 1, flavor))

# using enumerate.
for i, flavor in enumerate(flavor_list):
    print('%d : %s' % (i + 1, flavor))

# You can make this even shorter by specifying the number from which enumerate should begin counting (1 in this case)
for i, flavor in enumerate(flavor_list, 1):
    print('%d : %s' % (i, flavor))
