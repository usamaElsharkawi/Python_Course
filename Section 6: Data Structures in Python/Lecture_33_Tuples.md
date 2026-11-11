# Lecture 33 — Tuples and Operations on Tuples

**Units covered**: 1. What tuples are & how creation works,
2. Immutability in practice & the one-element rule,
3. Tuple unpacking,
4. Methods & why tuples

---

## Unit 1 — What Tuples Are & How Creation Works

### Core Concept
Tuples are **ordered but immutable collections** — they cannot be changed
after creation. The motivation: sometimes we *want* a collection that can
never change, to avoid accidental changes leading to disasters in big
programs.

```python
a = (3, 22, 13)
print(a)        # (3, 22, 13) — prints just like a list
print(a[0])     # 3 — indexing works identically to lists
print(a[2])     # 22
```
Very similar to lists — the only difference: immutability.

### What's Actually Happening

**1. The parentheses are a lie — the comma is the tuple**
```python
t = 3, 22, 13
print(type(t))    # <class 'tuple'>
```
Parentheses are optional. What actually creates a tuple is the **comma**.
Parentheses serve double duty as *grouping* operators (`(2 + 3) * 4`), which
is exactly why the one-element gotcha in Unit 2 exists.

**2. Bytecode: the tuple might not even be built at runtime**
`t = (3, 22, 13)` compiles to a **single `LOAD_CONST`**. The entire tuple is
frozen into `co_consts` as a pre-built constant object at compile time — no
`BUILD_TUPLE` instruction runs at all. Contrast with the list literal from
Lecture 31 (BUILD_LIST + LIST_EXTEND, built fresh every execution).

Why the difference? Because a tuple is **immutable**, the compiler can safely
share one canonical constant tuple across every execution of that code. A
list literal can't — any copy handed out could be mutated by user code,
corrupting the constant. This is the first crack in *why tuples are faster*
(Unit 4).

**3. Memory layout: one fixed allocation, no growth machinery**
```
[refcnt][type][ob_size][item0][item1][item2]   ← header + inline array
```
- The element array is **embedded directly in the object block** — one
  allocation of exactly `40 + 8n` bytes, sized at creation, **never resized**
- No over-allocation, no `ob_item` realloc path, no capacity field
- Measured: `(3, 22, 13)` = 72 bytes vs the same list = 88 bytes. The list's
  extra 16 bytes = pre-allocated spare slots the tuple will never waste

**4. Immutability's mechanism: the slot simply doesn't exist**
Lists *implement* `lst[0] = x` (`list_ass_subscript`). Tuples don't even have
it: `sq_ass_item` is NULL, so `a[0] = 99` fails at the type level with:
```
TypeError: 'tuple' object does not support item assignment
```
Same failure mode as strings (Lecture 31 Unit 3) — immutability is enforced
identically: the type object provides no way to rewrite slots. There is no
`tuple_append`, no `tuple_insert`, no `tuple.remove` in C — and that's why
the lecture later finds only **two** methods.

**5. Immutable ≠ frozen contents (preview gotcha)**
The tuple's *slots* can't be re-pointed — but if a slot points to a *mutable*
object, that object still changes:
```python
t = ([1, 2], [3, 4])
t[0].append(99)
print(t)        # ([1, 2, 99], [3, 4]) — tuple "changed"!
```
This bites hardest with **hashability** in Unit 4: a tuple containing a list
is itself unhashable, so it can't be a dict key.

### Why It Matters
- The ordered guarantee is identical to lists (same contiguous array math
  from Lecture 31 Unit 2) — all indexing/slicing knowledge transfers directly.
- The immutability is the *point*: it's a correctness tool, the lecture's
  "disaster prevention" for big programs — a value handed to other code
  physically cannot be modified through the tuple.
- The size difference (72 vs 88) and the constant-sharing bytecode are the
  seeds of the lecture's "tuples are faster" claim.

### Minimal Executable Example
```python
import sys

# Parentheses are optional — the comma makes the tuple
a = (3, 22, 13)
b = 3, 22, 13
print(a == b, type(b))            # True <class 'tuple'>

# Ordered: indexing/slicing exactly like lists
print(a[0], a[2], a[1:])          # 3 22 (22, 13)

# Immutability enforced by the type itself
try:
    a[3] = 32
except TypeError as e:
    print("TypeError -", e)       # 'tuple' object does not support item assignment

# No mutator methods exist at all
print([m for m in dir(a) if not m.startswith('_')])   # count, index only

# Smaller fixed allocation, no spare slots
print(sys.getsizeof(a), sys.getsizeof(list(a)))       # 72 88

# Immutable shell, mutable contents
t = ([1, 2],)
t[0].append(99)
print(t)                          # ([1, 2, 99],)
```

### Key Insight
A tuple is a **fixed-size array embedded in a single allocation, created once
and never resized**, with no slot-assignment path in its C type. That single
design decision produces everything the lecture will discuss: the
`TypeError`, the missing methods, the comma-required syntax, the speed, and
the hashability — all in the next three units.

---

## Unit 2 — Immutability in Practice & the One-Element Rule

### Core Concept
Trying to change a tuple element fails:
```python
a = (3, 22, 13)
a[3] = 32      # TypeError: 'tuple' object does not support item assignment
```
(Note: the transcript says `a[3]`, but `a` only has indices 0–2 — the
`TypeError` fires before any index check anyway, because tuple assignment
doesn't exist *at all*.)

And the interview question the lecture flags: **how do you make a tuple with
one element?**
```python
b = (7)        # NOT a tuple!
b = (7,)       # YES a tuple — the comma is required
```

### What's Actually Happening

**1. Why `b = (7)` is not a tuple**
```python
b = (7)
print(type(b))    # <class 'int'>
```
Because parentheses in Python are the **grouping operator** — `(7)` means "the
expression 7, grouped," which is just `7`. No comma, no tuple (Unit 1: the
comma creates the tuple, not the parens).

**2. Why `(7,)` works**
The trailing comma *is* the tuple constructor:
```python
b = (7,)
print(type(b), b)        # <class 'tuple'> (7,)
```
Even without parens: `7,` is also a valid one-element tuple. The compiler sees
a literal tuple in `co_consts` — `(1)` is constant-folded to `1`, but `(1,)`
must remain a `LOAD_CONST` tuple.

**3. The behind-the-scenes reason this exists at all**
Python couldn't make `(x)` a tuple even if it wanted to — it would break
arithmetic grouping:
```python
print((2 + 3) * 4)    # 20 — parens MUST mean grouping for this to work
```
If parentheses alone built tuples, arithmetic grouping would need new syntax.
The comma rule is the resolution: one symbol for both jobs, disambiguated by
the comma.

**4. What the error really tells you**
```
TypeError: 'tuple' object does not support item assignment
```
Same message shape as strings (Lecture 31 Unit 3) — both types simply have
**no item-assignment implementation**. The exception fires *before* the index
is even validated: in CPython, `tuple_subscript` handles reads; there's no
`tuple_ass_subscript` slot at all, so `a[3] = 32` fails at type-check time,
not bounds-check time. That's why even an out-of-range index gives the
assignment `TypeError` rather than `IndexError`.

**5. Single-element tuples are everywhere in practice**
- Function defaults stored as a one-tuple
- Building rows in a loop: `row = (value,)`
- Keeping API arguments uniform (a 1-tuple signals "still a sequence")

**6. The multi-element contrast (for completeness)**
```python
empty = ()          # empty tuple — valid, no comma needed
one   = (7,)        # comma REQUIRED
many  = (7, 22)     # commas naturally present — parens still optional
```

### Why It Matters
- This is the classic interview question the lecture names — you now know
  *why*, not just the rule: parentheses are overloaded, commas construct.
- Miswriting `(7)` creates an int silently — no error, wrong data flowing
  through your program, discovered much later (the exact class of "disaster"
  the lecture motivates tuples for).
- The error message shape is diagnostic: `does not support item assignment`
  means immutable type, and tells you nothing about your index.

### Minimal Executable Example
```python
a = (3, 22, 13)

# Assignment fails — TypeError, not IndexError, even with a bad index
try:
    a[3] = 32
except TypeError as e:
    print("TypeError -", e)     # 'tuple' object does not support item assignment

try:
    a[99] = 1
except TypeError as e:          # still TypeError! Index never checked
    print("TypeError -", e)

# The one-element rule
print(type((7)))                # <class 'int'>   ← grouping, not a tuple
print(type((7,)))               # <class 'tuple'> ← the comma builds it
print(type(7,))                 # <class 'tuple'> ← parens optional too

# Building a single-element tuple from a value
value = 42
row = (value,)
print(row)                      # (42,)

# Empty tuple needs no comma
print(type(()))                 # <class 'tuple'>

# Grouping vs tuple disambiguation
print((2 + 3) * 4)              # 20
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Forgetting the comma | `t = (7)` | Silently an `int`, not a tuple — no error raised |
| Assuming the error is about the index | `a[3] = 32` expecting IndexError | `TypeError` — the index is never checked, assignment doesn't exist |
| Tuple of mutable still mutable | `t = ([1],); t[0].append(2)` | Immutability is shallow — contents can change |
| Trailing comma forgotten in loops | `rows.append((v))` | Appends the raw value, not a 1-tuple |

### Key Insight
Parentheses group; **commas construct**. A tuple only exists where a comma
appears — which is why one-element tuples require the comma, multi-element
tuples can't avoid it, and empty tuples are the lone parens-only exception.
The assignment `TypeError` exists because tuple types expose read paths but
no write paths at all — immutability enforced at the type level, before any
index reasoning.

---
