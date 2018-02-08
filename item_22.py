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

# Dictionaries are so easy to use that there's a danger of overextending them to write brittle code.
# Eg: say you want to extend the SimpleGradebook to keep a list of grades by subjects, not just over all.
# you can do this by changing the grades dictionary to map student names (keys) to yet another dictionay (the values). 
# The inner most dictionary will map subjects (the keys) to grades (the values) 

class BySubjectGradebook(object):
    def __init__(self):
        self.grades = {}

    def add_student(self, name):
        self.grades[name] = {}

    def report_grade(self, name, subject, grade):
        by_subject = self.grades[name]
        grade_list = by_subject.setdefault(subject, [])
        grade_list.append(grade)

    def average_grade(self, name):
        by_subject   = self.grades[name]
        total, count = 0, 0
        for grades in by_subject.values():
            total += sum(grades)
            count += len(grades)
        return total / count

book1 = BySubjectGradebook()
book1.add_student('Warlock')
book1.report_grade('Warlock', 'Math', 75)
book1.report_grade('Warlock', 'Math', 85)
book1.report_grade('Warlock', 'Science', 55)
book1.report_grade('Warlock', 'Science', 85)
book1.report_grade('Warlock', 'English', 55)
book1.report_grade('Warlock', 'English', 96)
print(book1.average_grade('Warlock'))
