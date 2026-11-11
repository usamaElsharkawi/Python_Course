# Lecture 45 — Getters and Setters

**Units covered**: 1. Direct attribute access (no getters/setters yet),
2. Getter functions (computed attributes),
3. Setter functions (updating computed attributes),
4. `@property` and `@name.setter` decorators (clean syntax),
5. Encapsulation recap

---

## Unit 1 — Direct Attribute Access

### Core Concept
You can always read and write instance attributes directly: `e.projects = 6` then `print(e.projects)` → `6`. This works fine for simple data that needs no computation or validation.

### What's Actually Happening
```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

e = Employee("Jack Doe", 34555)
e.projects = 6          # creates instance attribute 'projects'
print(e.projects)       # 6 — read directly from e.__dict__
```

`e.projects = 6` writes `{"projects": 6}` into `e.__dict__`. Reading `e.projects` looks it up there. No functions involved — just plain attribute access.

### Why It Matters
- Simple, direct, Pythonic for plain data
- But it breaks when you need computed values (e.g., "first name" from "Jack Doe") or validation on write

### Minimal Executable Example
```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

e = Employee("Jack Doe", 34555)
e.projects = 6
print(e.projects)   # 6
```

---

## Unit 2 — Getter Functions

### Core Concept
Sometimes an attribute isn't stored directly — it's **computed** from other attributes. A getter function computes and returns it. Example: `first_name` computed from `self.name` by splitting on space.

### What's Actually Happening
```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def first_name(self):
        l = self.name.split(" ")   # ["Jack", "Doe"]
        return l[0]                # "Jack"
```

- `self.name.split(" ")` → `["Jack", "Doe"]`
- `l[0]` → `"Jack"` (first name)
- `l[1]` → `"Doe"` (last name)

Calling `e.first_name()` runs the computation each time — no separate `first_name` attribute is stored.

### Why It Matters
- Derived/computed attributes without storing redundant data
- `name.split(" ")` returns a list; index 0 is first name, index 1 is last name

### Minimal Executable Example
```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def first_name(self):
        l = self.name.split(" ")
        return l[0]

e = Employee("Jack Doe", 34555)
print(e.first_name())   # Jack
```

---

## Unit 3 — Setter Functions

### Core Concept
A setter function updates a computed attribute by reconstructing the source attribute. Example: `set_first_name("John")` splits `self.name`, keeps the last name, and rebuilds `"John Doe"`.

### What's Actually Happening
```python
    def set_first_name(self, new_first_name):
        l = self.name.split(" ")           # ["Jack", "Doe"]
        new_name = f"{new_first_name} {l[1]}"   # "John Doe"
        self.name = new_name               # update stored attribute
```

- `l[1]` is the original last name ("Doe")
- `f"{new_first_name} {l[1]}"` builds the new full name
- `self.name = new_name` writes it back — the stored attribute changes

### Why It Matters
- Lets you "set" a computed value while keeping the single source of truth (`self.name`)
- The caller doesn't need to know the internal structure (name = "First Last")

### Minimal Executable Example
```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def first_name(self):
        return self.name.split(" ")[0]

    def set_first_name(self, new_first_name):
        l = self.name.split(" ")
        self.name = f"{new_first_name} {l[1]}"

e = Employee("Jack Doe", 34555)
print(e.first_name())           # Jack
e.set_first_name("John")
print(e.name)                   # John Doe
```

---

## Unit 4 — `@property` and `@name.setter` Decorators

### Core Concept
The `@property` decorator lets you call a getter **without parentheses** — `e.first_name` instead of `e.first_name()`. The `@first_name.setter` decorator lets you assign **with `=`** — `e.first_name = "John"` instead of `e.set_first_name("John")`. Both functions must have the **same name** (`first_name`).

### What's Actually Happening
```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    @property
    def first_name(self):
        return self.name.split(" ")[0]

    @first_name.setter
    def first_name(self, new_first_name):
        l = self.name.split(" ")
        self.name = f"{new_first_name} {l[1]}"
```

- `@property` on the getter → `e.first_name` invokes the function, returns computed value
- `@first_name.setter` on the setter → `e.first_name = "John"` invokes the function with `"John"` as argument
- Same function name `first_name` for both — required by Python

### Usage
```python
e = Employee("Jack Doe", 34555)
print(e.first_name)        # Jack — no parentheses!
e.first_name = "John"      # calls setter with "John"
print(e.name)              # John Doe
```

### Why It Matters
- Cleaner syntax: attribute-like access for computed values
- Callers treat it like a plain attribute; don't need to know it's computed
- Encapsulation: internal logic (splitting/rejoining name) hidden behind a property interface

### Minimal Executable Example
```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    @property
    def first_name(self):
        return self.name.split(" ")[0]

    @first_name.setter
    def first_name(self, new_first_name):
        l = self.name.split(" ")
        self.name = f"{new_first_name} {l[1]}"

e = Employee("Jack Doe", 34555)
print(e.first_name)        # Jack
e.first_name = "John"
print(e.name)              # John Doe
```

---

## Unit 5 — Encapsulation Recap

### Core Concept
Getters and setters (via `@property`) are **encapsulation**: the internal representation (`self.name = "First Last"`) is hidden behind a clean property interface (`e.first_name`). The caller interacts with `first_name` as if it were a real attribute, but it's actually a function running logic.

### Key points from the lecture
- Before `@property`: `e.name` and `e.salary` existed; `first_name` did not
- After `@property`: `first_name` appears as a property on the object
- `@property` = getter (read); `@first_name.setter` = setter (write)
- Function names must match between getter and setter
- Common in real code for computed/validated attributes without exposing internals

### Minimal Executable Example (full flow)
```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    @property
    def first_name(self):
        return self.name.split(" ")[0]

    @first_name.setter
    def first_name(self, new_first_name):
        l = self.name.split(" ")
        self.name = f"{new_first_name} {l[1]}"

e = Employee("Jack Doe", 34555)
print(e.first_name)        # Jack
e.first_name = "John"
print(e.name)              # John Doe
print(e.salary)            # 34555
```

---

## Key Insight
`@property` turns a method into a read-only attribute; `@name.setter` turns a same-named method into the write side. Together they give attribute-like syntax (`e.first_name`, `e.first_name = "John"`) while hiding the computed logic behind the scenes — encapsulation without exposing internals.
