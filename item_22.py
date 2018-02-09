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

# Now, imagine your requirement change again. You also want to track the weight of each score toward the overall grade in the class
# so midterms and finals are more important than pop quizzes. One way to implement this feature is to change the innermost dictionay
# instead of mapping subjects to grades. we can use the tuple as value.

class WeightGradebook(object):
    #...
    def report_grade(self, name, subject, score, weight):
        by_subject = self.grades[name]
        grade_list = by_subject.setdefault(subject, [])
        grade_list.append(score, weight)

    # Although the changes to report_grade seem simple -- just make the value a tuple -- the average_grade method now has a loop within a loop and is difficult to read.
    def average_grade(self, name):
        by_subject = self.grades[name]
        score_sum, score_count = 0, 0
        for subject, scores in by_subject.items():
            subject_avg, total_weight = 0, 0
            for score, weight in scores:
                # ..
        return score_sum / score_count

book.report_grade('tms', 'Math', 80, 0.10)
    # Using the class has also gotten more difficult. It's unclear what all of the numbers in the positional arguments mean.
    # When you see the complexity like this happen, it's time to make the leap from dictionaries and tuples to a hierarchy of classes.

# # Refactoring of classes
# You can start moving to classes at the bottom of the dependency tree: a single grade. A class seems too heavyweight for such simple information.
# A tuple, though, seems appropriate because grades are immutable.
grades = []
grades.append((95, 0.45))
# ..
total         = sum(score * weight for score, weight in grades)
total_weight  = sum(weight for _, weight in grades)
average_grade = total / total_weight

# The problem is that plain tuples are positional. When you want to associate more info with the grade, like a set of notes
# from the teacher, you'll need to rewrite every usage of the two-tuple to be aware that there are now three items present instead of two.

grades = []
grades.append((95, 0.45, 'Great Job'))
# ..
total         = sum(score * weight for score, weight, _ in grades)
total_weight  = sum(weight for _, weight, _ in grades)
average_grade = total / total_weight

# The pattern of extending tuple longer and longer is similar to deep-ending layers of dictionaries. As soon as you find yourself going longer than a two-tuple. It's time to consider aother data class.

import collections
grade = collections.namedtuple('Grade', ('score', 'weight'))
# These classes can be constructed with positional or keyword arguments. The fields are accessible with named attributes.
# Having named attributes makes it easy to move from a namedtuple to your own class later if your requirement change again and you need to add behaviors to simple data contianers.


