# Lecture 19 — Strings in Python

**Completed**: Units 1, 2, 3

---

## Unit 1 — String Creation and Representation

### Core Concept
Python strings are immutable sequences of Unicode characters. The lecture introduced three syntactic forms for creating them:

| Form | Delimiters | Typical Use |
|------|------------|-------------|
| Single-quoted | `'...'` | Preferred for simple strings |
| Double-quoted | `"..."` | Same as single; useful when the string contains apostrophes |
| Triple-quoted | `'''...'''` or `"""..."""` | Multi-line strings; also used for docstrings/comments |

### What's Actually Happening

**1. String literal parsing**
During Python's parsing phase, string literals are tokenized. Triple-quoted strings consume everything between the opening and closing delimiter, including newlines, until the exact same delimiter is encountered. The string object at runtime contains the raw character sequence, including any embedded `\n`.

**2. Runtime object model (CPython)**
At runtime, a `str` object is created. In CPython, strings use one of two representations:

- **Compact string representation** (compact ASCII/Latin-1) for strings composed of characters in the range U+0000–U+00FF. Lower memory footprint, faster allocation.
- **Unicode compact/length representation** for strings containing characters outside that range. A `PyUnicodeObject` structure stores the character data and metadata.

Both representations are **immutable**: once created, the character sequence cannot change in-place. Any "modification" operation (concatenation, slicing, etc.) returns a **new** string object.

**3. Triple quotes as comments / docstrings**
A triple-quoted string that is not assigned to a variable and not passed to a function is simply a statement whose value is evaluated and discarded. Since it is syntactically valid and has no side effects, it behaves like a comment. This is why docstrings work — they appear as the first statement in a module/class/function and are stored in `__doc__`, but otherwise they are ignored.

### Minimal Executable Examples

```python
# Single vs double quotes
name_single = 'Harry'
name_double = "Harry"
print(name_single == name_double)  # True

# Triple-quoted single-line
tri = '''Harry'''
print(tri)

# Triple-quoted multi-line
multi = """Harry is a
good boy"""
print(repr(multi))
# 'Harry is a\\ngood boy'

# Accidental newline bug
bad = '''Hello
'''
print(len(bad))  # 6, not 5 — the newline is a real character
```

### Common Pitfalls / "Gotchas"

| Pitfall | Example | Result |
|---------|---------|--------|
| Accidental newlines in triple-quoted strings | `'''Hello'''` with Enter after Hello | String contains `\n`, silently changing its value |
| Quote escaping | `'It\'s fine'` vs `"It's fine"` | Choosing the right delimiter avoids backslash noise |
| Triple quotes are NOT "better" | Using `'''Hello'''` for a single-line string | Works, but uses more memory than `'Hello'` and may hide bugs |

### Key Insight
Always use the minimal delimiter that satisfies the string's content. Reserve triple quotes for genuine multi-line literals or docstrings.

---

## Unit 2 — Positive Indexing and IndexError

### Core Concept
Strings are **ordered sequences** of characters. Each character can be accessed by its **position** (index) in the string. In Python, indexing is **zero-based**: the first character is at index `0`, the second at `1`, and so on. Valid indices for a string of length `n` are `0` through `n - 1`. Accessing an index outside this range raises `IndexError`.

### What's Actually Happening

**1. Zero-based indexing rationale**
Python follows C-style zero-based indexing. For `"Harry"` (length 5):

```
Characters:  H   a   r   r   y
Indices:     0   1   2   3   4
```

Valid range: `0 <= i < n` (half-open interval).

**2. CPython bytecode for indexing**
`name[0]` compiles to:

```
LOAD_NAME    0 (name)
LOAD_CONST   0 (0)
BINARY_SUBSCR
```

`BINARY_SUBSCR` performs sequence subscription:
1. Checks if the index is within bounds
2. Computes the byte offset in the internal buffer
3. Returns a new `str` object of length 1

**3. IndexError mechanism**
If the index is out of range, CPython raises `IndexError: string index out of range`. This is implemented in C in `PyUnicode_Substring` — the bounds check occurs at the C level before any character data is accessed.

**4. Memory layout insight**
In CPython, a `str` object contains:
- Reference count
- Type pointer
- Length
- Pointer to character data

Index `i` means "character `i`", not "byte `i`". Python strings are sequences of **Unicode code points**, not raw bytes. For ASCII characters (U+0000–U+007F), each character is 1 byte in the compact representation. For multi-byte characters, the internal buffer adjusts accordingly.

### Why It Matters

- **Off-by-one bugs**: `len("abc") = 3`, max valid index = `2`. This is the #1 beginner bug.
- **Performance**: String indexing is O(1) — direct pointer arithmetic on the internal character array.
- **Immutability side-effect**: `name[0]` returns a **new** one-character string object, not a reference to the original character. You cannot assign to `name[0]`.

### Minimal Executable Examples

```python
name = "Harry"
print(name[0])   # H
print(name[4])   # y
print(name[5])   # IndexError: string index out of range

# Safe access with len()
print(f"Length: {len(name)}")
print(f"Last valid index: {len(name) - 1}")
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Result |
|---------|---------|--------|
| Index equals length | `"abc"[3]` | `IndexError` |
| Assuming byte index | `"é"[0]` | Returns `'é'` — indexes by Unicode character, not byte |
| Negative index treated as positive | `"abc"[-1]` if not understood | Should be `IndexError` if out of negative range |

### Key Insight
A string of length `n` has exactly `n` valid indices, numbered `0` to `n-1`. Always use `len(s) - 1` to find the last positive index.

---

## Unit 3 — Negative Indices and Conversion Math

### Core Concept
Python supports **negative indices** as a convenient way to count from the end of a sequence. The normalization formula is:

```
positive_index = len(string) + negative_index
```

For a string of length `n`, valid negative indices are `-n` through `-1`:
- `-1` → last character
- `-2` → second-to-last character
- ...
- `-n` → first character

### What's Actually Happening

**1. Negative index normalization at the C level**

In CPython, `BINARY_SUBSCR` for strings normalizes negative indices before bounds checking. The C code in `builtin_subscript` effectively does:

```c
if (index < 0) {
    index += Py_SIZE(op);  // Py_SIZE returns the string length
}
```

By the time the actual character access occurs, negative indices have already been converted to their positive equivalents internally. There is zero runtime overhead — it's a single integer addition.

**2. The mathematical model**

For `name = "Harry"` (length = 5):

| Negative Index | Calculation | Positive Equivalent | Character |
|----------------|-------------|---------------------|-----------|
| `-1` | `5 + (-1)` | `4` | `'y'` |
| `-2` | `5 + (-2)` | `3` | `'r'` |
| `-3` | `5 + (-3)` | `2` | `'r'` |
| `-4` | `5 + (-4)` | `1` | `'a'` |
| `-5` | `5 + (-5)` | `0` | `'H'` |
| `-6` | `5 + (-6)` | `-1` | `IndexError` (after normalization, still out of range) |

The bounds check still applies after normalization: valid positive range is `0 <= index < n`.

**3. Bytecode verification**

Both `name[-1]` and `name[4]` compile to the same underlying result. The negative constant `-1` is loaded onto the stack, then normalized inside `BINARY_SUBSCR`:

```
 1           0 LOAD_NAME                0 (name)
              2 LOAD_CONST               0 (-1)
              4 BINARY_SUBSCR
              6 RETURN_VALUE
```

The `-1` constant is pushed; `BINARY_SUBSCR` performs `len(name) + (-1)` internally.

### Why It Matters

- **Reverse traversal**: `for i in range(-1, -len(s)-1, -1)` iterates backward without computing positive indices.
- **Idiomatic Python**: `s[-1]` is the canonical way to get the last element; `s[len(s)-1]` is verbose.
- **Memory/performance**: No additional memory is used. Negative index conversion is O(1) arithmetic.

### Minimal Executable Examples

```python
name = "Harry"
length = len(name)  # 5

# Manual conversion
print(name[-1])         # y
print(name[length - 1]) # y — same result

# Edge cases
print(name[-5])  # H (first char)
print(name[-6])  # IndexError

# Negative indexing in slices
print(name[-3:])  # 'rry' — from index 2 to end
print(name[:-2])  # 'Har' — from start to index -3 (exclusive)
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Out-of-range negative | `"abc"[-4]` | `IndexError` — same as positive out-of-range |
| Confusing slice boundaries | `s[-3:]` vs `s[:-3]` | `-3:` includes from index 2 onward; `[:-3]` excludes last 3 chars |
| Length changes | Modifying string with concatenation changes all index math | Strings are immutable; create new objects |

### Key Insight
Negative indices are purely syntactic sugar. The CPython runtime normalizes them to positive indices internally via `len(string) + negative_index` before any bounds check or character access. There is zero runtime overhead.

---

**End of Lecture 19 — Strings in Python**

All 3 units documented. Ready for Quiz 2: Strings and the remaining exercises in Section 4.