# Prefer Helper Classes Over Bookkeeping with Dictionaries with Tuples

# Python's built-in dictionary is wonderful for maintaining dynamic internal state over the lifetime of an object.
# By dynamic, i mean situtaions in which you need to do bookkeeping for an unexpected set of identifiers.

# Eg: say you want to record the grades of a set of students whose names aren't known in advence.
# You can define a class to store the names in a dictinary instead of suing a predefinedattribute for each student.

class SimpleGradebook(object):
    def __init__(self):
        self.grades = {}

    def add_student(self, name):
        self.grades[name] = []

    def report_grade(self, name, score):
        self.grades[name].append(score)

    def average_grade(self, name):
        grades = self.grades[name]
        return sum(grades) / len(grades)

book = SimpleGradebook()
book.add_student('Mrinal')
book.report_grade('Mrinal', 90)
book.report_grade('Mrinal', 80)
book.report_grade('Mrinal', 50)
book.report_grade('Mrinal', 10)
print(book.average_grade('Mrinal'))