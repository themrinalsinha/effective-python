# Item 12 : Avoide else Blocks After for and while loops.

# Python loops have an extra feature that is not available in most other programming languages you can put an else block immediately after a loops repeated interior block.

for i in range(3):
    print('Loop %d' %i)
else:
    print('Else block\n')
# Surprisingly, the else block runs immediately after the loop finishes.

# Using a break statement in a loop will actually skip the else block.
for i in range(3):
    print('Loop %d' %i)
    if i == 1: break
else:
    print('Else block')

# Another surprise is that the else block will run immediately if you loop over an empty sequence.
for x in []:
    print('Never runs')
else:
    print('\nElse block')

# The else block also runs when while loops are initially false.
while False:
    print('Never runs')
else:
    print('\nElse block\n')

# The rationale for these behaviors is that else blocks after loops are useful when you're using loops to search for something..
# Eg: Yo want to determine whether two numbers are coprime (their only one common divisor is 1)
#  Here i iterate through every possible common divisor and test the numbers. After every option has been tred the loop ends. The else block runs when the numbers are coprime because the loop doesn't encounter a break.
a = 4
b = 9
for i in range(2, min(a, b) + 1):
    print('Testing', i)
    if a % i == 0 and b % i == 0:
        print('Not coprime')
        break
else:
    print('Coprime')

# In practice you wont write code this way. Instead you'd write a helper function to do the calculation. Such a helper function is written in two common styles.
# The first approach is to return early when you find the condition you're looking for. You return the default outcome if you fall through the loop.
def coprime(a, b):
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            return False
    return True
print(coprime(4, 9))

# The second way is to have a result variable that indicates whether you've found what you're looking for in the loop. You break out of the loop as soon as you find something.
def _coprime(a, b):
    is_coprime = True
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            is_coprime = False
            break
    return is_coprime
print(_coprime(4, 9))