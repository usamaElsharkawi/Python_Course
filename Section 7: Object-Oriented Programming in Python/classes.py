# Section 7: Object-Oriented Programming in Python — Complete Code Reference
# Covers Lectures 37–42: Classes/Objects, Constructors, Instance/Class Attributes,
# Inheritance & Polymorphism, Operator Overloading

# ============================================================
# Lecture 38 — Classes and Objects
# Class = blueprint/template. Object = instance created from it.
# ============================================================

class ExamForm:
    pass

john = ExamForm()
john.name = "John Doe"
john.age = 23
john.electives = ["Mathematics", "Social Science"]
john.father_name = "Kaido"

# print(type(ExamForm))   # <class 'type'> — classes are objects too
# print(type(john))       # <class '__main__.ExamForm'>


class Employee:
    company = "Assos"           # class attribute — shared by all instances

    def get_salary(self):       # self = the object being called on
        return 34000


e1 = Employee()
e2 = Employee()

# print(e1.get_salary())   # 34000 — self is e1
# print(e2.get_salary())   # 34000 — self is e2
# print(e1.company, e2.company)   # Assos Assos — shared class attribute
# print(id(e1) == id(e2))   # False — different objects


# ============================================================
# Lecture 39 — Constructors (__init__)
# ============================================================

class Employee2:
    def __init__(self, salary, name, bond):
        self.salary = salary    # instance attribute — lives in self.__dict__
        self.name = name
        self.bond = bond

    def get_salary(self):
        return self.salary

    def get_info(self):
        print(f"The name of the employee is {self.name}")
        print(f"Salary is {self.salary}")
        print(f"The bond is for {self.bond} years")


e1 = Employee2(34000, "John Doe", 4)
e2 = Employee2(50000, "Jane Smith", 2)

# print(e1.get_salary())   # 34000
# print(e2.get_salary())   # 50000
# e1.get_info()            # John Doe / 34000 / 4 years
# e2.get_info()            # Jane Smith / 50000 / 2 years
# print(e1.__dict__)       # {'salary': 34000, 'name': 'John Doe', 'bond': 4}
# print(e2.__dict__)       # {'salary': 50000, 'name': 'Jane Smith', 'bond': 2}


# ============================================================
# Lecture 40 — Instance vs Class Attributes
# ============================================================

class Employee3:
    company = "Assos"   # class attribute

    def __init__(self, salary, name, bond, company=None):
        self.salary = salary
        self.name = name
        self.bond = bond
        if company is not None:
            self.company = company   # instance attribute — shadows class attr


e1 = Employee3(34000, "John Doe", 4, company="Tesla")
e2 = Employee3(50000, "Jane Smith", 2)

# print(e1.company)        # Tesla — instance attribute wins
# print(e2.company)        # Assos — falls back to class attribute
# print(Employee3.company) # Assos — always the class attribute

# Object introspection
# print(dir(e1))           # lists all attributes & methods (dunder + user-defined)


# ============================================================
# Lecture 41 — Inheritance and Polymorphism
# ============================================================

class Animal:
    location = "Australia"   # inherited class attribute

    def __init__(self, name):
        self.name = name

    def speak(self):
        print("Generic animal sound")


class Dog(Animal):           # child class inherits from parent
    def __init__(self, name, breed):
        super().__init__(name)   # initialize parent part (name)
        self.breed = breed       # child's own part

    def speak(self):           # method overriding
        super().speak()          # call parent's speak
        print("Woof")


class Cat(Animal):
    def speak(self):
        print("Meow")


a = Animal("Generic")
d = Dog("Bruno", "Labrador")
c = Cat("Milo")

# print(d.name)       # Bruno — from parent __init__ via super()
# print(d.breed)      # Labrador — child's own attribute
# print(d.location)   # Australia — inherited class attribute
# d.speak()           # Generic animal sound / Woof — overridden + super()
# c.speak()           # Meow — polymorphism: same method name, different behavior

# Polymorphism in action
# for creature in (a, d, c):
#     creature.speak()


# ============================================================
# Lecture 42 — Operator Overloading
# ============================================================

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Point(self.x * other.x, self.y * other.y)

    def __truediv__(self, other):
        return Point(self.x / other.x, self.y / other.y)

    def print_point(self):
        print(f"x is {self.x} and y is {self.y}")


p1 = Point(3, 2)
p2 = Point(6, 3)

# p = p1 + p2          # Point(9, 5) — via __add__
# p.print_point()      # x is 9 and y is 5
# (p1 - p2).print_point()   # x is -3 and y is -1
# (p1 * p2).print_point()   # x is 18 and y is 6
# (p1 / p2).print_point()   # x is 0.5 and y is 0.66...
