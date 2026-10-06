# Lecture 21 — String Methods and Functions

**Units covered**: 1. String immutability, 2. `len()` and case methods,
3. Whitespace stripping methods, 4. Search and replace (`find`, `replace`),
5. Split and join, 6. Boolean checking methods

---

## Unit 1 — String Immutability

### Core Concept
Strings are **immutable** in Python. Once created, the character sequence
cannot change in memory. Any “modification” operation (like `upper()`,
`replace()`, slicing with assignment, etc.) returns a **new** string
object and leaves the original unchanged.

### What's Actually Happening
- When you write `name = "Harry"`, a `str` object is allocated in memory.
- `name[0] = 'r'` looks like valid Python syntax, but CPython checks at
  runtime whether the object supports item assignment.
- For `str`, `__setitem__` is **not implemented**. CPython raises
  `TypeError: 'str' object does not support item assignment`.
- Methods like `s.upper()`, `s.replace()`, etc., allocate a **new**
  string, copy/modify the data, and return it. The original `s`
  remains unchanged.

### Why It Matters
- **Memory safety**: Immutability means strings can be freely shared
  (interned, cached) without defensive copying.
- **Hashability**: Since strings are immutable, their hash value is
  cached and stable, making them usable as dict keys.
- **Side-effect debugging**: If you pass a string to a function, you
  know it won’t be silently mutated.

### Minimal Executable Examples

```python
name = "Harry"
# name[0] = "r"     # TypeError: 'str' object does not support item assignment

new_name = name.upper()
print(name)       # "Harry" — unchanged
print(new_name)   # "HARRY" — new object
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Assuming in-place change | `s = "hello"; s.upper(); print(s)` | Still `"hello"` — must reassign: `s = s.upper()` |
| `+=` looks in-place | `s += "x"` | Creates a **new** string, rebinds `s`. Original memory unchanged. |
| Slicing assignment | `s = "abc"; s[0:1] = "x"` | `TypeError` — strings do not support item assignment |

### Key Insight
Immutability is a guarantee, not just a convention. Any operation that
“changes” a string returns a new object.

---

## Unit 2 — `len()` and Case Methods

### Core Concept
`len()` returns the number of characters in a string. Case
transformation methods create a new string with modified casing:

| Method | Behavior |
|--------|----------|
| `str.upper()` | All characters → uppercase |
| `str.lower()` | All characters → lowercase |
| `str.capitalize()` | First character uppercase, rest lowercase |
| `str.title()` | First character of each word uppercase, rest lowercase |

### What's Actually Happening
- `len()` calls `PyUnicode_GetLength()` (or `str.__len__`), which
  reads the cached length stored in the `str` object header. O(1).
- Case methods iterate over Unicode code points and map each character
  through `Py_UNICODE_TO_UPPER` / `Py_UNICODE_TO_LOWER` (or
  locale-aware equivalents). The result is a newly allocated string.

### Minimal Executable Examples

```python
s = "hello world"
print(len(s))           # 11 — includes space
print(s.upper())        # "HELLO WORLD"
print(s.lower())        # "hello world"
print(s.capitalize())   # "Hello world"
print(s.title())        # "Hello World"
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Locale dependence | `"straße".upper()` in Turkish locale | Case mapping can be locale-dependent for some characters |
| `title()` on apostrophes | `"they're here".title()` → `"They'Re Here"` | Word boundaries split on apostrophes |

### Key Insight
`len(s)` is O(1) — the length is cached in the object header. Case
methods are O(n) — they create and return a new string.

---

## Unit 3 — Whitespace Stripping Methods

### Core Concept
Whitespace stripping removes leading and/or trailing whitespace
characters (`' '`, `'\t'`, `'\n'`, `'\r'`, `'\x0b'`, `'\x0c'`):

| Method | Behavior |
|--------|----------|
| `str.strip()` | Remove from **both** ends |
| `str.lstrip()` | Remove from **left** (start) only |
| `str.rstrip()` | Remove from **right** (end) only |

### What's Actually Happening
- Each method scans from the respective end(s) until a non-whitespace
  character is found.
- It uses the Unicode whitespace character database (or ASCII,
  depending on the build). For CPython, `Py_UNICODE_ISSPACE()`
  determines membership.
- The method returns a **new** string with the slice removed.

### Minimal Executable Examples

```python
text = "  hello world  \n\t"
print(repr(text.strip()))   # "'hello world'"
print(repr(text.lstrip()))  # "'hello world  \\n\\t'"
print(repr(text.rstrip()))  # "'  hello world'"
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| `strip()` removes all whitespace | `" a\\nb ".strip()` → `"a\\nb"` | `\n` inside the string is **not** removed; only leading/trailing |
| Stripping non-whitespace | `"xxhello".strip("x")` → `"hello"` | `strip(chars)` removes any chars in the given set, not just whitespace |
| `rstrip("\n")` on multi-line | Removes trailing newlines only | Does not remove internal newlines |

### Key Insight
`strip()` is purely about ends — it never touches internal whitespace.
Use `replace()` or regex for internal cleanup.

---

## Unit 4 — Search and Replace (`find`, `replace`)

### Core Concept
- `str.find(sub)` returns the **index of the first occurrence** of
  `sub`, or `-1` if not found.
- `str.replace(old, new)` returns a **new** string with **all**
  occurrences of `old` replaced by `new`.

### What's Actually Happening
- `find()` performs a substring search. CPython uses optimized
  algorithms (e.g., Boyer-Moore-Horspool or a fast memchr-like search
  for short needles). Returns `Py_ssize_t` index or `-1`.
- `replace()` scans the string, builds a new buffer, and copies
  everything except the matched `old` substrings, inserting `new` in
  their place. All occurrences are replaced; it is not
  first-occurrence-only.

### Minimal Executable Examples

```python
text = "Python is fun and fun"
print(text.find("is"))    # 7
print(text.find("Java"))  # -1 (not found)

print(text.replace("fun", "awesome"))
# "Python is awesome and awesome"
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| `find` vs `index` | `s.index("x")` vs `s.find("x")` | `index()` raises `ValueError`; `find()` returns `-1` |
| Case sensitivity | `"Python".find("py")` → `-1` | `find` is case-sensitive; use `lower()` first |
| Partial overlap | `"aaa".replace("aa", "b")` → `"ba"` | Replace is left-to-right; overlapping matches are not double-replaced |

### Key Insight
`find()` returns `-1` for “not found” — never rely on truthiness
alone. `replace()` is global and returns a new string.

---

## Unit 5 — Split and Join

### Core Concept
- `str.split(sep)` splits the string into a **list** of substrings
  using `sep` as the delimiter.
- `str.join(iterable)` concatenates an **iterable of strings** into a
  single string, inserting the original string between each element.

### What's Actually Happening
- `split(sep)` scans left-to-right. Each time `sep` is found, the
  preceding text becomes one list element. Consecutive separators
  produce empty strings.
- `join(sep)` calculates the total length of the result, allocates one
  contiguous buffer, and copies all elements with `sep` between them.
  This is more efficient than repeated string concatenation.

### Minimal Executable Examples

```python
text = "apples,bananas,pineapples"
parts = text.split(",")
print(parts)           # ['apples', 'bananas', 'pineapples']

joined = ",".join(parts)
print(joined)          # "apples,bananas,pineapples"
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| `split()` without args | `"a  b".split()` → `['a', 'b']` | Splits on **any** whitespace and discards empty strings |
| `join` with non-strings | `",".join([1, 2])` → `TypeError` | All elements must be strings |
| `split` on empty string | `"".split(",")` → `['']` | Returns `['']`, not `[]` |
| Trailing separator | `"a,b,".split(",")` → `['a', 'b', '']` | Trailing empty string preserved |

### Key Insight
`split()` turns a delimited string into a list; `join()` turns a list
back into a string. They are inverses when using the same separator.

---

## Unit 6 — Boolean Checking Methods

### Core Concept
These methods return `True` or `False` based on string content:

| Method | Returns `True` when |
|--------|---------------------|
| `str.isalpha()` | All characters are alphabetic and there is at least one character |
| `str.isdigit()` | All characters are digits |
| `str.isalnum()` | All characters are alphanumeric (letters or digits) |
| `str.isspace()` | All characters are whitespace and there is at least one character |

### What's Actually Happening
- Each method iterates over the string's Unicode code points and
  applies a predicate.
- `isalpha()` checks `Py_UNICODE_ISALPHA`; `isdigit()` checks
  `Py_UNICODE_ISDIGIT`; etc.
- Empty string returns `False` for all of these (the standard methods
  require at least one character to return `True`).

### Minimal Executable Examples

```python
print("abc".isalpha())    # True
print("abc123".isalpha()) # False
print("123".isdigit())    # True
print("abc123".isdigit()) # False
print("abc123".isalnum()) # True
print("   ".isspace())    # True
print("".isspace())       # False — empty string
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| `isdigit()` vs `isnumeric()` | `"½".isdigit()` → `False`; `"½".isnumeric()` → `True` | `isnumeric()` includes more Unicode numeric characters |
| Empty string | `"".isalpha()` → `False` | All checks require at least one character |
| Whitespace in `isalnum` | `"a b".isalnum()` → `False` | Space is neither alpha nor digit |

### Key Insight
These predicates are Unicode-aware. `isalpha()` returns `True` for
letters from any script (e.g., `"αβγ".isalpha()` → `True`), not just
ASCII.

---

**End of Lecture 21 — String Methods and Functions**

All 6 units documented. Ready for the next step.