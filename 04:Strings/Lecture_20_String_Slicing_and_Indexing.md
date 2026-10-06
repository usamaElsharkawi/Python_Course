# Lecture 20 — String Slicing and Indexing

**Units covered**: 1. Basic slicing syntax (`s[start:end]`), 2. Negative
indices in slicing, 3. Step slicing and omitting indices

---

## Unit 1 — Basic Slicing Syntax (`s[start:end]`)

### Core Concept
String slicing uses `s[start:end]` to extract a substring from index
`start` up to (but not including) index `end`. The end index is
**exclusive**, meaning the slice goes from `start` to `end-1`, analogous
to Python's `range(start, end)`.

### What's Actually Happening

**1. Slice object and bytecode**
`name[0:2]` compiles to a `slice` object `(0, 2, None)` passed to
`__getitem__`. In CPython, the string's `__getitem__` performs:
- Bounds clamping: if `start < 0`, add `len(s)`; if `end > len(s)`,
  clamp to `len(s)`
- Compute length: `end - start` (after normalization, if positive)
- Allocate a new string buffer and copy characters at indices
  `start, start+1, ..., end-1`

**2. Why exclusive end?**
This avoids ambiguity: for a 5-char string `"Harry"`:
- `s[0:5]` → indices 0,1,2,3,4 → all 5 characters
- `s[0:4]` → indices 0,1,2,3 → first 4 characters
- The exclusive end makes the math consistent:
  `length = end - start` when both are in-bounds

**3. Default values**
- `s[:end]` → `start` defaults to 0
- `s[start:]` → `end` defaults to `len(s)`
- `s[:]` → full copy (both defaults)

### Why It Matters
- **Off-by-one prevention**: Remember `s[0:2]` gives characters at
  indices 0 and 1 only. `len("abc") = 3`, so `s[0:3]` gives all 3
  chars.
- **Chaining & transformations**: `s[::2]` (every other char),
  `s[1::2]` (odd positions), `s[-1::-1]` (reverse from end).
- **Memory**: Slicing creates a **new** immutable string; the original
  is unchanged.

### Minimal Executable Examples

```python
name = "Harry"

# Basic slicing (exclusive end)
print(name[0:2])  # "Ha" — indices 0, 1
print(name[2:4])  # "rr" — indices 2, 3

# Default values
print(name[:3])   # "Har" — start defaults to 0
print(name[2:])   # "ry"  — end defaults to len(name) = 5
print(name[:])    # "Harry" — full copy

# Out-of-range (clamped, not error)
print(name[0:100])  # "Harry" — clamped to length
print(name[-100:0]) # "" — clamped, empty result
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Result |
|---------|---------|--------|
| Confusing inclusive vs exclusive | `"abc"[0:2]` → `"ab"` (stops before index 2) | End is exclusive; use `["0:3"]` for all 3 |
| Negative end index | `"abc"[-1]` — `IndexError` but `"abc"[-1:]` → `"c"` | Negative end works like index conversion |
| Mutable assumption | `s = "abc"; s[0:1] = "x"` — `TypeError` | Strings immutable; slicing returns new string |

### Key Insight
`s[start:end]` yields characters at indices `start, start+1, ...,
end-1`. The end is **exclusive**, mirroring `range()`. Omitted `start`
defaults to 0; omitted `end` defaults to `len(s)`.

---

## Unit 2 — Negative Indices in Slicing (`s[start:end]` with negative
indices)

### Core Concept
String slicing supports negative indices for both `start` and `end`. A
negative index is **normalized** by adding the string length:
`effective_index = len(s) + negative_index`. After normalization, the
same exclusive-end rule applies. Valid negative ranges: `-len(s)` to
`-1` (where `-1` is the last character, `-len(s)` is the first).

### What's Actually Happening

**1. Negative index normalization at the C level**
In CPython's string `__getitem__` / slice path, when a negative index
is encountered:
- `start < 0` → `start = max(0, len(s) + start)` (clamped to 0 if
  underflow)
- `end < 0` → `end = max(0, len(s) + end)` (also clamped to 0 if
  underflow)

After this, the normal exclusive-end rule applies: slice goes from
`start` to `end-1`. The normalization happens in the C-level string
substring logic, typically in `PyUnicode_Substring` or the string
`slice` method internals. After normalization, the slice uses pure
positive indices.

**2. Mathematical model**

For `name = "Harry"` (length = 5):

| Original Slice | Normalized Start | Effective End (exclusive) | Result |
|----------------|-----------------|---------------------------|--------|
| `name[0:2]` | 0 | 2 | "Ha" |
| `name[-2:]` | 5+(-2)=3 | 5 (end default) | "ry" |
| `name[-3:-1]` | 5+(-3)=2 | 5+(-1)=4 | "rr" |
| `name[-5:]` | 5+(-5)=0 | 5 | "Harry" |
| `name[:-2]` | 0 (start default) | 5+(-2)=3 | "Har" |
| `name[2:-1]` | 2 | 5+(-1)=4 | "rr" |

**3. Bytecode verification**

Both `name[-3:-1]` and `name[2:4]` compile to similar slice objects,
differing only in the loaded constants:

```python
>>> import dis
>>> dis.dis("name[-3:-1]")
  1           0 LOAD_NAME                0 (name)
              2 LOAD_CONST               0 (-3)
              4 LOAD_CONST               1 (-1)
              6 BUILD_SLICE              2
              8 BINARY_SUBSCR
             10 RETURN_VALUE
```

### Why It Matters
- **Idiomatic reverse/trim patterns**: `s[:-1]` removes last char;
  `s[-3:]` gets last 3 chars.
- **Reverse traversal**: `s[::-1]` reverses the string entirely.
- **Memory/performance**: No extra memory beyond the new slice string
  object.

### Minimal Executable Examples

```python
name = "Harry"  # length = 5

# Negative start only
print(name[-3:])   # "rry" — start = 5+(-3)=2, end=5 → indices 2,3,4 = "rry"

# Negative end only (exclusive)
print(name[:-2])   # "Har" — end = 5+(-2)=3 → indices 0,1,2 = "Har"

# Both negative
print(name[-3:-1]) # "rr" — start=5+(-3)=2, end=5+(-1)=4 → indices 2,3 = "rr"

# Out-of-range negative (clamped)
print(name[-10:])  # "Harry" — start clamped to 0
print(name[:-10])  # "" — end = 5+(-10) = -3 → clamped to 0, empty slice

# Omitted indices defaults
print(name[:3])    # "Har" — end defaults to 5, so name[0:3]
print(name[2:])    # "ry"  — start=2, end defaults to len=5
print(name[:])     # "Harry" full copy
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| `s[-1:0]` gives empty string | `"abc"[-1:0]` → `""` | After normalization, start (2) > end (0) → empty |
| `s[:-1]` removes last char | `"abc"[:-1]` → `"ab"` | `s[:-1]` is `s[0:len(s)-1]`, strips last char |
| `s[-1]` vs `s[-1:]` | `s[-1]` → last char (single string). `s[-1:]` → also last char | Both work, but `s[-1]` returns a 1-char string |

### Key Insight
Negative slice indices are normalized via `len(s) + negative_index`
before the exclusive-end rule applies. After normalization, the slice
uses pure positive indices; if `start >= end`, the result is an empty
string.

---

## Unit 3 — Step Slicing (`s[start:end:step]`) and Omitting Indices

### Core Concept
String slicing supports an optional `step` parameter:
`s[start:end:step]`. The step controls how many characters to skip
between each selected character:
- `step = 1` (default): every character from start to end-1
- `step > 1`: skip `step-1` characters between each selected one
- `step < 0`: traverse the string backward

Omitting `start` or `end` replaces them with `0` or `len(s)`
respectively.

### What's Actually Happening

**1. Step semantics at the implementation level**
In CPython, `name[0:10:2]` creates a `slice` object `(0, 10, 2)`. The
string's `__getitem__` / slice path iterates:
```
current = start
while (step > 0 and current < end) or (step < 0 and current > end):
    include s[current]
    current += step
```
For negative step, the loop comparison reverses and iteration goes
backward.

**2. The "n minus one" rule**
The instructor says: `step = n` means "skip `n-1` characters".
- `step = 1`: skip 0 characters → every character
- `step = 2`: skip 1 character → every other character
- `step = 3`: skip 2 characters → every third character

This matches the formula: selected indices = `start, start+step,
start+2*step, ...`

**3. Omitting indices defaults**
- `s[:end]` → `start` = 0
- `s[start:]` → `end` = `len(s)`
- `s[:]` → full copy (`start`=0, `end`=len, `step`=1)

### Why It Matters
- **Reverse traversal**: `s[::-1]` reverses the string; `s[::-2]`
  reverses and takes every other character.
- **Efficient subselection**: `s[::2]` extracts even-indexed chars in
  O(1) memory overhead for the slice iteration.
- **Empty slice detection**: `s[start:end:step]` returns `""` if the
  iteration never executes (e.g., `step=1` with `start >= end`).

### Minimal Executable Examples

```python
name = "Harry01234"  # length = 11

# Step = 1 (default) — no skipping
print(name[0:10:1])  # "Harry01234" (0-9)

# Step = 2 — skip 1 character between each
print(name[0:10:2])  # "Hry024" — indices 0,2,4,6,8

# Step = 3 — skip 2 characters between each
print(name[0:10:3])  # "Hr02" — indices 0,3,6,9

# Omitted start/end
print(name[:4])      # "Harry" — start=0, end=4
print(name[4:])      # "01234" — start=4, end=11 (len)
print(name[:])       # full copy

# Negative step — reverse
print(name[::-1])    # "43210yrraH" — full reverse
print(name[::-2])    # "420yrrH" — reverse, take every other char

# Reverse with bounds
print(name[4:0:-1])  # "10y" — from index 4 down to (but not including) 0
print(name[4::-1])   # "10yyrraH" — from 4 down to start

# Edge cases
print(name[5:0:1])   # "" — start > end with positive step → empty
print(name[0:10:-1]) # "" — start < end with negative step → empty
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Empty slice from start > end | `"abc"[2:1]` → `""` | Positive step with start >= end → empty |
| Confusing direction | `"abc"[0:2:-1]` → `""` | Negative step needs start > end to produce output |
| `s[::-1]` vs `s.reverse()` | `"abc"[::-1]` → `"cba"` (new string). `list.reverse()` mutates in-place | Strings immutable; slicing always returns new string |
| Step and bounds interaction | `"abc"[0:10:2]` → `"ac"` | Out-of-range `end` is clamped, step still applied |

### Key Insight
`step` controls the iteration direction and density: `step=k` selects
characters at indices `start, start+k, start+2k, ...` until reaching
`end`. Negative `step` reverses traversal. Omitting `start` or `end`
replaces them with `0` or `len(s)` respectively.

---

**End of Lecture 20 — String Slicing and Indexing**

All 3 units documented. Ready for the next step.