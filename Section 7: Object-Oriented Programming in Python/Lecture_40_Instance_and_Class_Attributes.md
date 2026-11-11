# Lecture 40 — Instance and Class Attributes

**Units covered**: 1. Instance vs class attributes: definition & lookup,
2. Accessing class attributes directly & shadowing,
3. Object introspection with `dir()`

---

## Unit 1 — Instance vs Class Attributes: Definition & Lookup

### Core Concept
A class can hold two kinds of attributes:

| Kind | Where defined | Lives in | Shared? |
|---|---|---|---|
| **Class attribute** | Directly in the class body (`company = "Assos"`) | `Employee.__dict__` | Yes — all instances see the same value |
| **Instance attribute** | Via `self.attr = value` (usually in `__init__`) | `self.__dict__` | No — belongs to one object only |

When you read `e1.company`, Python follows this lookup order:
1. `e1.__dict__` — instance attribute? If yes, return it (instance wins).
2. `Employee.__dict__` — class attribute? If yes, return it.
3. Base classes following `Employee.__mro`.

### What's Actually Happening
```python
class Employee:
    company = "Assos"   # class attribute — lives in Employee.__dict__

    def __init__(self, salary, name, bond, company=None):
        self.salary = salary     # instance attribute — lives in e1.__dict__
        self.name = name
        self.bond = bond
        if company is not None:
            self.company = company   # instance attribute — shadows class attr
```

- `company = "Assos"` at class level is stored once in `Employee.__dict__`.
- `self.company = company` inside `__init__` writes `{"company": "Tesla"}` into `e1.__dict__`.
- Reading `e1.company` finds the instance attribute first and returns `"Tesla"`.
- Reading `e2.company` (no instance attribute) falls through to `Employee.__dict__` and returns `"Assos"`.

### Why It Matters
- Class attributes = shared defaults for all instances (company name, tax rate, etc.).
- Instance attributes = per-object state; changing one never affects another.
- The lookup order explains why an instance attribute with the same name "hides" the class attribute when accessed through the object.

### Minimal Executable Example
```python
class Employee:
    company = "Assos"   # class attribute

    def __init__(self, salary, name, bond, company=None):
        self.salary = salary
        self.name = name
        self.bond = bond
        if company is not None:
            self.company = company   # instance attribute

e1 = Employee(34000, "John Doe", 4, company="Tesla")
e2 = Employee(50000, "Jane Smith", 2)

print(e1.company)        # Tesla — instance attribute present, wins
print(e2.company)        # Assos — no instance attr, falls back to class attribute
print(Employee.company)  # Assos — class attribute itself
```

---

## Unit 2 — Accessing Class Attributes Directly & Shadowing

### Core Concept
If you want the class attribute *regardless* of whether an instance has shadowed it, access it through the class name: `Employee.company`. This always returns the class attribute, bypassing any instance-level shadowing.

### What's Actually Happening
```python
e1.company        # Tesla — instance attribute shadows
Employee.company  # Assos — always the class attribute, no shadowing possible
```

`Employee.company` reads `Employee.__dict__["company"]` directly. It never consults `e1.__dict__`, so instance shadowing is irrelevant here.

### Why It Matters
- Use `instance.attr` when you want the object's effective value (instance override if present, else class default).
- Use `ClassName.attr` when you specifically need the class-level default, unaffected by instance mutations.
- This is the mechanism behind reading shared configuration, counters, or constants that belong to the class as a whole.

### Minimal Executable Example
```python
class Employee:
    company = "Assos"

    def __init__(self, company=None):
        if company is not None:
            self.company = company

e1 = Employee("Tesla")
print(e1.company)        # Tesla — instance shadow
print(Employee.company)  # Assos — class attribute, always
```

---

## Unit 3 — Object Introspection with `dir()`

### Core Concept
**Object introspection** is examining an object at runtime to discover its attributes and methods. In Python, `dir(obj)` returns a list of all attribute and method names available on that object.

### What's Actually Happening
```python
dir(e1)
# ['__class__', '__delattr__', ..., '__init__', ..., '__dict__', ...,
#  'company', 'get_info', 'get_salary', 'name', 'salary', ...]
```

`dir(e1)` includes:
- **User-defined attributes/methods** — `name`, `salary`, `bond`, `company`, `get_info`, `get_salary` (the ones you wrote).
- **Dunder methods** — `__init__`, `__str__`, `__repr__`, `__dict__`, `__class__`, `__module__`, etc. (built-in Python machinery).

The lecture notes these dunder methods will be covered in later videos.

### Why It Matters
- `dir()` is a debugging and exploration tool — see what an object supports without reading source code.
- It confirms methods live on the class but are accessible through instances.
- It's the first step toward understanding Python's dynamic object model (`__dict__`, `__class__`, etc.) covered in subsequent lectures.

### Minimal Executable Example
```python
e1 = Employee(34000, "John Doe", 4)
print("get_info" in dir(e1))      # True — method accessible
print("salary" in dir(e1))        # True — instance attribute
print("__init__" in dir(e1))      # True — dunder method present
print("company" in dir(e1))       # True — resolved via class attribute
```

---

## Key Insight
Class attributes are shared defaults stored on the class; instance attributes are per-object state stored on `self.__dict__`. Attribute lookup checks the instance first, then the class. To bypass instance shadowing, read through the class name (`Employee.company`). Use `dir(obj)` to introspect everything available on an object at runtime.
