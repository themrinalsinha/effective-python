"""
5.2. Printing to file
"""
with open("somefile.txt", "w") as f:
    print("Hello world !", file=f)
# ----------------------------------------------------------------------------------
