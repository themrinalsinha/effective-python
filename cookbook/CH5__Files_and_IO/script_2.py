"""
5.2. Printing to file
"""
with open("somefile.txt", "w") as f:
    print("Hello world !", file=f)
# ----------------------------------------------------------------------------------


"""
5.3. Printing with a different separator or line ending
"""
print("ACME", 50, 90.5)
print("ACME", 50, 90.5, sep=',')
print("ACME", 50, 90.5, sep=',', end="!!\n")
