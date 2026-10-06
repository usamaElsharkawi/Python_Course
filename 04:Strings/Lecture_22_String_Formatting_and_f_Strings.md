# Lecture 22 — String Formatting and f-Strings

**Units covered**: 1. Why formatting exists: the template problem, 2.
f-strings: inline expression formatting, 3. Character encoding:
`ord()` and `chr()`, 4. Summary: string functions covered in this
section

---

## Unit 1 — Why Formatting Exists: The Template Problem

### Core Concept
When you need to inject variables into a fixed string template,
**string formatting** lets you create the final message without manual
concatenation or repeated `print` statements.

### What's Actually Happening
The lecture introduces the **`.format()`** method:

```python
template = "Dear {}, you are awesome. Take this ${} back"
name = "John"
amount = 10000
s1 = template.format(name, amount)
```

`str.format()`:
1. Scans the string for `{}` placeholders
2. Replaces each placeholder, left-to-right, with the corresponding
   positional argument
3. Returns a **new** string; the original `template` is unchanged

Under the hood in CPython, this is implemented in `builtin_format()`
and the `str.__format__` machinery, which parses format specifiers,
calls `__format__` on each argument, and assembles the result.

### Minimal Executable Examples

```python
template = "Dear {}, you are awesome. Take this ${} back"
a, a1 = "John", 10000
s1 = template.format(a, a1)
print(s1)
# Dear John, you are awesome. Take this $10000 back
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Mismatched placeholders | `"{x}".format(1)` | `IndexError` if positional index is out of range |
| Reusing placeholders | `"{0} vs {0}".format(a)` | Works, but empty `{}` always consumes the next positional arg |
| Curly braces in output | `"Set: {1, 2, 3}"` | Interpreted as format field; use `{{` and `}}` to escape |

### Key Insight
`.format()` separates the **template** (structure) from the **data**
(variables). It was the standard before Python 3.6 and is still fully
supported.

---

## Unit 2 — f-Strings: Inline Expression Formatting

### Core Concept
An **f-string** (formatted string literal) is created by prefixing a
string with `f` or `F`. Inside the string, `{expression}` is replaced
by the value of that expression at runtime.

```python
a, a1 = "John", 10000
s = f"Dear {a}, you are awesome. Take this ${a1} back"
```

### What's Actually Happening
- The parser recognizes the `f` prefix and processes the string at
  **compile time**.
- Each `{...}` expression is evaluated and converted via `__format__`
  during string construction.
- f-strings are generally **faster** than `.format()` because the
  parsing and evaluation happen at compile time, not runtime.

In CPython, f-strings are implemented in the parser
(`Parser/action_helpers.c`) and compiled to `FORMAT_VALUE` and
`BUILD_STRING` bytecode instructions.

**Bytecode example:**

```
  1           0 LOAD_NAME                0 (a)
              2 LOAD_NAME                1 (a1)
              4 FORMAT_VALUE            2
              6 BUILD_STRING             3
              8 RETURN_VALUE
```

`FORMAT_VALUE` calls `__format__` on the loaded object, and
`BUILD_STRING` assembles the final string.

### Why It Matters
- **Readability**: `f"{name} is {age} years old"` is far cleaner than
  `"{} is {} years old".format(name, age)`.
- **Performance**: f-strings are typically 2-5x faster than `%`
  formatting or `.format()`.
- **Expressiveness**: Any valid Python expression can go inside `{}`:
  `f"2+2={2+2}"`, `f"upper={name.upper()}"`.

### Minimal Executable Examples

```python
name, amount = "John", 10000
s = f"Dear {name}, you are awesome. Take this ${amount} back"
print(s)
# Dear John, you are awesome. Take this $10000 back
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Same braces for literal `{`/`}` | `f"value: {x} kg"` | Use `{{` and `}}` for literal braces |
| Backslash in expression | `f"{\n}"` | `SyntaxError` — expressions cannot contain backslashes |
| Evaluation time | `f"{x}"; x = 5` | `NameError` — evaluated at runtime when the f-string is constructed |
| Quote confusion | `f'It\'s {x}'` | Works; use opposite quotes or escape to avoid confusion |

### Key Insight
f-strings are **compile-time parsed** and **runtime evaluated**. They
are the idiomatic way to embed variables in strings in modern Python
(3.6+).

---

## Unit 3 — Character Encoding: `ord()` and `chr()`

### Core Concept
- `ord(character)` → returns the **Unicode code point** (integer) of a
  single character.
- `chr(code_point)` → returns the **character** for a given Unicode
  code point.

These bridge the gap between human-readable characters and their
numeric representations.

### What's Actually Happening
- `ord('A')` looks up the code point for `'A'` in the Unicode table.
  In ASCII/Unicode, `'A'` is `U+0041` = `65`.
- `chr(65)` maps the integer `65` back to `'A'`.
- In CPython, `ord()` calls `PyUnicode_Ord()`, and `chr()` calls
  `_PyUnicode_FromOrdinal()`.

**ASCII vs Unicode:**
- ASCII defines 128 characters (0–127). `ord()`/`chr()` work for the
  full Unicode range (0–1,114,111).

### Minimal Executable Examples

```python
print(ord('A'))   # 65
print(chr(65))    # 'A'
print(ord('α'))   # 945 (Greek small letter alpha)
print(chr(945))   # 'α'
print(ord(' '))   # 32 (space character)
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Multi-character strings | `ord("AB")` | `TypeError` — `ord()` expects exactly one character |
| Invalid code point | `chr(9999999)` | `ValueError` if outside valid Unicode range |
| ASCII assumption | `chr(200)` → `'È'` | Not all values 0–255 are printable ASCII |

### Key Insight
`ord()` and `chr()` are inverses of each other within valid ranges.
They expose the underlying numeric representation that Python uses for
characters.

---

## Unit 4 — Summary: String Functions Covered in This Section

| Function/Method | Purpose | Returns |
|-----------------|---------|---------|
| `len(s)` | Length of string | `int` |
| `s.upper()` | Uppercase | new `str` |
| `s.lower()` | Lowercase | new `str` |
| `s.capitalize()` | First char uppercase, rest lowercase | new `str` |
| `s.title()` | Title case | new `str` |
| `s.strip()` | Remove whitespace from both ends | new `str` |
| `s.lstrip()` | Remove whitespace from left | new `str` |
| `s.rstrip()` | Remove whitespace from right | new `str` |
| `s.find(sub)` | Index of first `sub`, or `-1` | `int` |
| `s.replace(old, new)` | Replace all occurrences | new `str` |
| `s.split(sep)` | Split into list | `list` |
| `sep.join(iterable)` | Join iterable into string | `str` |
| `s.isalpha()` | All alphabetic? | `bool` |
| `s.isdigit()` | All digits? | `bool` |
| `s.isalnum()` | Alphanumeric? | `bool` |
| `s.isspace()` | All whitespace? | `bool` |
| `ord(c)` | Unicode code point | `int` |
| `chr(i)` | Character from code point | `str` |
| `s.format(...)` | Template substitution | new `str` |
| `f"...{var}..."` | f-string interpolation | new `str` |

### Key Insight
Strings are **immutable**. Every function/method that "modifies" a
string returns a **new** object. Use reassignment (`s = s.upper()`) to
update variables.

---

**End of Lecture 22 — String Formatting and f-Strings**

All 4 units documented. Ready for the next step.