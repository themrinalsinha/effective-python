# Item 1 : Know which version of python you're using.

# you can use --version flag at terminal with python
# or to do it programatically.

import sys

print(sys.version)
print(sys.api_version)
print(sys.version_info)

# You can parse the result as per your need. Eg:
if sys.version_info.major == 3:
    print('\n\nUSING PYTHON 3\n\n')
else:
    print('\n\nUSING PYTHON 2\n\n')