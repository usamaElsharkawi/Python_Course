# Lecture 47 — Magic/Dunder Methods

**Units covered**: 1. What dunder methods are & `__init__`,
2. `__str__` vs `__repr__`,
3. `__len__`

---

## Unit 1 — What Dunder Methods Are & `__init__`

### Core Concept
Dunder (double underscore) methods are special methods that let objects interact with built-in Python operators, functions, and language constructs. They enable operator overloading and customize default Python behavior.

### What's Actually Happening
```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

e = Employee("Harry", 43566)
print(e.name, e.salary)   # Harry 43566
```

- `__init__` is a dunder method — the constructor
- When you call `Employee("Harry", 43566)`, Python automatically invokes `__init__` with those arguments
- `self.name = "Harry"`, `self.salary = 43566` are set on the new instance

### Why It Matters
- `__init__` is called by default whenever you instantiate a class
- It's the entry point for object initialization — the first dunder method most programmers encounter
- Dunder methods let you hook into Python's language features (printing, length, operators, etc.)

### Minimal Executable Example
```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

e = Employee("Harry", 43566)
print(e.name, e.salary)   # Harry 43566
```

---

## Unit 2 — `__str__` vs `__repr__`

### Core Concept
`__str__` and `__repr__` both return a string representation of an object, but they serve different audiences:

| Method | Audience | Used by | Purpose |
|---|---|---|---|
| `__str__` | End users | `print()`, `str()` | Readable, friendly output |
| `__repr__` | Developers | `repr()`, interactive console | Debugging, unambiguous representation |

### What's Actually Happening
```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def __str__(self):
        return f"The name is {self.name} and the salary is {self.salary}"

    def __repr__(self):
        return f"name is {self.name}\nsalary is {self.salary}"

e = Employee("Harry", 43566)

print(e)           # invokes __str__ → "The name is Harry and the salary is 43566"
print(str(e))      # same as above
print(repr(e))     # invokes __repr__ → "name is Harry\nsalary is 43566"
```

- `print(e)` → Python calls `__str__` implicitly
- `str(e)` → explicit call to `__str__`
- `repr(e)` → explicit call to `__repr__`

### Why It Matters
- `__str__` = user-facing presentation (what the end user sees)
- `__repr__` = developer-facing debugging (what you see in the console/interactive interpreter)
- Without `__str__`, `print(e)` shows `<__main__.Employee object at 0x...>` (the default object representation)

### Minimal Executable Example
```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def __str__(self):
        return f"The name is {self.name} and the salary is {self.salary}"

    def __repr__(self):
        return f"name is {self.name}\nsalary is {self.salary}"

e = Employee("Harry", 43566)
print(str(e))    # The name is Harry and the salary is 43566
print(repr(e))   # name is Harry\nsalary is 43566
```

---

## Unit 3 — `__len__`

### Core Concept
`__len__` lets you define what `len(obj)` means for your custom objects. Without it, `len(employee_object)` raises `TypeError: object of type 'Employee' has no len()`.

### What's Actually Happening
```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def __len__(self):
        return len(self.name)   # length of the name attribute

e = Employee("Harry", 43566)
print(len(e))   # 5 — "Harry" has 5 characters
```

- `len(e)` → `e.__len__()` → returns `len(self.name)`
- The lecture defines "length of an employee" as "number of characters in their name"

### Why It Matters
- Makes your objects work with Python's built-in `len()` function
- You define what "length" means for your domain (could be name length, number of projects, list size, etc.)
- Part of the same dunder family as `__add__`, `__sub__` (covered in Lecture 42 operator overloading)

### Minimal Executable Example
```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def __len__(self):
        return len(self.name)

e = Employee("Harry", 43566)
print(len(e))   # 5
```

---

## Key Insight
Dunder methods (`__init__`, `__str__`, `__repr__`, `__len__`, `__add__`, etc.) let your custom objects participate in Python's built-in language features. Define them to control how your objects are constructed, displayed, measured, and combined with operators.
