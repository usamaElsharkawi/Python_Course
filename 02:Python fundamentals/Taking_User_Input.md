# Lecture 3: Taking User Input in Python

---

## Unit 1: The `input()` Function — Always Returns a String

### Core Truth
**`input()` ALWAYS returns a string.** No matter what the user types — a number, a name, anything — Python receives it as a `PyUnicodeObject`. This is the single most important fact about `input()`.

### How `input()` Works

```python
a = input("Enter a number: ")
# Step 1: Program pauses, displays prompt
# Step 2: User types "34" and presses Enter
# Step 3: Python creates PyUnicodeObject("34")
# Step 4: Variable a is bound to that string object
```

```
Memory after a = input():

┌─────────────────────────────────────────────┐
│ a (label) ──▶ PyUnicodeObject("34")        │  ← STRING, not int!
└─────────────────────────────────────────────┘
```

### The Prompt

```python
# With prompt (recommended)
a = input("Enter a number: ")
# Output on screen: Enter a number:

# Without prompt (bad practice)
a = input()
# Output on screen: (nothing — user doesn't know what to do)
```

**The prompt is an optional string parameter** passed to `input()`. It tells the user what to enter.

### The Lecture's Key Demonstration

```python
a = input("Enter a number: ")  # User types: 34
print(a)                        # "34" ← looks like a number, but it's a STRING
print(type(a))                  # <class 'str'>
```

**Even if the user types `34`, `type(a)` returns `<class 'str'>`.**

### Why Does `input()` Always Return a String?

```python
# The keyboard only sends characters
# '3', '4' — two characters, not the number thirty-four
# Python has no way to know if you meant:
#   - The number 34
#   - The phone number "34"
#   - The code "34"
# So it defaults to string — the safest choice
```

### The Problem This Creates

```python
a = input("Enter a number: ")  # User enters: 34
# a is "34" (string)

# This FAILS:
# a + 3    → TypeError: can only concatenate str (not int) to str

# This also FAILS:
# a * 2    → "3434" (string repetition, not math!)
```

### The Lecture's Example — Full Breakdown

```python
a = input("Enter first number: ")  # User enters: 34
# a = PyUnicodeObject("34")

# a + 3 → ERROR!
# Python sees: PyUnicodeObject("34") + PyLongObject(3)
# → TypeError: can only concatenate str (not int) to str
```

```
Memory:
┌─────────────────────────────────────────────┐
│ a (label) ──▶ PyUnicodeObject("34")        │  ← STRING
│                              │
│                              │  ERROR: can't add int to str
│                              ▼
│                         PyLongObject(3)     │  ← int
└─────────────────────────────────────────────┘
```

### The Fix — Typecasting

```python
a = input("Enter a number: ")  # User enters: 34
a = int(a)                     # Now a is integer 34
print(a + 3)                   # 37 ← works!
```

```
Memory after fix:

HEAP:
┌─────────────────────────────────────────────┐
│ PyUnicodeObject("34")  ← old, refcount drops │
│ PyLongObject(34)       ← new, a points here  │
└─────────────────────────────────────────────┘
       ▲
       │
    a (namespace)
```

### Adding Two Numbers

```python
# WITHOUT typecasting — FAILS
a = input("Enter first number: ")  # "3"
b = input("Enter second number: ") # "4"
# print(a + b) → TypeError!

# WITH typecasting — WORKS
a = input("Enter first number: ")  # "3"
b = input("Enter second number: ") # "4"
a = int(a)
b = int(b)
print(a + b)  # 7 ← correct!
```

### The Shortcut — `int(input())`

```python
# Instead of two lines, combine them:
a = int(input("Enter first number: "))
b = int(input("Enter second number: "))
print(a + b)  # 7
```

```
Memory:
┌─────────────────────────────────────────────┐
│ a (label) ──▶ PyLongObject(3)              │  ← directly int
│ b (label) ──▶ PyLongObject(4)              │  ← directly int
└─────────────────────────────────────────────┘
```

**The shortcut**: `int(input())` reads the string and immediately converts it to an integer in one step. No intermediate string variable.

### Common Patterns

| Pattern | What It Does | Example |
|---------|-------------|---------|
| `input()` | Get string from user | `name = input("Name: ")` |
| `int(input())` | Get integer from user | `age = int(input("Age: "))` |
| `float(input())` | Get float from user | `gpa = float(input("GPA: "))` |
| `str(input())` | Explicitly get string (redundant) | `x = str(input("X: "))` |

### Key Takeaways

1. **`input()` always returns a string** — no exceptions
2. **The prompt is optional but recommended** — tells the user what to enter
3. **Even numeric input is a string** — `input("34")` → `"34"` (str)
4. **You cannot do math with `input()` directly** — need typecasting
5. **The keyboard sends characters, not numbers** — Python defaults to string for safety
6. **`a + 3` fails** when `a` is from `input()` — `TypeError`
7. **Fix**: `a = int(input())` — combine input and typecasting in one line
8. **Adding two numbers**: `int(input()) + int(input())` — the standard pattern

---

**Next: Unit 2** — The String Problem — Why Typecasting Is Essential, `int(input())` Pattern, and the `+` Operator with Strings vs Integers

---

### Unit 2: The String Problem — Why Typecasting Is Essential, `int(input())` Pattern, and the `+` Operator

#### Core Truth
**The `+` operator behaves completely differently depending on the types of its operands.** With strings, `+` means **concatenation**. With integers, `+` means **addition**. `input()` always returns a string, so `+` always concatenates unless you typecast first.

#### The `+` Operator — Two Completely Different Operations

```python
# With integers → addition
print(3 + 4)    # 7

# With strings → concatenation
print("3" + "4")  # "34" ← NOT 7!
```

```
Integer addition:
┌──────────────┐     ┌──────────────┐
│ PyLongObject(3)│ + │ PyLongObject(4)│
│ tp_add: add  │   │ tp_add: add  │
└──────────────┘     └──────────────┘
         │
         ▼
    PyLongObject(7)

String concatenation:
┌──────────────┐     ┌──────────────┐
│ PyUnicodeObject("3")│ + │ PyUnicodeObject("4")│
│ tp_add: concat│   │ tp_add: concat│
└──────────────┘     └──────────────┘
         │
         ▼
    PyUnicodeObject("34")
```

**Same operator, completely different behavior** — determined by `ob_type->tp_add`.

#### The Lecture's Problem — `a + 3` with `input()`

```python
a = input("Enter a number: ")  # User enters: 34
# a = PyUnicodeObject("34")

# This FAILS:
# a + 3 → TypeError
# Python sees: PyUnicodeObject("34") + PyLongObject(3)
# → "can only concatenate str (not int) to str"
```

**Why the error?** Python checks `a`'s type first:
1. `a` is `PyUnicodeObject` → `tp_add` is string concatenation
2. String concatenation expects another string
3. `3` is `PyLongObject` → not a string → **TypeError**

```
Error explanation:
┌──────────────────────────────────────────────┐
│ TypeError: can only concatenate str          │
│            (not "int") to str                │
│                                              │
│ a → PyUnicodeObject("34")                    │
│ 3  → PyLongObject(3)                         │
│                                              │
│ String concat can't accept int operand       │
└──────────────────────────────────────────────┘
```

#### The Fix — `int(input())` Pattern

```python
a = int(input("Enter a number: "))  # User enters: 34
# Step 1: input() → PyUnicodeObject("34")
# Step 2: int() → PyLongObject(34)
# Step 3: a → PyLongObject(34)

print(a + 3)  # 37 ← works!
```

```
Memory after fix:

HEAP:
┌─────────────────────────────────────────────┐
│ PyUnicodeObject("34")  ← temporary, freed   │
│ PyLongObject(34)       ← a points here      │
└─────────────────────────────────────────────┘
       ▲
       │
    a (namespace)
```

**Key insight**: `int(input())` creates a **temporary string** from `input()`, then `int()` creates a **new integer** from that string. The temporary string is freed when `int()` finishes.

#### Adding Two Numbers — Full Breakdown

```python
# WITHOUT typecasting — FAILS
a = input("Enter first number: ")  # "3"
b = input("Enter second number: ") # "4"
# print(a + b) → "34" (string concatenation!)

# WITH typecasting — WORKS
a = int(input("Enter first number: "))  # PyLongObject(3)
b = int(input("Enter second number: ")) # PyLongObject(4)
print(a + b)  # 7 ← integer addition
```

```
Without typecasting:
┌──────────────┐     ┌──────────────┐
│ a → "3"     │ + │ b → "4"     │
│ (string)    │   │ (string)    │
└──────────────┘     └──────────────┘
         │
         ▼
    "34" ← concatenation, NOT addition

With typecasting:
┌──────────────┐     ┌──────────────┐
│ a → 3       │ + │ b → 4       │
│ (int)       │   │ (int)       │
└──────────────┘     └──────────────┘
         │
         ▼
    7 ← addition
```

#### The Shortcut — `int(input())` Directly

```python
# Instead of:
a = input("Enter first number: ")
a = int(a)

# Use the shortcut:
a = int(input("Enter first number: "))
```

**What happens internally:**
1. `input()` creates `PyUnicodeObject("3")` — temporary
2. `int()` reads that temporary, creates `PyLongObject(3)`
3. `a` is bound to `PyLongObject(3)`
4. The temporary `PyUnicodeObject` has refcount 0 → freed immediately

```
Memory:
┌─────────────────────────────────────────────┐
│ PyUnicodeObject("3")  ← temporary, freed    │
│ PyLongObject(3)       ← a points here       │
└─────────────────────────────────────────────┘
                              ▲
                              │
                           a (namespace)
```

**No intermediate variable** — the string exists only briefly inside the `int()` call.

#### The `+` Operator — Complete Behavior Map

| Operand 1 | Operand 2 | `+` Does | Example | Result |
|-----------|-----------|----------|---------|--------|
| `int` | `int` | Addition | `3 + 4` | `7` |
| `float` | `float` | Addition | `3.0 + 4.0` | `7.0` |
| `str` | `str` | Concatenation | `"3" + "4"` | `"34"` |
| `str` | `int` | **TypeError** | `"3" + 4` | Error |
| `int` | `str` | **TypeError** | `3 + "4"` | Error |
| `list` | `list` | Concatenation | `[1] + [2]` | `[1, 2]` |

**Rule**: `+` only works when both operands are the **same type** (or compatible types).

#### Why Python Doesn't Auto-Convert

```python
# Python does NOT automatically convert:
a = "34"
# a + 3  → TypeError (not 37)

# Why? Because "34" could mean:
#   - The number thirty-four
#   - A phone number
#   - A zip code
#   - A product code
# Python doesn't assume → you must be explicit
```

**Explicit is better than implicit** — this is a core Python philosophy (from "The Zen of Python": `import this`).

#### The Lecture's Example — Complete

```python
# The problem:
a = input("Enter first number: ")  # "3"
b = input("Enter second number: ") # "4"
# print(a + b) → "34" (wrong!)

# The fix:
a = int(input("Enter first number: "))  # 3
b = int(input("Enter second number: ")) # 4
print(a + b)  # 7 (correct!)
```

```
Without fix:
┌──────────────┐     ┌──────────────┐
│ a → "3"     │ + │ b → "4"     │
└──────────────┘     └──────────────┘
         │
         ▼
    "34" ← string concatenation

With fix:
┌──────────────┐     ┌──────────────┐
│ a → 3       │ + │ b → 4       │
└──────────────┘     └──────────────┘
         │
         ▼
    7 ← integer addition
```

#### Common Pitfalls

##### 1. Forgetting Typecasting
```python
a = input("Age: ")  # "25"
print(a + 1)        # TypeError!
# Fix: a = int(input("Age: "))
```

##### 2. Using `+` with Mixed Types
```python
"3" + 4    # TypeError
3 + "4"    # TypeError
# Fix: convert both to same type
int("3") + 4    # 7
str(3) + "4"    # "34"
```

##### 3. Float Input
```python
age = input("Height: ")  # "5.9"
# int(age) → ValueError! (can't parse "5.9" as int)
# Fix: float(age)
height = float(input("Height: "))  # 5.9
```

##### 4. Multiple Cursors Shortcut
The lecture mentions using VSCode's multiple cursors (`Alt + Click`) to type `int(` at multiple locations simultaneously — a productivity tip, not a Python concept.

#### Key Takeaways

1. **`+` with strings = concatenation** (`"3" + "4"` → `"34"`)
2. **`+` with integers = addition** (`3 + 4` → `7`)
3. **`+` with mixed types = TypeError** (`"3" + 4` → Error)
4. **`input()` always returns string** — even numeric input
5. **Fix**: `int(input())` or `float(input())` — convert immediately
6. **The shortcut pattern**: `a = int(input("prompt"))` — one line, no intermediate variable
7. **Python is explicit** — it won't auto-convert types for you
8. **Same `+` operator, different behavior** — determined by `ob_type->tp_add`

---

**Next: Unit 3** — Comments, Escape Sequences & Print Statement — how `#` comments work, escape sequences like `\n`, `\t`, and how `print()` formats output.
