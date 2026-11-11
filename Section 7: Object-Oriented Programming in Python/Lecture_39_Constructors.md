# Lecture 39 — Constructors in Python

**Units covered**: 1. What a constructor is & `__init__`,
2. `self` binding parameters to instance attributes,
3. Methods operating on instance state & instance independence

---

## Unit 1 — What a Constructor Is & `__init__`

### Core Concept
A constructor initializes an object **after** it's created. In Python, that's the `__init__` method. It runs automatically every time you call `Employee(...)`, letting you set the object's initial state with parameters passed in.

### What's Actually Happening

Recall from Lecture 37 Unit 3: `Employee()` → `type.__call__` runs two phases:
1. `__new__` — allocates the raw instance
2. `__init__` — initializes it (this is the constructor)

```python
class Employee:
    def __init__(self, salary, name, bond):
        pass  # body runs after instance exists
```

`__init__` receives:
- `self` — the brand-new instance (just allocated by `__new__`)
- `salary, name, bond` — the arguments you passed to `Employee(...)`

The constructor **returns nothing** (implicitly `None`). Its job is solely to mutate `self` — set up instance attributes so the object is ready to use.

### Why It Matters
Without a constructor, you'd create an empty object then manually assign attributes afterward — error-prone and easy to forget. `__init__` guarantees every `Employee` starts with salary, name, and bond defined.

### Minimal Executable Example
```python
class Employee:
    def __init__(self, salary, name, bond):
        pass

e = Employee(34000, "John Doe", 4)
print(e)           # <__main__.Employee object at 0x...> — object exists even with pass
print(hasattr(e, 'salary'))  # False — nothing set yet
```

---

## Unit 2 — `self` Binding Parameters to Instance Attributes

### Core Concept
Inside `__init__`, `self.salary = salary` means: "on this specific object (`self`), create an instance attribute called `salary` and assign it the value of the parameter `salary`." This stores the data in `self.__dict__`.

### What's Actually Happening

**1. Instance attribute creation**
```python
self.salary = salary   # writes {'salary': 34000} into self.__dict__
self.name = name       # writes {'name': 'John Doe'} into self.__dict__
self.bond = bond       # writes {'bond': 4} into self.__dict__
```
The local parameters (`salary`, `name`, `bond`) exist only during the `__init__` call. `self.salary = salary` copies the value into the instance's permanent storage.

**2. The parameter and attribute can share names**
`self.salary = salary` — left side is the attribute (`self.salary`), right side is the parameter (`salary`). Python distinguishes them because `self.` prefixes the attribute.

**3. Each instance gets its own copy**
`e1 = Employee(34000, "John Doe", 4)` stores 34000 in `e1.__dict__`. A second `e2 = Employee(50000, "Jane", 2)` stores 50000 in `e2.__dict__`. They don't interfere.

### Why It Matters
This is how objects hold state. Without `self.attribute = value`, the constructor parameters would vanish when `__init__` ends, and the object would remember nothing.

### Minimal Executable Example
```python
class Employee:
    def __init__(self, salary, name, bond):
        self.salary = salary
        self.name = name
        self.bond = bond

e = Employee(34000, "John Doe", 4)
print(e.__dict__)        # {'salary': 34000, 'name': 'John Doe', 'bond': 4}
print(e.salary, e.name, e.bond)  # 34000 John Doe 4
```

---

## Unit 3 — Methods Operating on Instance State & Instance Independence

### Core Concept
Once `__init__` has populated `self.__dict__`, other methods can read that state via `self`. `self` always refers to *the object the method is called on*, so `e1.get_salary()` returns e1's salary and `e2.get_salary()` returns e2's.

### What's Actually Happening

**1. Method reads instance state**
```python
def get_salary(self):
    return self.salary
```
`self.salary` looks up `salary` in `self.__dict__`. Since `__init__` put it there, it returns the stored value.

**2. `get_info` uses f-string with self**
```python
def get_info(self):
    print(f"The name of the employee is {self.name}")
    print(f"Salary is {self.salary}")
    print(f"The bond is for {self.bond} years")
```
Each `self.*` reads from the calling object's `__dict__`, so the output reflects that specific employee.

**3. Instance independence**
```python
e1 = Employee(34000, "John Doe", 4)
e2 = Employee(50000, "Jane Smith", 2)
e1.get_info()   # John Doe / 34000 / 4 years
e2.get_info()   # Jane Smith / 50000 / 2 years
```
Same class, same methods, completely different data — because each `self.__dict__` is separate.

### Why It Matters
- Methods + instance state = encapsulation (data and behavior bundled together)
- `self` is the thread connecting a method to the exact object it should operate on
- This is the pattern you'll extend in inheritance (Lecture 41) where child constructors call parent constructors via `super().__init__()`

### Minimal Executable Example
```python
class Employee:
    def __init__(self, salary, name, bond):
        self.salary = salary
        self.name = name
        self.bond = bond

    def get_salary(self):
        return self.salary

    def get_info(self):
        print(f"The name of the employee is {self.name}")
        print(f"Salary is {self.salary}")
        print(f"The bond is for {self.bond} years")

e1 = Employee(34000, "John Doe", 4)
e2 = Employee(50000, "Jane Smith", 2)

print(e1.get_salary())   # 34000
print(e2.get_salary())   # 50000
e1.get_info()            # John Doe / 34000 / 4 years
e2.get_info()            # Jane Smith / 50000 / 2 years
print(e1.__dict__)       # {'salary': 34000, 'name': 'John Doe', 'bond': 4}
print(e2.__dict__)       # {'salary': 50000, 'name': 'Jane Smith', 'bond': 2}
```

---

## Key Insight
`__init__` runs automatically after `__new__` allocates the instance. Its job is to bind constructor parameters to `self` (`self.attr = value`), writing them into `self.__dict__`. Later methods read that state through `self`, giving each instance independent data while sharing the same class methods.
