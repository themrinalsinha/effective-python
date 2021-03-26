"""
Item 9: Avoid else Blocks After for and while loops
"""

for i in range(3):
    print('LOOP', i)
else:
    print('Else Block...')

# Surprisingly, the else block runs immediately after the loop finishes.
# Why is the clause called “else”? Why not “and”? In an if / else statement,
# else means “Do this if the block before this doesn’t happen.” In a
# try / except statement, except has the same definition: “Do this if
# trying the block before this failed.”

# Similarly, else from try / except / else follows this pattern (see Item 65:
# “Take Advantage of Each Block in try / except / else / finally ”) because it
# means “Do this if there was no exception to handle.” try / finally is also
# intuitive because it means “Always do this after trying the block before.”

# Another surprise is that the else block runs immediately if you loop over an
# empty sequence:
for x in []:
    print('Never runs...')
else:
    print('For Else Block...')

# The else block also runs when while loops are initially false
while False:
    print("Never runs")
else:
    print("While else block...")

"""
Things to Remember
✦ Python has special syntax that allows else blocks to immediately
follow for and while loop interior blocks.
✦ The else block after a loop runs only if the loop body did not encoun-
ter a break statement.
✦ Avoid using else blocks after loops because their behavior isn’t
intuitive and can be confusing.
"""
