# Lecture 5: Operators in Python

---

## Unit 1: Arithmetic Operators — `+`, `-`, `*`, `/`, `//`, `%`, `**`

### Core Truth
**Arithmetic operators perform mathematical operations on numbers.** Python supports all standard arithmetic operations plus two extras: floor division (`//`) and exponentiation (`**`).

### The Seven Arithmetic Operators

| Operator | Name | Example | Result |
|----------|------|---------|--------|
| `+` | Addition | `34 + 2` | `36` |
| `-` | Subtraction | `34 - 2` | `32` |
| `*` | Multiplication | `34 * 2` | `68` |
| `/` | Division | `34 / 2` | `17.0` (float!) |
| `//` | Floor Division | `34 // 2` | `17` (int) |
| `%` | Modulus | `34 % 2` | `0` (remainder) |
| `**` | Exponentiation | `34 ** 2` | `1156` |

### Division Always Returns Float

```python
print(34 / 2)    # 17.0 ← float, not int!
print(34 // 2)   # 17   ← int (floor division)
```

**`/` always produces a `float`.** Even when the result is a whole number.

### Floor Division — Drops the Decimal

```python
# Floor division rounds DOWN toward negative infinity
print(7 // 2)    # 3
print(-7 // 2)   # -4 (rounds toward negative infinity, not zero!)
```

```
Memory:
┌─────────────────────────────────────────────┐
│ 34 / 2 → PyFloatObject(17.0)              │
│ 34 // 2 → PyLongObject(17)              │
└─────────────────────────────────────────────┘
```

### Exponentiation — Power Operation

```python
print(2 ** 3)    # 8 (2³)
print(34 ** 2)   # 1156 (34²)
```

**`**` raises the left operand to the power of the right operand.**

### Modulus — Remainder

```python
print(10 % 3)    # 1 (10 ÷ 3 = 3 remainder 1)
print(34 % 2)    # 0 (34 is evenly divisible by 2)
```

**`%` returns the remainder after division.**

### The REPL — Python's Interactive Mode

```python
# You can type Python directly in the terminal
$ python
>>> 5 + 4
9
>>> 100 - 98
2
>>> 34 / 4
8.5
```

**REPL** = Read-Evaluate-Print-Loop. It reads your input, evaluates it, prints the result, and loops back.

### Mixed Type Operations

```python
# int + float → float
print(3 + 2.5)    # 5.5

# int * float → float
print(3 * 2.5)    # 7.5

# int / int → float
print(6 / 2)      # 3.0

# int // int → int
print(6 // 2)     # 3
```

**Rule**: Any operation involving a `float` produces a `float` (except `//` which produces `int`).

### Operator Precedence

```python
# Standard math precedence applies
print(2 + 3 * 4)    # 14 (3*4=12, then 2+12=14)
print((2 + 3) * 4)  # 20 (parentheses first)
print(2 ** 3 + 1)   # 9 (2³=8, then 8+1=9)
```

**Precedence**: `**` > `*`, `/`, `//`, `%` > `+`, `-`

### Common Pitfalls

#### 1. Division Returns Float
```python
result = 10 / 2
print(type(result))  # <class 'float'> — not int!
```

#### 2. Floor Division with Negatives
```python
print(-7 // 2)   # -4 (not -3!)
# Floor division rounds toward negative infinity
```

#### 3. Modulus with Negatives
```python
print(-7 % 2)    # 1 (sign follows divisor)
print(7 % -2)    # -1 (sign follows divisor)
```

#### 4. Exponentiation Precedence
```python
print(2 ** 3 ** 2)  # 512 (right-associative: 2**(3**2) = 2**9)
# NOT (2**3)**2 = 64
```

### Key Takeaways

1. **`+`, `-`, `*`** work as expected
2. **`/` always returns `float`** — even for whole numbers
3. **`//` returns `int`** — drops the decimal (floor division)
4. **`%` returns the remainder**
5. **`**` is exponentiation** — `a ** b` = a^b
6. **REPL** lets you run Python interactively in the terminal
7. **Mixed operations**: `int + float` → `float`
8. **Operator precedence**: `**` > `*`, `/`, `//`, `%` > `+`, `-`
9. **Parentheses override precedence**
10. **Floor division rounds toward negative infinity**, not toward zero

---

**Next: Unit 2** — Comparison Operators — `>`, `<`, `>=`, `<=`, `==`, `!=` — Always Return `True` or `False`

---

### Unit 2: Comparison Operators — `>`, `<`, `>=`, `<=`, `==`, `!=`

#### Core Truth
**Comparison operators always return `True` or `False`.** They compare two values and produce a boolean result. `==` (double equal) is comparison; `=` (single equal) is assignment — they are completely different operations.

#### The Six Comparison Operators

| Operator | Name | Example | Result |
|----------|------|---------|--------|
| `>` | Greater than | `10 > 5` | `True` |
| `<` | Less than | `10 < 5` | `False` |
| `>=` | Greater than or equal | `10 >= 10` | `True` |
| `<=` | Less than or equal | `10 <= 5` | `False` |
| `==` | Equal to | `10 == 10` | `True` |
| `!=` | Not equal to | `10 != 5` | `True` |

#### `==` vs `=` — The Most Important Distinction

```python
# = is ASSIGNMENT — gives a variable a value
a = 34      # a now holds 34

# == is COMPARISON — asks a question
a == 34     # True — is a equal to 34?
a == 4      # False — is a equal to 4?
```

```
Memory:
┌─────────────────────────────────────────────┐
│ a = 34                                      │
│   → a ──▶ PyLongObject(34)              │
│                                              │
│ a == 34                                     │
│   → asks: is a's value == 34?              │
│   → True (PyBoolObject)                     │
│   → NO variable is modified                │
└─────────────────────────────────────────────┘
```

**`=` modifies memory. `==` reads memory and produces a boolean.**

#### How Comparison Works Internally

```python
# When Python evaluates 10 > 5:
# 1. Load PyLongObject(10)
# 2. Load PyLongObject(5)
# 3. Call 10->ob_type->tp_richcompare(10, 5, Py_GT)
# 4. Returns PyBoolObject(True)
```

```c
// Simplified CPython (Objects/object.c)
PyObject* PyObject_RichCompare(PyObject *v, PyObject *w, int op) {
    // op can be Py_GT, Py_LT, Py_EQ, Py_NE, Py_GE, Py_LE
    // Calls v->ob_type->tp_richcompare(v, w, op)
    // Returns True or False
}
```

**Every comparison calls `tp_richcompare` on the object's type.**

#### All Comparisons Return `bool`

```python
print(10 > 5)     # True  → PyBoolObject(True)
print(10 < 5)     # False → PyBoolObject(False)
print(10 >= 10)   # True
print(10 <= 5)    # False
print(10 == 10)   # True
print(10 != 5)    # True
```

```
Memory:
┌─────────────────────────────────────────────┐
│ All comparisons produce PyBoolObject        │
│                                              │
│ 10 > 5  → PyBoolObject(True)              │
│ 10 < 5  → PyBoolObject(False)             │
│                                              │
│ These are SINGLETON objects (like True/False)│
└─────────────────────────────────────────────┘
```

#### Chaining Comparisons

```python
# Python supports chained comparisons!
print(1 < 2 < 3)    # True (1 < 2 AND 2 < 3)
print(1 < 3 < 2)    # False (1 < 3 is True, but 3 < 2 is False)
print(5 <= 5 <= 5)  # True
```

**Python evaluates `a < b < c` as `(a < b) and (b < c)`.**

#### String Comparisons

```python
# Strings are compared lexicographically (dictionary order)
print("apple" < "banana")   # True
print("apple" > "banana")   # False
print("apple" == "apple")   # True
```

**Strings are compared character by character using Unicode code points.**

```
"apple" vs "banana":
'a' (97) vs 'b' (98) → 'a' < 'b' → True
```

#### Comparing Different Types

```python
# Python 3 does NOT allow comparing incompatible types
# print(3 > "hello")  # TypeError: '>' not supported between int and str

# But same types work:
print(3 > 2)        # True
print("a" > "b")    # False
```

**Python 3 is strict about type comparison** — you can't compare `int` with `str`.

#### `!=` — Not Equal To

```python
print(34 != 4)     # True  (34 is not equal to 4)
print(34 != 34)    # False (34 IS equal to 34)
```

**`!=` is the negation of `==`.**

#### The Lecture's Example — Full Breakdown

```python
a = 34

# Is a greater than 4?
print(a > 4)      # True

# Is a less than 4?
print(a < 4)      # False

# Is a less than or equal to 4?
print(a <= 4)     # False

# Is a greater than or equal to 4?
print(a >= 4)     # True

# Is a equal to 34?
print(a == 34)    # True

# Is a equal to 4?
print(a == 4)     # False

# Is a not equal to 34?
print(a != 34)    # False
```

```
Memory:
┌─────────────────────────────────────────────┐
│ a ──▶ PyLongObject(34)                    │
│                                              │
│ a > 4  → tp_richcompare(34, 4, GT) → True  │
│ a < 4  → tp_richcompare(34, 4, LT) → False │
│ a == 34 → tp_richcompare(34, 34, EQ) → True│
│ a != 34 → tp_richcompare(34, 34, NE) → False│
└─────────────────────────────────────────────┘
```

#### Common Pitfalls

##### 1. Using `=` Instead of `==`
```python
# WRONG — this is assignment, not comparison
if a = 34:    # SyntaxError!

# CORRECT
if a == 34:   # This works
```

##### 2. Comparing Strings Numerically
```python
# WRONG — string comparison is lexicographic, not numeric
print("10" > "5")   # False! ('1' < '5' in Unicode)

# CORRECT
print(10 > 5)       # True
```

##### 3. Chaining with `and`
```python
# These are equivalent:
print(1 < 2 and 2 < 3)   # True
print(1 < 2 < 3)         # True
```

#### Key Takeaways

1. **Comparison operators always return `bool`** — `True` or `False`
2. **`==` is comparison, `=` is assignment** — completely different
3. **Six operators**: `>`, `<`, `>=`, `<=`, `==`, `!=`
4. **All call `tp_richcompare`** on the object's type
5. **Strings compare lexicographically** — by Unicode code points
6. **Python 3 doesn't allow cross-type comparison** — `3 > "hello"` is `TypeError`
7. **Chained comparisons work** — `1 < 2 < 3` is valid
8. **`!=` is the negation of `==`**
9. **Comparisons don't modify variables** — they only read values
10. **Results are `PyBoolObject` singletons** — `True` and `False` are reused

---

**Next: Unit 3** — Logical Operators — `and`, `or`, `not` — How They Operate on Booleans and Short-Circuit Evaluation

---

### Unit 3: Logical Operators — `and`, `or`, `not`

#### Core Truth
**Logical operators operate on boolean values (`True`/`False`).** They combine or negate boolean expressions to produce new boolean results. `and`, `or`, and `not` are the three logical operators.

#### The Three Logical Operators

| Operator | Name | Example | Result |
|----------|------|---------|--------|
| `and` | Logical AND | `True and True` | `True` |
| `or` | Logical OR | `True or False` | `True` |
| `not` | Logical NOT | `not True` | `False` |

#### `and` — Both Must Be True

```python
# and returns True ONLY when both operands are True
print(True and True)    # True
print(True and False)   # False
print(False and True)   # False
print(False and False)  # False
```

```
Truth Table for AND:
┌──────┬──────┬──────┐
│  A   │  B   │ A AND B│
├──────┼──────┼──────┤
│ True │ True │ True │
│ True │ False│ False│
│ False│ True │ False│
│ False│ False│ False│
└──────┴──────┴──────┘
```

**Rule**: `and` returns `True` only if **both** operands are `True`. Otherwise `False`.

#### `or` — At Least One Must Be True

```python
# or returns True if AT LEAST ONE operand is True
print(True or True)    # True
print(True or False)   # True
print(False or True)   # True
print(False or False)  # False
```

```
Truth Table for OR:
┌──────┬──────┬───────┐
│  A   │  B   │ A OR B │
├──────┼──────┼───────┤
│ True │ True │ True  │
│ True │ False│ True  │
│ False│ True │ True  │
│ False│ False│ False │
└──────┴──────┴───────┘
```

**Rule**: `or` returns `True` if **at least one** operand is `True`. Only returns `False` when **both** are `False`.

#### `not` — Negation

```python
# not flips the boolean value
print(not True)    # False
print(not False)   # True
```

```
Truth Table for NOT:
┌──────┬───────┐
│  A   │ NOT A │
├──────┼───────┤
│ True │ False │
│ False│ True  │
└──────┴───────┘
```

**Rule**: `not` flips `True` to `False` and `False` to `True`.

#### How Logical Operators Work Internally

```python
# When Python evaluates True and False:
# 1. Load PyBoolObject(True)
# 2. Load PyBoolObject(False)
# 3. Call tp_richcompare or binary_op with AND logic
# 4. Returns PyBoolObject(False)
```

```c
// Simplified CPython
// Logical operators work on PyObject* values
// They call PyObject_IsTrue() on each operand
// Then apply the boolean logic

int PyObject_IsTrue(PyObject *v) {
    if (v->ob_type->tp_bool) {
        return v->ob_type->tp_bool(v);
    }
    // Fall back to __len__()
    Py_ssize_t len = PyObject_Length(v);
    return len > 0 ? 1 : 0;
}
```

**Key insight**: `and`, `or`, `not` call `PyObject_IsTrue()` on their operands. This means they work on **any object**, not just booleans.

#### `and` and `or` Work on Any Object (Not Just Booleans)

```python
# Python's and/or return the LAST evaluated operand, not necessarily True/False
print(0 and 5)     # 0 (0 is falsy, returns 0)
print(5 and 0)     # 0 (5 is truthy, evaluates 0, returns 0)
print(5 and 3)     # 3 (both truthy, returns last evaluated: 3)

print(0 or 5)      # 5 (0 is falsy, returns 5)
print(5 or 0)      # 5 (5 is truthy, returns 5 immediately)
print(0 or 0)     # 0 (both falsy, returns last: 0)
```

```
Memory:
┌─────────────────────────────────────────────┐
│ 5 and 3 → PyLongObject(3)              │
│   → 5 is truthy → evaluate 3 → return 3  │
│                                              │
│ 0 or 5 → PyLongObject(5)                 │
│   → 0 is falsy → evaluate 5 → return 5   │
└─────────────────────────────────────────────┘
```

**Short-circuit evaluation**: `and` and `or` evaluate only as much as needed.

#### Short-Circuit Evaluation

```python
# and: if first operand is False, second is NEVER evaluated
# or: if first operand is True, second is NEVER evaluated

# Example:
print(False and expensive_function())  # expensive_function() is NEVER called
print(True or expensive_function())    # expensive_function() is NEVER called
```

```
Short-circuit behavior:
┌─────────────────────────────────────────────┐
│ False and X → returns False immediately    │
│   X is never evaluated                     │
│                                              │
│ True or X → returns True immediately       │
│   X is never evaluated                     │
└─────────────────────────────────────────────┘
```

**Why this matters**: It enables patterns like:
```python
# Guard clauses
if x is not None and x.value > 0:  # x.value is only accessed if x is not None
    ...
```

#### `not` with Non-Boolean Values

```python
# not uses truthiness
print(not 0)       # True (0 is falsy)
print(not 1)       # False (1 is truthy)
print(not "")      # True (empty string is falsy)
print(not "hello") # False (non-empty string is truthy)
print(not [])      # True (empty list is falsy)
print(not [1, 2])  # False (non-empty list is truthy)
```

**`not` calls `PyObject_IsTrue()` and negates the result.**

#### Truthiness Table

| Value | `bool()` | `not value` |
|-------|----------|-------------|
| `0`, `0.0`, `0j` | `False` | `True` |
| `""` (empty string) | `False` | `True` |
| `[]`, `()`, `{}` | `False` | `True` |
| `None` | `False` | `True` |
| Everything else | `True` | `False` |

#### The Lecture's Example — Full Breakdown

```python
# The lecture demonstrates:
# true and true → true
# true and false → false
# false and true → false
# false and false → false

# true or true → true
# false or true → true
# false or false → false

# not true → false
# not false → true
```

```
Memory:
┌─────────────────────────────────────────────┐
│ True and True → PyBoolObject(True)       │
│ True and False → PyBoolObject(False)     │
│ False and True → PyBoolObject(False)     │
│ False and False → PyBoolObject(False)    │
│                                              │
│ True or True → PyBoolObject(True)        │
│ False or True → PyBoolObject(True)       │
│ False or False → PyBoolObject(False)     │
│                                              │
│ not True → PyBoolObject(False)           │
│ not False → PyBoolObject(True)           │
└─────────────────────────────────────────────┘
```

#### Common Pitfalls

##### 1. Confusing `and`/`or` with `&`/`|`
```python
# Logical operators (short-circuit):
True and False   # False

# Bitwise operators (always evaluate both):
True & False     # 0 (bitwise AND)
```

##### 2. `and`/`or` Return Operands, Not Booleans
```python
# These don't return True/False!
print(5 and 3)   # 3 (not True!)
print(5 or 3)    # 5 (not True!)

# Use bool() if you need a boolean
print(bool(5 and 3))  # True
```

##### 3. Chaining `and` and `or`
```python
# Precedence: and > or
# True or False and False → True or (False and False) → True or False → True
# NOT (True or False) and False → False and False → False
```

#### Key Takeaways

1. **`and`** returns `True` only if **both** operands are `True`
2. **`or`** returns `True` if **at least one** operand is `True`
3. **`not`** flips the boolean value
4. **All call `PyObject_IsTrue()`** — they work on any object
5. **Short-circuit evaluation**: `and`/`or` stop evaluating as soon as the result is determined
6. **`and`/`or` return the last evaluated operand**, not necessarily `True`/`False`
7. **`not` always returns `bool`**
8. **Truthiness** determines what counts as `True`/`False` for non-boolean objects
9. **`and` has higher precedence than `or`**
10. **Logical operators are the foundation of conditional statements**

---

**Next: Unit 4** — Assignment Operators — `=`, `+=`, `-=`, `*=`, `/=`, `%=`, `**=`, `//=` — Modify Variables In Place

---

### Unit 4: Assignment Operators — `=`, `+=`, `-=`, `*=`, `/=`, `%=`, `**=`, `//=`

#### Core Truth
**Assignment operators modify a variable in place.** They combine an arithmetic operation with assignment in a single step. `a += 3` is shorthand for `a = a + 3`, but they are **not always identical** under the hood.

#### The Eight Assignment Operators

| Operator | Name | Equivalent To | Example | Result |
|----------|------|---------------|---------|--------|
| `=` | Assignment | — | `a = 34` | `a` → 34 |
| `+=` | Add and assign | `a = a + 3` | `a += 3` | `a` becomes 37 |
| `-=` | Subtract and assign | `a = a - 3` | `a -= 3` | `a` becomes 31 |
| `*=` | Multiply and assign | `a = a * 3` | `a *= 3` | `a` becomes 102 |
| `/=` | Divide and assign | `a = a / 3` | `a /= 3` | `a` becomes 11.33... |
| `%=` | Modulus and assign | `a = a % 3` | `a %= 3` | `a` becomes 1 |
| `**=` | Exponent and assign | `a = a ** 3` | `a **= 3` | `a` becomes 39304 |
| `//=` | Floor divide and assign | `a = a // 3` | `a //= 3` | `a` becomes 11 |

#### How `+=` Works — The Shorthand

```python
# Without +=
a = 34
a = a + 3    # Step 1: compute a + 3 → 37, Step 2: bind a to 37

# With +=
a = 34
a += 3       # Same result, but more concise
```

```
Memory:
┌─────────────────────────────────────────────┐
│ a = 34                                      │
│   → a ──▶ PyLongObject(34)              │
│                                              │
│ a += 3                                      │
│   → Load a (PyLongObject(34))              │
│   → Add 3 → PyLongObject(37)              │
│   → Rebind a → PyLongObject(37)            │
│   → Old PyLongObject(34) refcount drops    │
└─────────────────────────────────────────────┘
```

#### `+=` vs `a = a + 3` — Are They Always Identical?

```python
# For immutable types (int, str, float), they behave the same
a = 34
a += 3    # a is now 37

a = "hello"
a += " world"    # a is now "hello world"
```

**But for mutable types, they differ:**

```python
# For lists, += modifies the list IN PLACE
a = [1, 2, 3]
a += [4, 5]     # Modifies the original list
print(a)        # [1, 2, 3, 4, 5]

# vs a = a + [4, 5] creates a NEW list
b = [1, 2, 3]
b = b + [4, 5]  # Creates new list, b points to new object
```

```
Memory for a += [4, 5] (list):
┌─────────────────────────────────────────────┐
│ a ──▶ [1, 2, 3, 4, 5]                    │
│        ↑ Same object, modified in place    │
└─────────────────────────────────────────────┘

Memory for b = b + [4, 5] (list):
┌─────────────────────────────────────────────┐
│ b ──▶ [1, 2, 3, 4, 5]                    │
│        ↑ NEW object                        │
│ Old [1, 2, 3] still exists if referenced   │
└─────────────────────────────────────────────┘
```

#### All Assignment Operators in Action

```python
a = 34

a += 3     # a = 37
a -= 5     # a = 32
a *= 2     # a = 64
a /= 4     # a = 16.0 (float!)
a //= 3    # a = 5 (int)
a %= 3     # a = 2
a **= 2    # a = 4
```

```
Step-by-step memory:
┌─────────────────────────────────────────────┐
│ a = 34 → PyLongObject(34)                │
│ a += 3 → PyLongObject(37)              │
│ a -= 5 → PyLongObject(32)              │
│ a *= 2 → PyLongObject(64)              │
│ a /= 4 → PyFloatObject(16.0)           │
│ a //= 3 → PyLongObject(5)              │
│ a %= 3 → PyLongObject(2)               │
│ a **= 2 → PyLongObject(4)              │
└─────────────────────────────────────────────┘
```

#### Division Always Produces Float

```python
a = 34
a /= 2     # a = 17.0 (float, not int!)
```

**`/=` always produces a `float`.** Even when the result is a whole number.

#### `**=` — Exponentiation Assignment

```python
a = 2
a **= 3    # a = 8 (2³)
```

**`a **= b` is equivalent to `a = a ** b`.**

#### Under the Hood — How Python Processes `+=`

```python
# When Python sees a += 3:
# 1. Load variable a → PyObject*
# 2. Call a->ob_type->nb_inplace_add(a, 3)
# 3. If nb_inplace_add exists, use it (in-place modification)
# 4. If not, fall back to a = a + 3 (create new object)
```

```c
// Simplified CPython
PyObject* PyNumber_InPlaceAdd(PyObject *v, PyObject *w) {
    // Try in-place addition first
    if (v->ob_type->tp_as_number && v->ob_type->tp_as_number->nb_inplace_add) {
        return v->ob_type->tp_as_number->nb_inplace_add(v, w);
    }
    // Fall back to regular addition
    return PyNumber_Add(v, w);
}
```

**For immutable types**: `nb_inplace_add` doesn't exist → falls back to `a = a + 3` → new object.
**For mutable types**: `nb_inplace_add` exists → modifies the object in place.

#### Common Pitfalls

##### 1. `/=` Always Returns Float
```python
a = 10
a /= 2     # a = 5.0 (float, not int!)
```

##### 2. `//=` Returns Int
```python
a = 10
a //= 3    # a = 3 (int)
```

##### 3. Chaining Assignment Operators
```python
# These are equivalent:
a = 34
a += 3     # a = 37

# NOT the same as:
a = 34 + 3  # a = 37 (different approach)
```

#### Key Takeaways

1. **`=`** is basic assignment — binds a name to an object
2. **`+=`, `-=`, `*=`, `/=`** combine arithmetic with assignment
3. **`a += b` is shorthand for `a = a + b`**
4. **`/=` always produces `float`** — even for whole numbers
5. **`//=` produces `int`** — drops the decimal
6. **`**=` is exponentiation assignment** — `a **= b` = a^b
7. **For immutable types**: `+=` creates a new object
8. **For mutable types**: `+=` modifies the object in place
9. **`nb_inplace_add`** determines whether modification is in-place
10. **Assignment operators are concise** but behave identically to expanded form for scalars

---

**Lecture 5 complete!** All 4 units documented. Ready for **Lecture 6: Coding Exercise 2** whenever you are!
