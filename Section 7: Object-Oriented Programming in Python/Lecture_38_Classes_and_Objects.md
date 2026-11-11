# Lecture 38 — Classes and Objects in Python

**Units covered**: 1. Class as blueprint, object as instance,
2. Writing your first class & `self`,
3. Multiple instances, class attributes & instance independence

---

## Unit 1 — Class as Blueprint, Object as Instance

### Core Concept
A **class** is a template/blueprint that defines what data an object holds (attributes) and what actions it can perform (methods). It does **not** create objects itself — only the instructions for creating them. An **object** is a specific instance created from that blueprint, with its own concrete data.

Lecture examples:
- **Exam form** = class (fields: name, age, electives, father's name); **John Doe's filled form** = object (name: "John Doe", age: 23, electives: math/social science, father: "Kaido")
- **Car** = class; **your red Honda Civic** = object

### What's Actually Happening
The class body defines a namespace — attributes (variables) and methods (functions) that describe the shape and behavior of future instances. No memory is allocated for individual objects at class-definition time; the class just stores the blueprint.

### Why It Matters
This is the mental model for everything that follows: constructors, instance vs class attributes, inheritance. If you don't internalize "class = instructions, object = actual thing," the rest of OOP won't click.

### Minimal Executable Example
```python
# Class = blueprint (instructions only, no object created yet)
class ExamForm:
    pass

# Object = specific instance with concrete data
john = ExamForm()
john.name = "John Doe"
john.age = 23
john.electives = ["Mathematics", "Social Science"]
john.father_name = "Kaido"

print(type(ExamForm))   # <class 'type'> — the class itself is an object
print(type(john))       # <class '__main__.ExamForm'> — instance of the class
```

---

## Unit 2 — Writing Your First Class & `self`

### Core Concept
To create a class: `class Employee:`. Inside, attributes like `company = "HP"` and methods like `def get_salary(self):`. The first parameter of every instance method is `self` — a reference to the specific object the method is being called on.

### What's Actually Happening

**1. Parentheses are required to instantiate**
```python
e = employee        # WRONG — e is just the class object itself
e = employee()      # RIGHT — calls type.__call__ → __new__ + __init__
```
Without `()`, you don't get an object; you get the class. Calling `e.get_salary()` without instantiating raises `TypeError: missing one required positional argument: 'self'` because there's no instance to bind.

**2. `self` is the instance, passed automatically**
When you call `e.get_salary()`, Python translates it to `Employee.get_salary(e)`. The instance `e` is passed as the first argument — that's `self`. So:
- `e.get_salary()` → `self` is `e`
- `e2.get_salary()` → `self` is `e2`

`self` is a **convention, not a keyword** — you could name it `this` or `self_instance`, but `self` is the universal Python convention.

**3. Printing `self` reveals object identity**
```python
print(self)   # <__main__.employee object at 0x104a2c310>
```
Each instance has a unique memory address (`id()`), confirming `e` and `e2` are distinct objects.

**4. Class attributes are shared**
`company = "HP"` defined directly in the class body lives on `Employee.__dict__`. Accessing `e.company` or `e2.company` returns `"HP"` because there's no instance attribute shadowing it — the lookup falls through to the class.

### Why It Matters
- `self` is how a method knows *which* object's data to operate on — the essence of encapsulation
- `()` after the class name is non-optional for instantiation
- Class attributes defined in the body are shared across all instances unless overridden per-instance

### Minimal Executable Example
```python
class Employee:
    company = "HP"   # class attribute — shared by all instances

    def get_salary(self):
        return 34000

# e is the class itself, not an object — no ()
e_wrong = Employee
try:
    e_wrong.get_salary()   # TypeError: missing 'self'
except TypeError as err:
    print("TypeError:", err)

# e1 and e2 are actual instances — ()
e1 = Employee()
e2 = Employee()

print(e1.get_salary())   # 34000 — self is e1
print(e2.get_salary())   # 34000 — self is e2
print(e1.company, e2.company)  # HP HP — shared class attribute
print(id(e1) == id(e2))  # False — different objects, different memory
print(e1.get_salary is e2.get_salary)  # False — new bound method each access
```

---

## Unit 3 — Multiple Instances, Class Attributes & Instance Independence

### Core Concept
One class can create unlimited objects. Each object is independent with its own identity and its own `__dict__` for instance attributes, while sharing class-level attributes and methods defined on the class.

### What's Actually Happening

**1. Instance creation is `type.__call__`**
`Employee()` → `type.__call__(Employee)` → `Employee.__new__(Employee)` allocates, then `Employee.__init__(instance)` initializes. (Default `object.__new__` and `object.__init__` do nothing special here.)

**2. Each instance has its own `__dict__`**
```python
e1.__dict__   # {} — empty initially
e2.__dict__   # {} — empty initially
```
Any attribute you set on `e1` (e.g., `e1.name = "John"`) lives only in `e1.__dict__`; `e2` is unaffected.

**3. Attribute lookup: instance → class**
When you read `e1.company`, Python checks `e1.__dict__` first. Not found → checks `Employee.__dict__` → finds `"HP"`. If you later do `e1.company = "Google"`, it creates an instance attribute that shadows the class attribute for `e1` only; `e2` still sees `"HP"`.

**4. Methods are shared, not duplicated**
`get_salary` lives once in `Employee.__dict__`. Each access `e1.get_salary` creates a *new* bound method object wrapping `e1`, but the underlying function is shared.

### Why It Matters
- Explains why changing one instance never accidentally changes another (crucial for avoiding bugs)
- Class attributes = shared defaults; instance attributes = per-object state
- This distinction is the foundation for Lecture 40 (instance vs class attributes in depth)

### Minimal Executable Example
```python
e1 = Employee()
e2 = Employee()

e1.name = "John Doe"     # instance attribute — lives in e1.__dict__ only
print(e1.name)           # John Doe
print(hasattr(e2, 'name'))  # False — e2 doesn't have it

print(e1.company, e2.company)   # HP HP — both read class attribute
e1.company = "Google"            # shadows for e1 only
print(e1.company, e2.company)   # Google HP — e2 still sees class value
print(e1.__dict__)               # {'name': 'John Doe', 'company': 'Google'}
print(e2.__dict__)               # {} — untouched
```

---

## Key Insight
A class is a first-class object (instance of `type`) — a blueprint with no instances created until you call it with `()`. An object is an instance with its own `__dict__` and memory address. `self` connects methods to the specific object they operate on; class attributes are shared, instance attributes are per-object.
