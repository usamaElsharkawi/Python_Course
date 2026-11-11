# Lecture 46 — Static & Class Methods

**Units covered**: 1. Instance methods (default, `self`),
2. Static methods (`@staticmethod`, no `self`/`cls`),
3. Class methods (`@classmethod`, `cls`),
4. Comparison & attribute lookup recap

---

## Unit 1 — Instance Methods (Default, `self`)

### Core Concept
Instance methods are the default — every method you define inside a class without a decorator is an instance method. Python automatically passes the instance (`self`) as the first argument when you call it on an object.

### What's Actually Happening
```python
class Employee:
    company = "HP"   # class attribute

    def __init__(self, name, salary):
        self.name = name     # instance attribute
        self.salary = salary # instance attribute

    def print_info(self):    # instance method — self is automatic
        return f"The name is {self.name} and the salary is {self.salary}"

e1 = Employee("Jack", 34555)
e2 = Employee("Jill", 34355)

print(e1.print_info())   # The name is Jack and the salary is 34555
print(e2.print_info())   # The name is Jill and the salary is 34355
```

- `e1.print_info()` → `Employee.print_info(e1)` — `e1` is bound to `self`
- `self.name`, `self.salary` read from `e1.__dict__`
- Changing `e2.salary` only affects `e2`, not `e1`

### Class vs instance attribute access
```python
print(Employee.company)   # HP — class attribute accessible via class name
print(e1.company)         # HP — also accessible via instance (falls through to class)
# print(Employee.name)    # AttributeError — name is an instance attribute, not on the class
```

### Why It Matters
- Instance methods operate on instance state (`self.__dict__`)
- `self` is passed automatically — you don't pass it manually
- Class attributes are shared; instance attributes are per-object

### Minimal Executable Example
```python
class Employee:
    company = "HP"

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def print_info(self):
        return f"The name is {self.name} and the salary is {self.salary}"

e1 = Employee("Jack", 34555)
print(e1.print_info())   # The name is Jack and the salary is 34555
print(Employee.company)  # HP
```

---

## Unit 2 — Static Methods (`@staticmethod`, no `self`/`cls`)

### Core Concept
A static method doesn't receive `self` or `cls` automatically. It's a plain function that happens to live inside a class — used for utility logic that doesn't need instance or class state.

### What's Actually Happening
```python
class Employee:
    company = "HP"

    @staticmethod
    def sum(a, b):
        return a + b

e2 = Employee("Jill", 34355)
print(e2.sum(5, 23))   # 28 — no self passed
```

### The problem without `@staticmethod`
```python
def sum(a, b):           # no self
    return a + b

e2.sum(5, 23)            # TypeError: sum() takes 2 positional arguments but 3 were given
```
Python tries to pass `e2` as the first argument (instance method default), so `sum` receives `(e2, 5, 23)` = 3 args but only accepts 2.

### With `@staticmethod`
- No `self` is passed, even when called via `e2.sum(...)`
- Can be called on the class too: `Employee.sum(5, 23)` → `28`
- Doesn't access `self.name`, `self.salary`, or `cls.company` — pure utility

### Why It Matters
- Use when you need a function logically grouped with the class but that doesn't touch instance/class state
- Common for utility/math operations (harmonic mean, average, validation helpers)
- Avoids accidentally passing a "heavy" object you don't need

### Minimal Executable Example
```python
class Employee:
    @staticmethod
    def sum(a, b):
        return a + b

print(Employee.sum(5, 23))   # 28
e = Employee("X", 1)
print(e.sum(5, 23))          # 28 — works on instance too, but self is NOT passed
```

---

## Unit 3 — Class Methods (`@classmethod`, `cls`)

### Core Concept
A class method receives the class itself (`cls`) as the first argument automatically. It can read and modify class attributes, and changes affect all instances.

### What's Actually Happening
```python
class Employee:
    company = "HP"

    @classmethod
    def print_company(cls):
        print(cls.company)   # HP — cls is Employee

    @classmethod
    def change_company(cls, new_company):
        cls.company = new_company   # modifies the class attribute

e1 = Employee("Jack", 34555)

e1.print_company()           # HP
e1.change_company("Acer")
e1.print_company()           # Acer
print(Employee.company)      # Acer — changed for the whole class
```

- `cls` is bound to `Employee` (the class), not to any instance
- `cls.company = new_company` writes to `Employee.__dict__` — affects all instances
- Called on instance (`e1.change_company(...)`) or class (`Employee.change_company(...)`), `cls` is still the class

### Why It Matters
- Factory methods / alternative constructors (common pattern: `cls(...)`)
- Modifying class state that should propagate to all instances
- Accessing class attributes without needing an instance

### Minimal Executable Example
```python
class Employee:
    company = "HP"

    @classmethod
    def print_company(cls):
        print(cls.company)

    @classmethod
    def change_company(cls, new_company):
        cls.company = new_company

e1 = Employee("Jack", 34555)
e1.print_company()       # HP
e1.change_company("Acer")
print(Employee.company)  # Acer
```

---

## Unit 4 — Comparison & Attribute Lookup Recap

| Method type | Decorator | First arg | Can access `self`? | Can access `cls`? | Typical use |
|---|---|---|---|---|---|
| Instance | none | `self` | ✅ | ❌ | Instance state/behavior |
| Static | `@staticmethod` | none | ❌ | ❌ | Utility functions |
| Class | `@classmethod` | `cls` | ❌ | ✅ | Class state, factories |

### Attribute lookup order (for `e.company`)
1. `e.__dict__` — instance attribute?
2. `Employee.__dict__` — class attribute? (falls through here if not in instance)

So `e1.company` returns `"HP"` (class attribute) because `e1` has no instance attribute `company`. But `Employee.name` raises `AttributeError` because `name` only exists on instances, not the class.

### When to use which
- Need instance data (`self.name`)? → Instance method
- Need class data (`cls.company`) or to modify class state? → Class method
- Pure utility, no state needed? → Static method

### Minimal Executable Example (all three together)
```python
class Employee:
    company = "HP"

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def print_info(self):              # instance method
        return f"{self.name}: {self.salary}"

    @staticmethod
    def sum(a, b):                     # static method
        return a + b

    @classmethod
    def print_company(cls):            # class method
        print(cls.company)

e = Employee("Jack", 34555)
print(e.print_info())      # Jack: 34555
print(e.sum(5, 23))        # 28
e.print_company()          # HP
```

---

## Key Insight
Instance methods get `self` automatically and work with instance state. Static methods get nothing automatically and are pure utilities grouped inside a class. Class methods get `cls` automatically and can read/modify class-level state. Choose based on what state the method needs: instance, class, or none.
