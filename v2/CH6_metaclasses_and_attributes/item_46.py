"""
Item 46: Use Descriptors for Reusable @property Methods

The big problem with the @property built-in is reuse. The method is decorates can't
be reused for multiple attributes of the same class. They also can't be reused by
unrelated classes.
"""

# I want a class to validate that the grade received by a student on a homework
# assignment is a percentage:
class Homework:
    def __init__(self) -> None:
        self._grade = 0

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must between 0 and 100')
        self._grade = value

# using @property makes this class easy to use:
galileo = Homework()
galileo.grade = 95

# say that i also want to give the student a grade for an exam, where the exam has
# multiple subjects, each with a separate grade
class Exam:
    def __init__(self) -> None:
        self._writing_grade = 0
        self._math_grade    = 0

    @staticmethod
    def _check_grade(value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')

    # this quickly gets tedious. For each section of the exam i need to add a new
    # @property and related validation:
    @property
    def writing_grade(self):
        return self._writing_grade

    @writing_grade.setter
    def writing_grade(self, value):
        self._check_grade(value)
        self._writing_grade = value

    @property
    def math_grade(self):
        return self._math_grade

    @math_grade.setter
    def math_grade(self, value):
        self._check_grade(value)
        self._math_grade = value

    # Also, this approach is not general. If I want to reuse the percentage validation
    # in other classes beyond homework and exams, I'll need to write the @property
    # boilerplate and _check_grade method over and over again.



# The betweer way to do this in Python is to use a descriptor. The descriptor
# protocol defines how attribute access is interpreted by the language. A descriptor
# class can provide __get__ and __set__ methods that let you reuse the grade
# validation behavior without boilerplate.

# Here, I define a new class called Exam with class attributes that are Grade instances.
# The Grade class implements the descriptor protocol:

class Grade:
    def __get__(self, instance, instance_type):
        pass

    def __set__(self, instance, value):
        pass

class Exam:
    math_grade    = Grade()
    writing_grade = Grade()
    science_grade = Grade()

# Before I explain how the Grade class works, it's important to understand what python
# will do when such descriptor attributes are accessed on an Exam instance. When i assign
# a property:

exam = Exam()
exam.writing_grade = 40

# It is interpreted as -
Exam.__dict__['writing_grade'].__set__(exam, 40)

# It is retrieved as -
Exam.__dict__['writing_grade'].__set__(exam, Exam)


# ===================================================================================

class Grade:
    def __init__(self) -> None:
        self._value = 0

    def __get__(self, instance, instance_type):
        return self._value

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._value = value


# Unfortunately, this is wrong and results in broken behavior. Accessing
# multiple attributes on a single Exam instance works as expected:
class Exam:
    math_grade    = Grade()
    writing_grade = Grade()
    science_grade = Grade()

first_exam = Exam()
first_exam.writing_grade = 82
first_exam.science_grade = 99

print('Writing: ', first_exam.writing_grade)
print('Science: ', first_exam.science_grade)


second_exam = Exam()
second_exam.writing_grade = 75
print(f'\nSecond {second_exam.writing_grade} is right')
print(f'First {first_exam.writing_grade} is wrong; should be 82')
# ====================================================================================

# To solve this, I need the Grade class to keep track of its value for each unique
# Exam instance. I can do this by saving the per-instance state in a dictionary:

class Grade:
    def __init__(self) -> None:
        self._values = {}

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._values[instance] = value

# This implementation is simple and works well, but there's still one gotcha: It
# leaks memory. The _values dictionary holds a reference to every instance of Exam
# ever passed to __set__ over the lifetime of the program. This causes instances to
# never have their reference count go to zero, preventing cleanup by the garbage
# collector.

# To fix this, I can use Python's weakref built-in module. The module provides
# a special class called WeakKeyDictionary that can take the place of the simple
# dictionary used for _values.

from weakref import WeakKeyDictionary

class Grade:
    def __init__(self) -> None:
        self._values = WeakKeyDictionary()

    def __get__(self, instance, instance_type):
        pass

    def __set__(self, instance, value):
        pass

    # Using this implementation of the Grade descriptor, everything works as expected

"""
Things to Remember
✦ Reuse the behavior and validation of @property methods by defining your own descriptor classes.
✦ Use WeakKeyDictionary to ensure that your descriptor classes don’t cause memory leaks.
✦ Don’t get bogged down trying to understand exactly how __getattribute__ uses the descriptor protocol for getting and setting attributes.
"""
