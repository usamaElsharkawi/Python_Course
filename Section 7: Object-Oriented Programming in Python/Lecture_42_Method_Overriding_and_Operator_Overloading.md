# Lecture 42 — Method Overriding and Operator Overloading

**Units covered**: 1. What operator overloading is & why `+` fails by default,
2. The `__add__` dunder method — overloading `+`,
3. Other operator dunder methods (`__sub__`, `__mul__`, `__truediv__`)

---

## Unit 1 — What Operator Overloading Is & Why `+` Fails by Default

### Core Concept
Operator overloading lets you define what Python's built-in operators (`+`, `-`, `*`, `/`, etc.) do when applied to objects of your own class. By default, Python doesn't know how to add two `Point` objects — it raises `TypeError: unsupported operand types for +`.

### What's Actually Happening
```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p1 = Point(3, 2)
p2 = Point(6, 3)

p = p1 + p2   # TypeError: unsupported operand types for +: 'Point' and 'Point'
```

Python evaluates `p1 + p2` by calling `p1.__add__(p2)`. The base `object` type doesn't define `__add__`, so Python doesn't know how to combine two `Point` instances — hence the error.

### Why It Matters
- Without operator overloading, you're stuck with named methods like `p1.sum(p2)`.
- Overloading lets your custom objects behave like built-in types, making code more readable and natural (`p1 + p2` instead of `p1.sum(p2)`).
- This is a form of polymorphism — the same `+` operator works differently depending on the operand types.

### Minimal Executable Example
```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p1 = Point(3, 2)
p2 = Point(6, 3)

try:
    p = p1 + p2
except TypeError as err:
    print("TypeError:", err)   # unsupported operand types for +
```

---

## Unit 2 — The `__add__` Dunder Method — Overloading `+`

### Core Concept
Define `__add__(self, other)` in your class to tell Python how `+` works between two instances. It should return a new `Point` whose `x` and `y` are the sums of the operands' components.

### What's Actually Happening
```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def print_point(self):
        print(f"x is {self.x} and y is {self.y}")
```

- `p1 + p2` → `p1.__add__(p2)` → `Point(3+6, 2+3)` → `Point(9, 5)`.
- The original objects `p1` and `p2` are unchanged; `__add__` returns a **new** `Point` (immutable-style behavior).
- `self.x + other.x` — `self` is the left operand (`p1`), `other` is the right operand (`p2`).

### Why It Matters
- `p = p1 + p2` now works and produces `Point(9, 5)`.
- `__add__` is the canonical example of operator overloading — it maps syntax (`+`) to a method call.
- Returning a new instance (rather than mutating `self`) is the expected convention for `+`.

### Minimal Executable Example
```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def print_point(self):
        print(f"x is {self.x} and y is {self.y}")

p1 = Point(3, 2)
p2 = Point(6, 3)

p = p1 + p2          # Point(9, 5)
p.print_point()      # x is 9 and y is 5
```

---

## Unit 3 — Other Operator Dunder Methods (`__sub__`, `__mul__`, `__truediv__`)

### Core Concept
Python provides dunder methods for most operators. You overload them the same way as `__add__`:

| Operator | Dunder method |
|---|---|
| `+` | `__add__` |
| `-` | `__sub__` |
| `*` | `__mul__` |
| `/` | `__truediv__` |

### What's Actually Happening
```python
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
```

- `p1 - p2` → `p1.__sub__(p2)` → `Point(-3, -1)`
- `p1 * p2` → `p1.__mul__(p2)` → `Point(18, 6)`
- `p1 / p2` → `p1.__truediv__(p2)` → `Point(0.5, 0.66...)`

Each returns a new `Point` instance — consistent with the `__add__` convention.

### Why It Matters
- One pattern covers all arithmetic operators — define the dunder, get the syntax.
- Makes your custom types feel like first-class citizens in Python.
- Note: these are the same dunder methods Python uses internally for built-in types (`int.__add__`, `list.__add__`, etc.).

### Minimal Executable Example
```python
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

p1 = Point(6, 4)
p2 = Point(2, 2)

(p1 + p2).print_point()   # x is 8 and y is 6
(p1 - p2).print_point()   # x is 4 and y is 2
(p1 * p2).print_point()   # x is 12 and y is 8
(p1 / p2).print_point()   # x is 3.0 and y is 2.0
```

---

## Key Insight
Operator overloading maps Python syntax (`+`, `-`, `*`, `/`) to dunder methods (`__add__`, `__sub__`, `__mul__`, `__truediv__`) on your class. Define the dunder to return a new instance, and your custom objects behave like built-in types. The same `+` operator works differently depending on operand types — that's polymorphism in action.
