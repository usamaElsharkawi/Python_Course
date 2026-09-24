# Lecture 2: Typecasting in Python

---

## Unit 1: What Is Typecasting? — The Concept and Why It Exists

### Core Truth
**Typecasting creates a new object of a different type from an existing object.** The original object is never modified. A new variable is bound to the new type's object.

### The Problem Typecasting Solves

```python
# User input always returns a string — even if it looks like a number
age = "34"        # This is a STRING, not an integer
# age + 5         # TypeError: can't concatenate str and int

# But we need to do math with it
# Solution: typecast
age_int = int(age)  # Now age_int is an integer 34
print(age_int + 5)  # 39 ← works!
```

### The Lecture's Kitchen Analogy (Fixed)

The lecture says: *"Variables are containers that can store data in memory."*

**More accurately**: Variables are **labels** pointing to **objects**. Typecasting creates a **new object** with a different type and binds a (possibly new) label to it.

```
BEFORE typecasting:
┌──────────────────────────────────┐
│ b (label) ──▶ PyUnicodeObject("34") │  ← string object
└──────────────────────────────────┘

AFTER typecasting (c = int(b)):
┌──────────────────────────────────┐
│ b (label) ──▶ PyUnicodeObject("34") │  ← unchanged!
│ c (label) ──▶ PyLongObject(34)      │  ← NEW object, int type
└──────────────────────────────────┘
```

### The Four Typecasting Functions

| Function | Converts TO | Example | Result |
|----------|------------|---------|--------|
| `int()` | integer | `int("34")` | `34` (int) |
| `str()` | string | `str(23)` | `"23"` (str) |
| `float()` | float | `float("3.14")` | `3.14` (float) |
| `bool()` | boolean | `bool(1)` | `True` (bool) |

### The Fundamental Rule

```python
# Typecasting ALWAYS creates a NEW object
# The ORIGINAL variable is NEVER modified

b = "34"          # b is a string
c = int(b)        # c is an integer
# b is STILL "34" (string) — unchanged!
```

### Why This Matters

```python
# Without typecasting, you get errors
age_str = "34"
# age_str + 5    → TypeError

# With typecasting, you can compute
age_int = int(age_str)
result = age_int + 5    # 39 ← works
```

### The Lecture's Example Explained

```python
b = "34"          # b is string "34"
c = int(b)        # c is integer 34

print(b)          # "34" ← still a string
print(type(b))    # <class 'str'>
print(c)          # 34 ← now an integer
print(type(c))    # <class 'int'>
```

**Key insight**: `int(b)` doesn't modify `b`. It reads `b`'s value, creates a **new** integer object, and binds `c` to it.

### What Happens Under the Hood

```python
c = int(b)
# Step 1: Python reads b → finds PyUnicodeObject("34")
# Step 2: Calls int() → parses "34" → creates PyLongObject(34)
# Step 3: Binds c → PyLongObject(34)
# Step 4: b still points to PyUnicodeObject("34") — untouched
```

```
Memory after c = int(b):

HEAP:
┌──────────────────────┐     ┌──────────────────────┐
│ PyUnicodeObject("34") │     │ PyLongObject(34)     │
│ ob_refcnt: 2         │     │ ob_refcnt: 1         │
│                      │     │                      │
└──────────────────────┘     └──────────────────────┘
       ▲                            ▲
       │                            │
    b (namespace)               c (namespace)
```

### Key Takeaways

1. **Typecasting creates a NEW object** — original is never modified
2. **Four functions**: `int()`, `str()`, `float()`, `bool()`
3. **Why needed**: User input is always string; math needs numbers
4. **Original variable stays the same type** after typecasting
5. **The value is converted**, not the variable itself
6. **Typecasting reads the source object** and creates a new typed object

---

**Next: Unit 2** — The Four Typecasting Functions in Detail

---

### Unit 2: The Four Typecasting Functions — Internal Behavior, Truncation, Edge Cases

#### Core Truth
**Each typecasting function has specific rules about what it accepts and what it produces.** `int()` truncates floats, `str()` creates a textual representation, `float()` parses numeric strings, and `bool()` follows truthiness rules.

#### 1. `int()` — Convert to Integer

##### What It Accepts

```python
# From string (must be valid integer representation)
int("34")      # 34
int("-5")      # -5
int("0")       # 0

# From float (TRUNCATES toward zero)
int(3.14)      # 3 (not 4!)
int(-3.14)     # -3 (not -4!)

# From another int (no change)
int(34)        # 34 (same object, no new allocation needed)
```

##### What It Rejects

```python
# Invalid strings → ValueError
int("hello")   # ValueError: invalid literal for int() with base 10
int("3.14")    # ValueError: invalid literal for int() with base 10
int("")        # ValueError: invalid literal for int() with base 10
```

##### Internal Behavior

```python
# int() on a string: parses the string character by character
# int("34") → reads '3', '4' → computes 3*10 + 4 = 34 → PyLongObject(34)

# int() on a float: truncates (drops decimal part)
# int(3.14) → PyLongObject(3) — NOT rounded!
```

##### Truncation vs Rounding

```python
# int() ALWAYS truncates (drops decimal), never rounds
print(int(3.9))    # 3
print(int(3.1))    # 3
print(int(-3.9))   # -3 (truncates toward zero)

# For rounding, use round()
print(round(3.9))  # 4
```

##### int() on Already-Integer

```python
# If the value is already an integer, int() returns the same object
a = 34
b = int(a)
print(a is b)  # True ← same object (small int caching)
```

**Why?** CPython checks if the input is already a `PyLongObject` and returns it directly — no new object created.

#### 2. `str()` — Convert to String

##### What It Does

```python
# Converts ANY object to its string representation
str(34)        # "34"
str(3.14)      # "3.14"
str(True)      # "True"
str([1, 2, 3]) # "[1, 2, 3]"
```

##### Internal Behavior

```python
# str() calls the object's __str__() method
# For int: __str__() returns the decimal representation
# For float: __str__() returns the decimal representation
# For custom objects: __str__() returns whatever the class defines
```

```c
// Simplified CPython
PyObject* PyUnicode_FromObject(PyObject *v) {
    // Calls v->ob_type->tp_str (which is __str__)
    return v->ob_type->tp_str(v);
}
```

##### str() vs repr()

```python
# str() is for human-readable output
# repr() is for developer-readable output
str(34)    # "34"
repr(34)   # "34"

str(3.14)  # "3.14"
repr(3.14) # "3.14"
```

For most built-in types, `str()` and `repr()` produce the same result. The difference matters for custom classes.

#### 3. `float()` — Convert to Float

##### What It Accepts

```python
# From string (must be valid numeric representation)
float("3.14")    # 3.14
float("3")       # 3.0
float("-5.5")    # -5.5
float("1e3")     # 1000.0 (scientific notation)

# From integer
float(34)        # 34.0

# From another float (no change)
float(3.14)      # 3.14
```

##### What It Rejects

```python
# Invalid strings → ValueError
float("hello")   # ValueError: could not convert string to float
float("")        # ValueError
```

##### Internal Behavior

```python
# float("3.14") → parses string → creates PyFloatObject(3.14)
# float(34) → creates PyFloatObject(34.0)
```

**Key insight**: `float()` always produces a **64-bit IEEE 754 double**. Even `float(3)` becomes `3.0` — a completely different object from the integer `3`.

##### Integer vs Float — Different Objects

```python
a = 3
b = float(a)
print(a)        # 3
print(b)        # 3.0
print(a == b)   # True (same value)
print(a is b)   # False (different objects, different types)
```

```
Memory:
┌──────────────────────┐     ┌──────────────────────┐
│ PyLongObject(3)     │     │ PyFloatObject(3.0)  │
│ ob_type: int        │     │ ob_type: float      │
└──────────────────────┘     └──────────────────────┘
       ▲                            ▲
       │                            │
    a (namespace)               b (namespace)
```

#### 4. `bool()` — Convert to Boolean

##### What It Does

```python
# Converts ANY value to True or False based on truthiness
bool(1)        # True
bool(0)        # False
bool(-1)       # True
bool(0.0)      # False
bool(0.1)      # True
bool("")       # False (empty string)
bool("hello")  # True (non-empty string)
bool([])       # False (empty list)
bool([1, 2])   # True (non-empty list)
bool(None)     # False
```

##### Internal Behavior

```python
# bool() calls the object's __bool__() method
# If __bool__() doesn't exist, calls __len__()
# If __len__() returns 0 → False, otherwise → True
```

```c
// Simplified CPython
int PyObject_IsTrue(PyObject *v) {
    if (v->ob_type->tp_bool) {
        return v->ob_type->tp_bool(v);
    }
    // Fall back to __len__
    Py_ssize_t len = PyObject_Length(v);
    return len > 0 ? 1 : 0;
}
```

##### Truthiness Table

| Value | `bool()` | Why |
|-------|----------|-----|
| `0`, `0.0`, `0j` | `False` | Zero is falsy |
| `""` (empty string) | `False` | Empty sequence |
| `[]`, `()`, `{}` | `False` | Empty collections |
| `None` | `False` | Null value |
| Everything else | `True` | Non-zero, non-empty |

##### bool() on Already-Boolean

```python
bool(True)     # True (same object)
bool(False)    # False (same object)
```

#### Complete Comparison Table

| Function | Input | Output | Behavior |
|----------|-------|--------|----------|
| `int("34")` | str | int | Parses string → integer |
| `int(3.14)` | float | int | **Truncates** → 3 |
| `int(34)` | int | int | Returns same object |
| `str(34)` | int | str | Creates "34" |
| `str(3.14)` | float | str | Creates "3.14" |
| `float("3.14")` | str | float | Parses → 3.14 |
| `float(34)` | int | float | Creates 34.0 |
| `bool(1)` | int | bool | True |
| `bool(0)` | int | bool | False |
| `bool("")` | str | bool | False |
| `bool("hi")` | str | bool | True |

#### The Lecture's Example — Full Breakdown

```python
num_str = "10"      # string "10"
num_int = int(num_str)  # integer 10
num_float = float(num_str)  # float 10.0

print(num_str)      # "10" ← string
print(type(num_str)) # <class 'str'>
print(num_int)      # 10 ← integer
print(type(num_int)) # <class 'int'>
print(num_float)    # 10.0 ← float
print(type(num_float)) # <class 'float'>
```

```
Memory after all conversions:

HEAP:
┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│ PyUnicodeObject("10") │     │ PyLongObject(10)     │     │ PyFloatObject(10.0) │
│ ob_refcnt: 2         │     │ ob_refcnt: 1         │     │ ob_refcnt: 1         │
└──────────────────────┘     └──────────────────────┘     └──────────────────────┘
       ▲                            ▲                            ▲
       │                            │                            │
    num_str                    num_int                     num_float
```

#### Common Pitfalls

##### 1. int() Truncates, Doesn't Round
```python
print(int(3.9))   # 3 (not 4!)
print(int(-3.9))  # -3 (not -4!)
```

##### 2. int() on Float String Fails
```python
int("3.14")  # ValueError! Use float("3.14") then int()
int(float("3.14"))  # 3 ← works but two steps
```

##### 3. bool() of Empty Collections
```python
bool([])   # False — not 0, not None, just False
bool([0])  # True — list contains one element (0)
```

##### 4. str() on Objects Creates Representation
```python
str([1, 2, 3])  # "[1, 2, 3]" — string representation, not the list itself
```

#### Key Takeaways

1. **`int()`**: Parses strings, truncates floats, returns same int if already int
2. **`str()`**: Calls `__str__()`, creates human-readable string representation
3. **`float()`**: Parses strings, converts int to float (adds `.0`), always 64-bit
4. **`bool()`**: Follows truthiness rules — zero/empty/None → False, everything else → True
5. **`int()` truncates toward zero** — never rounds
6. **Each function creates a new object** — original unchanged
7. **`int()` on already-int returns same object** (optimization)
8. **`float(3)` ≠ `3`** — different types, different objects, same value

---

**Next: Unit 3** — Taking User Input in Python — how `input()` always returns a string, why typecasting is essential for user input, and practical patterns.
