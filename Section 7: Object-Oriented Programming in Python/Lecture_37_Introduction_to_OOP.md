# Lecture 37 — Introduction to OOP

**Units covered**: 1. What OOP is & why it exists,
2. The `class` statement internals,
3. Objects & instance creation

---

## Unit 1 — What OOP Is & Why It Exists

### Core Concept
OOP is a way of programming that focuses on creating **objects**. An object is a self-contained unit that bundles together **data** (state) and **actions** (behavior). A **class** is the blueprint/template; an **object** is an instance created from it.

Example from the lecture: a train-booking form is a class (template with name, age, train number, boarding station, etc.). Each filled form is an object.

### Four Pillars of OOP

| Pillar | Meaning | Real-world analogy |
|---|---|---|
| **Abstraction** | Hide implementation details; expose a simple interface | Driving a car using steering/pedals without knowing engine internals |
| **Encapsulation** | Bundle data + methods together; protect data from outside misuse | Car engine parts inside a protective casing |
| **Inheritance** | Extend an existing class; reuse its features | `Programmer` inherits from `Employee` |
| **Polymorphism** | Same method name, different behavior per object | `Dog.makesound()` → "bow", `Cat.makesound()` → "meow" |

### What's Actually Happening
In Python, **everything is an object**, including classes themselves. A class is an instance of `type`.

### Why It Matters
- **Organization** — related data and behavior live together; large programs stay navigable
- **Reusability** — define once, instantiate many times; avoids repeated procedural code
- **Debuggability** — structure mirrors the problem domain, so bugs map to real-world concepts
- **Modeling** — maps directly to domain entities (train form → class, filled form → object)

### Minimal Executable Example
```python
class TrainForm:
    def __init__(self, name, age, train_number):
        self.name = name
        self.age = age
        self.train_number = train_number

    def summary(self):
        return f"{self.name}, age {self.age}, train {self.train_number}"

passenger1 = TrainForm("Alice", 30, "T101")
passenger2 = TrainForm("Bob", 25, "T202")

print(passenger1.summary())
print(passenger2.summary())
print(type(TrainForm))        # <class 'type'> — classes are objects too
print(passenger1.__dict__)    # {'name': 'Alice', 'age': 30, 'train_number': 'T101'}
```

---

## Unit 2 — The `class` Statement Internals

### Core Concept
The `class` statement is **executable code**, not just a declaration. Python executes the class body, collects everything defined inside into a namespace, then hands that namespace to `type` to build a class object.

### What's Actually Happening

**1. The `class` statement executes the body at runtime**
```python
class Car:
    wheels = 4
    def drive(self):
        print("vroom")
```
Python:
1. Creates a fresh namespace dict for the class body
2. Executes every statement in that body — assignments, `def`s, nested classes
3. `wheels = 4` stores `4` under key `"wheels"` in the class namespace
4. `def drive(self):` creates a function object, stored under `"drive"`
5. Calls `type("Car", (), namespace)` to build the class object

**2. `type` is the metaclass — the class of classes**
```python
print(type(Car))   # <class 'type'>
```
Just as `int()` instances are made by `int`, class objects are made by `type`. `type(name, bases, dict)` is the constructor:
- `name` — `"Car"`
- `bases` — tuple of parent classes (`()` here)
- `dict` — the captured namespace (becomes `Car.__dict__`)

**3. Class object structure (simplified `PyTypeObject`)**
```
[refcnt][type pointer][ob_size]          ← PyObject header
[tp_name = "Car"]                        ← class name
[tp_basicsize]                           ← instance size
[tp_dict]    → {'wheels': 4, 'drive': <function>, ...}
[tp_bases]   → ()                         ← parent classes
[tp_mro]     → (Car, object)             ← method resolution order
```

**4. Methods are plain functions until accessed**
`drive` stored in `Car.__dict__` is a function object. It becomes a bound method only when accessed via an instance (`car.drive`) — via the descriptor protocol (`__get__`).

### Why It Matters
- Classes are **first-class objects** — pass them around, store in lists, introspect at runtime
- `__dict__` is the source of truth for class-level attributes — runtime changes affect all instances
- `type(name, bases, dict)` demystifies metaclasses: any callable with that signature can be one
- This is the foundation for inheritance: `tp_bases` and `tp_mro` drive method lookup up the chain

### Minimal Executable Example
```python
class Car:
    wheels = 4
    def drive(self):
        return "vroom"

print(type(Car))                      # <class 'type'>
print(Car.__name__)                   # 'Car'
print(Car.__bases__)                  # (<class 'object'>,)
print(Car.__mro__)                    # (<class 'Car'>, <class 'object'>)
print('wheels' in Car.__dict__)       # True
print('drive' in Car.__dict__)        # True
print(Car.__dict__['wheels'])         # 4

# Build a class manually with type() — same result as `class` statement
ManualCar = type('ManualCar', (), {'wheels': 4, 'drive': lambda self: 'vroom'})
print(ManualCar.wheels)               # 4
print(type(ManualCar))                # <class 'type'>
```

---

## Unit 3 — Objects & Instance Creation

### Core Concept
Calling `Car()` triggers a two-phase protocol: `__new__` allocates and returns a new instance, then `__init__` initializes that instance's state. Each object carries its own `__dict__` for instance attributes; methods live on the class and are resolved at access time through the instance → class → MRO lookup chain.

### What's Actually Happening

**1. `ClassName()` invokes `type.__call__`**
```python
my_car = Car()
```
`type.__call__(Car)` runs:
1. Calls `Car.__new__(Car)` to **create** the object
2. Calls `Car.__init__(my_car, ...)` to **initialize** it
3. Returns the initialized instance

`object.__new__` (the default) allocates memory via `PyObject_Malloc`, zeroes the header, sets the type pointer to `Car`, and returns the raw instance.

**2. `__new__` vs `__init__`**
| | `__new__` | `__init__` |
|---|---|---|
| Purpose | Create & return the instance | Initialize the instance |
| First arg | The class (`cls`) | The instance (`self`) |
| Returns | Must return an instance | Returns `None` implicitly |
| Called | Once per instantiation | Once per instantiation |

If `__new__` doesn't return an instance of `cls`, `__init__` is **not** called.

**3. Instance `__dict__` — per-object state**
```python
my_car.color = "red"
```
Stores `{"color": "red"}` in `my_car.__dict__`. Each instance has its own dict; class attributes live in `Car.__dict__`. Two `Car` objects can have different colors while sharing the same `drive` method.

**4. Attribute lookup order (simplified)**
For `my_car.some_attr`:
1. `my_car.__dict__` (instance attributes)
2. `Car.__dict__` then base classes' `__dict__` following `Car.__mro` (methods, class attributes)
3. Data descriptors (e.g., properties) take priority over instance `__dict__`
4. Non-data descriptors (plain functions) are shadowed by instance `__dict__`

A plain function in `Car.__dict__` becomes a bound method when accessed via an instance — the function's `__get__(instance, owner)` returns a method object binding `self`.

**5. `self` is convention, not a keyword**
`self` is just the first parameter name. Python passes the instance automatically as the first argument when you access a method through an instance. `my_car.drive()` → `Car.drive(my_car)`.

### Why It Matters
- `__new__` controls *what kind* of object is created (immutables like `int`, `str`, singletons); `__init__` controls *how* it's initialized
- Instance `__dict__` explains why instance attributes shadow class attributes and don't affect other instances
- Attribute lookup order powers inheritance and `super()` (next lecture)
- Knowing `self` is explicit clarifies bound methods, `@staticmethod`, `@classmethod`

### Minimal Executable Example
```python
class Car:
    wheels = 4  # class attribute

    def __new__(cls, *args, **kwargs):
        print("__new__ called")
        return super().__new__(cls)

    def __init__(self, color):
        print("__init__ called")
        self.color = color  # instance attribute

    def drive(self):
        return f"{self.color} car driving"

car1 = Car("red")
car2 = Car("blue")

print(car1.color, car2.color)     # red blue — separate instance dicts
print(car1.wheels, car2.wheels)   # 4 4 — shared class attribute
print(car1.__dict__)              # {'color': 'red'}
print(car2.__dict__)              # {'color': 'blue'}
print(Car.__dict__['wheels'])     # 4 — lives on class
print(car1.drive)                 # <bound method Car.drive of <Car object>>
print(car1.drive())               # red car driving
print(car1.drive is car2.drive)   # False — new bound method each access
```

---

## Key Insight
A class is a first-class object (instance of `type`) built by executing its body and passing the namespace to `type(name, bases, dict)`. An instance is created via `type.__call__` → `__new__` (allocate) + `__init__` (initialize), carrying its own `__dict__` while sharing class-level methods through the MRO lookup chain.
