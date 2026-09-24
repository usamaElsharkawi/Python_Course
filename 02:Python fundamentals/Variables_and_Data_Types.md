# Lecture 1: Variables and Data Types in Python

---

## Unit 1: Variables as Memory Locations — Python's Object Model, Assignment Semantics, Reference Semantics

### Core Truth

**Variables are not containers** like kitchen boxes. They are **labels/names** that point to **objects** (actual data) living on the heap.

```python
# WRONG: "variable is container"
age = 34

# RIGHT: "variable is label pointing to object"
# ┌─────────────┐
# │   "age"     │ ──refers to──▶ PyLongObject(34)
# └─────────────┘                    ↓
#                                 type=int
```

### The Model

| Component | What It Is | Analogy |
|-----------|------------|---------|
| **Variable** | Name in a namespace dict | Label on a box |
| **Object** | Actual data on heap + type attached | The box itself |
| **Assignment** | Point name to object | Labeling the box |
| **Type** | Attached to object, not variable | Box label (int, str, etc.) |

### How Python Executes `age = 34`

1. **Object Creation**: Integer `34` is created on heap with type `int` attached
2. **Binding**: Name `"age"` in current namespace (global dict) points to that object

```python
# Internals visualization:
# globals = {"age": <PyLongObject at 0x...>}  
# PyLongObject structure: {value: 34, type: int, refcount: 1}
```

### Key Principles

#### 1. Multiple Names → Single Object
```python
# Two names pointing to the SAME list object
a = [1, 2, 3]
b = a
b.append(4)    # Modifies the shared list
print(a)       # [1, 2, 3, 4] ← both a and b see it
```

#### 2. Objects Carry Their Type
```python
age = 34
print(type(age))  # <class 'int'>
name = "Harry"   
print(type(name)) # <class 'str'>
```

Variables don't have types — objects do.

#### 3. Immutability vs. Mutability
```python
# Immutable: Create new object on "modification"
x = 10
y = x
x = 20  # Creates new int object, x now points to new object
print(y)  # 10 ← y still points to original

# Mutable: Changes affect all names
mylist = [1, 2]
other = mylist
other.append(3)
print(mylist)  # [1, 2, 3] ← both see changes
```

### The "Container" Analogy Fixed

| Lecture Model | Python Reality |
|---------------|----------------|
| Variable = container holding value | Variable = label pointing to object |
| Assignment = put value in container | Assignment = stick label on object |
| Multiple variables = multiple containers | Multiple names = multiple labels on same object |

### Key Takeaways

1. **Variables are labels, not containers**
2. **Objects carry their type, variables don't**
3. **Multiple names can point to same object**
4. **Immutable vs mutable behavior differs**
5. **No variable type declarations at runtime**
6. **Memory is managed via reference counting**

### Exercises

1. Explain `a = b = [1, 2, 3]`
2. Why `a = 5; b = a; a = 10` doesn't affect `b`
3. Demonstrate mutable vs immutable reassignment
4. Show how `type()` reveals object type, not variable type
5. Explain reference counting with simple examples

---

**Next: Unit 2** — Dynamic Typing & PyObject Internals

### Unit 2: Dynamic Typing — PyObject Internals, Type Tags, and Type Inference

#### Core Truth
**Types live on objects, not variables.** When you write `age = 34`, the integer object carries its type information (int) with it. The variable `age` is just a name pointing to that object.

```
PyObject (HEAP)                   ← Object with its type attached
┌─────────────────┐               ┌─────────────────────┐
│ ob_refcnt: 1     │               │ PyLong_Type        │
│ ob_type: ────▶   │──▶ age ─────▶│  tp_name: "int"    │
│ PyLong_Type     │               │   (in memory)      │
└─────────────────┘               └─────────────────────┘
           │                           │
           │    Variable points here   │
           ▼                           ▼
      Name in namespace dict      Value: 34
```

#### How Python "Figures Out" Types

1. **Literal Creation**: When you write `34`, the **compiler** creates a `PyLongObject` at parse time
2. **Type Attached**: Every object has `ob_type` pointer → `PyLong_Type`
3. **Runtime Lookup**: `type(age)` follows `age` → `PyObject*` → read `ob_type`

#### Key Points

| Concept | What Happens | Memory View |
|---------|-------------|-------------|
| `age = 34` | Creates int object, binds name to it | Heap: PyLongObject, Namespace: "age" → PyLongObject |
| `type(age)` | Follows pointer to `ob_type` field | Returns `PyLong_Type` object |
| `age = "text"` | Creates new str object, rebinds name | Heap: PyUnicodeObject, Namespace: "age" → PyUnicodeObject |

#### The PyObject Header (What Every Python Object Has)

```c
typedef struct _object {
    Py_ssize_t ob_refcnt;   // Reference count
    PyTypeObject *ob_type;  // ← Type tag (key!)
} PyObject;
```

**Every Python object**: int, str, list, custom class → has this exact structure!

#### Type Dispatch (How `+` Works)

```python
# Every operation checks the type at runtime
def add_py(a, b):
    # CPython internals (simplified):
    if a->ob_type->tp_as_number && a->ob_type->tp_as_number->nb_add:
        return a->ob_type->tp_as_number->nb_add(a, b)
    if b->ob_type->tp_as_number && b->ob_type->tp_as_number->nb_add:
        return b->ob_type->tp_as_number->nb_add(b, a)
    # ... error handling ...
```

**Every `+`** → type check → dispatch to right method → runtime polymorphism

#### Dynamic Typing (Conceptual)

| Aspect | Python (Dynamic) | Static (C / Java) |
|--------|------------------|-------------------|
| **Type storage** | In object (`ob_type` field) | In variable declaration |
| **Type checking** | Every operation (`+`, `len()`, etc.) | Compile-time only |
| **Generic code** | Works on any object with right methods | Need function overloading / templates |
| **Type errors** | `TypeError` at runtime | Compile error |

#### Type Annotations (Optional Metadata)

```python
# Runtime: ignored completely
age: int = 34      # Stored in __annotations__, but Python doesn't check

# Static analysis tools (mypy, pyright):
def foo(x: int, y: str) -> bool: ...
# At runtime: function is just def foo(x, y): ...
```

#### Why Dynamic Typing Matters

1. **Flexibility**: Same function works for `int`, `float`, `Decimal`, `numpy.int64`
2. **Duck typing**: Any object with `__add__` works with `+`
3. **Easier refactoring**: Add new types without changing function signatures

```python
# Works for any numeric type!
def calculate(value, multiplier):
    return value * multiplier  # Works for int, float, Decimal...

print(calculate(5, 3))       # 15
print(calculate(5.5, 3))     # 16.5
```

#### Common Pitfalls

```python
# Type annotations don't enforce types at runtime!
x: int = "not an int"  # This works (no runtime error)
print(type(x))        # <class 'str'>
```

```python
# Duck typing can mask bugs!
def get_length(obj):
    return len(obj)  # Works for str, list, dict, but not int!

print(get_length("hello"))  # 5
print(get_length([1,2,3]))  # 3
# print(get_length(42))   # TypeError (but only when run)
```

#### Key Takeaways

1. **Types are on objects** (`ob_type` pointer)
2. **Compiler creates typed objects** for literals
3. **Every operation checks types** and dispatches accordingly
4. **Type annotations are metadata only** (ignored at runtime)
5. **Dynamic = runtime polymorphism for free**
6. **Memory is managed via reference counting**

### Exercises

1. Explain `a = 34` vs `b = a` in terms of object creation
2. Why `type(34)` returns `<class 'int'>`
3. Show how `+` works with different types
4. Demonstrate reference counting behavior
5. Show why type annotations don't prevent type errors

---

**Next: Unit 3** — Variable Naming Rules — Python's Identifier Grammar

### Unit 3: Variable Naming Rules — Python's Identifier Grammar

#### Core Truth
**Python has strict rules about what can be used as variable names.** These are defined in PEP 3131 and the Python language reference. The rules specify valid characters and patterns for identifiers.

#### What Makes a Valid Variable Name?

A variable name (identifier) must follow these rules:

| Rule | Example | Valid? |
|------|---------|--------|
| **Must start with letter or underscore** | `age`, `_name`, `__init__` | ✅ Yes |
| **Cannot start with digit** | `34age`, `2cool` | ❌ No |
| **Can contain letters, digits, underscores** | `var1`, `name_2`, `item_3` | ✅ Yes |
| **Case sensitive** | `age` vs `Age` vs `AGE` | ✅ Three different variables |
| **Cannot be Python keyword** | `if`, `while`, `for`, `class`, `def` | ❌ No (reserved) |

#### Visual: What VS Code Sees

```
# Valid (VS Code: no underline)
age = 34
_name = "Harry"
var_123 = 1.5

# Invalid (VS Code: red underline)
34age = 10      # ❌ Starts with digit
\$dollar = 5    # ❌ Special character
if = 10         # ❌ Keyword
```

#### Under the Hood: What Python Actually Does

When Python parser sees `34age`:

1. **Tokenizer** reads `34` as number literal
2. **Sees** `age` identifier
3. **Fails** because identifier can't start with digit
4. **SyntaxError**: `invalid syntax`

When Python parser sees `\$dollar`:

1. **Tokenizer** reads `\$` 
2. **Fails** because `\$` is not valid in identifiers
3. **SyntaxError**: `invalid character in identifier`

#### Python Keywords (Reserved Words)

These 35+ words **cannot** be used as variable names:

```python
False, None, True, and, as, assert, async, await,
break, class, continue, def, del, elif, else,
except, finally, for, from, global, if, import,
in, is, lambda, nonlocal, not, or, pass, raise,
return, try, while, with, yield
```

#### Workaround: Using Keywords as Variables

```python
# ❌ Doesn't work (SyntaxError)
# if = 10

# ✅ Workarounds:
if_ = 10          # Add underscore suffix
_if = 10          # Add underscore prefix
if_10 = 10        # Add suffix with number
```

#### Unicode in Variable Names

Python 3 fully supports Unicode identifiers:

```python
# These are ALL valid variable names in Python 3:
λ = "lambda"        # Greek lambda
α = 3.14           # Greek alpha
日本語 = "test"    # Japanese characters
émoji = "🚀"       # With emoji (yes, really!)
```

```python
# Examples:
λ_func = lambda x: x + 1
α_π = 3.14159
print(λ_func(5))    # 6
print(α_π)          # 3.14159
```

#### What About Special Characters?

| Character | Valid in Variable Name? |
|-----------|------------------------|
| Letters (a-z, A-Z, Unicode) | ✅ Yes |
| Digits (0-9) | ❌ Only after first character |
| Underscore (_) | ✅ Yes |
| Dollar sign (\$) | ❌ No |
| At sign (@) | ❌ No |
| Percent (%) | ❌ No |
| Hash (#) | ❌ No |
| Dot (.) | ❌ No |
| Space | ❌ No |

#### Comparison: What's Allowed Where

| Language | First Char | Subsequent Chars |
|----------|-----------|------------------|
| **Python** | a-z, A-Z, _ | a-z, A-Z, 0-9, _ |
| **JavaScript** | a-z, A-Z, _, \$ | a-z, A-Z, 0-9, _, \$ |
| **TypeScript** | same as JS (erased at runtime) | same as JS |
| **C** | a-z, A-Z, _ | a-z, A-Z, 0-9, _ |
| **Rust** | a-z, A-Z, _ | a-z, A-Z, 0-9, _ |

#### Why These Rules Exist

1. **Parser simplicity**: Compiler can easily distinguish identifiers from numbers/literals
2. **Language consistency**: Same rules apply everywhere (functions, classes, variables)
3. **Avoid ambiguity**: `age` vs `3age` — rules prevent confusion
4. **Historical legacy**: C's identifier syntax carried forward

#### Demonstration: What Python Accepts/Rejects

```python
# Valid assignments:
my_var = 1        # Starts with letter
_my_var = 2       # Starts with underscore
my_var_1 = 3      # Contains digit after first char
λ_var = 4         # Unicode (Python 3)
__dunder__ = 5    # Special methods convention

# Invalid (will cause SyntaxError):
# 1var = 6        # Starts with digit → SyntaxError
# my-var = 7      # Contains hyphen → SyntaxError
# class = 8       # Keyword → SyntaxError
```

#### Common Beginner Mistakes

1. **Using hyphens**: `my-var = 1` → SyntaxError (looks like subtraction)
2. **Starting with number**: `1st = "first"` → SyntaxError
3. **Using keywords**: `for = 5milo` → SyntaxError (or overwrites keyword)
4. **Spaces in names**: `my var = 1` → SyntaxError (spaces not allowed)

#### Why This Matters

```python
# These are ALL different variables (case sensitive):
age = 25
Age = 30
AGE = 35

print(age)  # 25
print(Age)  # 30
print(AGE)  # 35

# Changing one doesn't affect others
age = 99
print(age)  # 99 ← only age changed, Age and AGE unchanged
```

#### Key Takeaways

1. **Must start with letter (a-z, A-Z) or underscore (_)**
2. **Cannot start with digit (0-9)**
3. **Can contain: letters, digits, underscores (after first char)**
4. **Case sensitive: `age`, `Age`, `AGE` are different variables**
5. **Cannot use Python keywords: `if`, `while`, `class`, `def`, etc.**
6. **Python 3 supports Unicode identifiers (λ, α, 日本語, etc.)**
7. **No special characters: no \$, @, %, -, spaces, etc.**
8. **VS Code red underline = actual syntax error, not just style warning**

---

**Next: Unit 4** — Built-in Scalar Types (int, float, str, bool) — Internal Representation, Immutability

---

### Unit 4: Built-in Scalar Types — Internal Representation, Immutability

#### Core Truth
**Each scalar type has a specific internal memory layout.** Python's `int`, `float`, `str`, and `bool` are not just abstract concepts — they have concrete C structures in CPython with fixed memory footprints and specific behaviors.

#### The Four Scalar Types at a Glance

| Type | C Struct | Size (approx) | Mutable? | Examples |
|------|----------|---------------|----------|----------|
| **int** | `PyLongObject` | 28 bytes | ❌ Immutable | `34`, `-5`, `1000000` |
| **float** | `PyFloatObject` | 24 bytes | ❌ Immutable | `3.14`, `-0.5`, `8.2` |
| **str** | `PyUnicodeObject` | Variable | ❌ Immutable | `"Harry"`, `"hello"` |
| **bool** | `PyBoolObject` | 1 byte (singleton) | ❌ Immutable | `True`, `False` |

#### 1. Integer (`int`) — Arbitrary Precision

##### Internal Structure

```c
// Objects/longobject.h (simplified)
typedef struct {
    PyObject_HEAD
    digit ob_digit[1];  // Array of "digits" (30-bit chunks)
} PyLongObject;
```

**Key insight**: Python integers are **arrays of 30-bit digits**, not fixed-size C `int`s. This enables **arbitrary precision**.

##### Small Integer Caching

```python
# Small integers (-5 to 256) are pre-allocated singletons
a = 256
b = 256
print(a is b)  # True ← Same object!

c = 257
d = 257
print(c is d)  # False ← Different objects (not cached)
```

**Why?** Small ints are created at interpreter startup and reused. This saves memory and speeds up common operations.

##### Arithmetic Operations

```python
# Addition creates NEW int objects (immutability)
a = 10
b = a + 5    # Creates NEW PyLongObject(15)
# a still points to PyLongObject(10)
```

#### 2. Float (`float`) — IEEE 754 Double Precision

##### Internal Structure

```c
// Objects/floatobject.h
typedef struct {
    PyObject_HEAD
    double ob_fval;  // C double (64-bit IEEE 754)
} PyFloatObject;
```

**Key insight**: Python floats are **C doubles** — 64-bit IEEE 754 format:
- 1 bit for sign
- 11 bits for exponent
- 52 bits for mantissa (fraction)

##### Precision Limitations

```python
# Precision limitations
print(0.1 + 0.2)  # 0.30000000000000004 ← Not exactly 0.3!
print(0.1 + 0.2 == 0.3)  # False
```

**Why?** `0.1` and `0.2` cannot be represented exactly in binary floating point. The sum accumulates rounding errors.

##### Float Operations

```python
# All float operations create new objects
x = 3.14
y = x + 1.0    # Creates NEW PyFloatObject(4.14)
print(x)        # 3.14 ← original unchanged
```

#### 3. String (`str`) — Unicode, Immutable

##### Internal Structure

```c
// Objects/unicodeobject.h (simplified)
typedef struct {
    PyObject_HEAD
    Py_ssize_t length;
    Py_UCS4 *data;      // Pointer to UTF-32 encoded data
    Py_hash_t hash;     // Cached hash value
    int kind;           // 1=Latin-1, 2=UCS-2, 4=UCS-4
} PyUnicodeObject;
```

**Key insight**: Python 3 strings are **Unicode** with flexible encoding:
- **Latin-1** (1 byte/char) for ASCII characters
- **UCS-2** (2 bytes/char) for BMP characters
- **UCS-4** (4 bytes/char) for full Unicode

##### String Immutability

```python
# String immutability
s = "hello"
# Attempting to modify creates a NEW string
s2 = s + " world"  # NEW PyUnicodeObject
print(s)    # "hello" ← unchanged
print(s2)   # "hello world"
```

##### String Interning

```python
# Short strings and identifiers are interned (cached)
a = "hello"
b = "hello"
print(a is b)  # True ← Same object (interned)

c = "hello world"
d = "hello world"
print(c is d)  # False ← Not interned (longer string)
```

**Why immutability matters:**
- Enables safe use as dictionary keys (hash never changes)
- Enables thread safety (no locks needed)
- Allows string interning optimization

#### 4. Boolean (`bool`) — Subclass of `int`

##### Internal Structure

```c
// Objects/boolobject.h
typedef struct {
    PyLongObject long;  // bool IS a subclass of int!
} PyBoolObject;
```

**Key insight**: `bool` is a **subclass of `int`** in Python!

```python
# Proof:
print(issubclass(bool, int))  # True
print(True + True)            # 2 (True == 1)
print(True * 10)              # 10
print(False == 0)             # True
print(False + 5)              # 5
```

##### Boolean Singletons

```python
# Only TWO boolean objects exist in memory
True  # Singleton object
False # Singleton object

print(True is True)   # True
print(False is False) # True
print(True is 1)      # False (different objects, though equal)
print(True == 1)      # True (but different objects)
```

#### Immutability — The Common Thread

**All four scalar types are immutable.** This means:

```python
# Once created, the object NEVER changes
x = 10
x = x + 1  # Creates NEW object, rebinds x
# Original PyLongObject(10) still exists (if referenced elsewhere)
```

##### What Immutability Enables

| Feature | How Immutability Helps |
|---------|------------------------|
| **Hashability** | Objects can be dict keys (hash never changes) |
| **Thread safety** | No locks needed (can't be modified) |
| **Caching** | Same value = same object (small int, string interning) |
| **Predictability** | Function arguments can't be accidentally changed |

##### Mutable vs Immutable Comparison

```python
# IMMUTABLE: Creates new object on "change"
x = 10
y = x
x = 20
print(y)  # 10 ← original unchanged

# MUTABLE: Modifies the same object
a = [1, 2]
b = a
a.append(3)
print(b)  # [1, 2, 3] ← b sees the change!
```

#### Memory Layout Comparison

```
┌─────────────────────────────────────────────────────────────┐
│                    HEAP                                      │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ PyLongObject │  │ PyFloatObject│  │PyUnicodeObj  │     │
│  │ ob_refcnt: 2 │  │ ob_refcnt: 1 │  │ ob_refcnt: 3 │     │
│  │ ob_type:int  │  │ ob_type:float│  │ ob_type:str  │     │
│  │ value: 34    │  │ ob_fval:8.2  │  │ length:5     │     │
│  └──────────────┘  └──────────────┘  │ data:"Harry" │     │
│                                      └──────────────┘     │
│                                                             │
│  ┌──────────────┐                                          │
│  │ PyBoolObject │                                          │
│  │ (subclass    │                                          │
│  │  of int)     │                                          │
│  │ value: True  │                                          │
│  └──────────────┘                                          │
└─────────────────────────────────────────────────────────────┘

NAMESPACE (dict):
┌─────────────────────────────────────────┐
│ "age"    ──▶ PyLongObject(34)           │
│ "gpa"    ──▶ PyFloatObject(8.2)         │
│ "name"   ──▶ PyUnicodeObject("Harry")   │
│ "done"   ──▶ PyBoolObject(True)         │
└─────────────────────────────────────────┘
```

#### Type Conversion

```python
# Explicit conversion between scalar types
int(3.9)      # 3 (truncates float)
float(5)      # 5.0 (converts int)
str(42)       # "42" (converts to string)
bool(0)       # False (empty/falsy → False)
bool(1)       # True (non-zero → True)
int("10")     # 10 (parses string)
float("3.14") # 3.14 (parses string)
```

#### Common Pitfalls

##### 1. Float Precision
```python
# Don't compare floats with ==
print(0.1 + 0.2 == 0.3)  # False
# Use math.isclose() instead
import math
print(math.isclose(0.1 + 0.2, 0.3))  # True
```

##### 2. String Concatenation in Loops
```python
# INEFFICIENT: Creates new string each iteration
result = ""
for i in range(1000):
    result += str(i)  # 1000 new string objects!

# EFFICIENT: Single allocation
result = "".join(str(i) for i in range(1000))
```

##### 3. Boolean Arithmetic
```python
# Booleans behave like integers (subclass!)
print(True + True)    # 2
print(True * False)   # 0
# This can be confusing if you expect boolean-only behavior
```

##### 4. Small Int Caching Surprises
```python
# Works for small ints (-5 to 256)
a = 256
b = 256
print(a is b)  # True

# Fails for larger ints
c = 257
d = 257
print(c is d)  # False (implementation detail, don't rely on this!)
```

#### Key Takeaways

1. **`int`**: Array of 30-bit digits → arbitrary precision. Small ints (-5 to 256) cached as singletons.
2. **`float`**: C `double` (64-bit IEEE 754). Precision limitations cause `0.1 + 0.2 != 0.3`.
3. **`str`**: Unicode with flexible encoding (Latin-1/UCS-2/UCS-4). Immutable, interned for short strings.
4. **`bool`**: Subclass of `int`. `True == 1`, `False == 0`. Only two singleton objects exist.
5. **All scalar types are immutable**: Operations create new objects, never modify existing ones.
6. **Immutability enables**: Hashability, thread safety, caching, predictability.
7. **Memory layout matters**: Each type has a specific C struct with different fields and sizes.

#### Exercises

1. Explain why `a = 256; b = 256; a is b` returns `True` but `c = 257; d = 257; c is d` returns `False`
2. Demonstrate float precision issue with `0.1 + 0.2`
3. Show string immutability with a code example
4. Prove `bool` is a subclass of `int`
5. Compare memory usage of `int(1000)` vs `int(100)`
6. Explain why string interning doesn't work for long strings
7. Show the difference between `==` and `is` for scalar types

---

**Next: Unit 5** — Collection Types Overview (list, tuple, set, dict) — Mutability, Hashability