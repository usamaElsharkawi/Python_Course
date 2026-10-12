# Lecture 31 — Introduction to Lists

**Units covered**: 1. Why data structures exist & what a list really is,
2. Indexing, slicing, and the `IndexError` mechanics,
3. Mutability: in-place change vs string immutability

---

## Unit 1 — Why Data Structures Exist & What a List Really Is

### Core Concept
Data structures exist to **store and process data correctly** inside a program.
The motivating problem: you want the marks of five students, but a single
variable holds only one value. You *could* write `marks1, marks2, marks3...` —
but that doesn't scale and gives no way to process them as a group.

A **list** solves this: multiple values under one name, enclosed in square
brackets, separated by commas:
```python
marks = [54, 23, 64, 93, 32]
```
Lists don't require uniform types:
```python
mixed = [43, "hello", False, 4.2]
```
The definition: **lists are ordered, mutable collections of items** — both
words matter:
- **Ordered**: the list always reads `54, 23, 64, 93, 32` in that sequence;
  order is maintained throughout the program.
- **Mutable**: elements can be added, removed, and inserted (Lecture 32
  covers the methods).

### What's Actually Happening

**1. The namespace problem a list solves**
Every name maps → one `PyObject` (via the module `__dict__` or frame locals).
Before lists, N values meant N names, each bound independently. A list is one
`PyObject` containing references to N other objects. One name, N values:

```python
x = 10          # namespace: {"x": PyObject(10)}
marks = [...]   # namespace: {"marks": PyListObject -> [54, 23, 64, 93, 32]}
```

**2. The bytecode: `BUILD_LIST` + `LIST_EXTEND`**
Compiling `marks = [54, 23, 64, 93, 32]` does **not** emit five separate push
instructions (that was Python <= 3.7). In CPython 3.14:

```
LOAD_CONST   1 ((54, 23, 64, 93, 32))   # values baked into the code object as a TUPLE
BUILD_LIST   0
LIST_EXTEND  1
STORE_NAME   marks
```
The literal's values are frozen into `co_consts` as a tuple (the compiler's
preferred immutable constant container), then `LIST_EXTEND` copies those
pointers into a freshly built list. Implication: the constants are shared
across runs, but the list you get each time is a **brand-new object** —
`LIST_EXTEND` copies, so constants can never be mutated in place.

**3. Memory layout: a contiguous array of pointers**
```
marks ──► [ PyListObject: ob_size=5 ]
              └── ob_item: [ptr][ptr][ptr][ptr][ptr]
                              │    │    │    │    │
                              v    v    v    v    v
                            [54] [23] [64] [93] [32]   ← independent int objects
```
Each slot is a **strong reference** (8 bytes). The ints exist as separate
objects; the list only points. "Ordered" is not a remembered promise — it's a
physical consequence of array layout: element 3 always lives at
`ob_item + 3`, deterministically, for the object's entire life (unless mutated).

**4. Why mixed types are legal**
`mixed = [43, "hello", False, 4.2]` builds fine because the list stores
**pointers**, and a pointer doesn't care what it points to:
```python
print(type(mixed))      # <class 'list'>  — always exactly list
print(type(mixed[1]))   # <class 'str'>   — types tracked per-element
```
Each element carries its own type tag in its `PyObject` header. Type errors
can only surface at runtime, element by element. Homogeneous lists keep the
array's cache-friendly behavior and catch mistakes earlier; mixed lists are a
tool, not a default.

**5. "Mutable" preview: same object, changed contents**
String methods build a **new** object (`"ab".upper()` returns a new `"AB"`);
list methods are C functions (`list_append`, `list_insert`, ...) that rewrite
`ob_item`/`ob_size` **in place**:
```python
marks = [54, 23, 64]
i = id(marks)
marks.append(32)
print(id(marks) == i)   # True — SAME object, contents changed
```

### Why It Matters
- One container = one handle: pass `marks` to a function, loop over it, hand
  it to `sum()` — impossible with scattered `marks1...marks5` names.
- The ordered guarantee is what makes indexing, slicing, and deterministic
  iteration coherent — a set (later lecture) offers none of these.
- Mutability is powerful and dangerous: it's why aliasing must be understood
  before Lecture 32's methods (Unit 3 covers it).

### Minimal Executable Example
```python
import dis

# Same bytecode every run, a NEW list object every run
dis.dis(compile("marks = [54, 23, 64, 93, 32]", "<ex>", "exec"))

marks = [54, 23, 64, 93, 32]
mixed = [43, "hello", False, 4.2]

print(marks)                  # [54, 23, 64, 93, 32] — ordered
print(mixed)                  # mixed types are legal
print(type(marks))            # <class 'list'>
print(type(mixed[1]))         # <class 'str'>

# Mutability preview vs string immutability
before = id(marks)
marks.append(99)
print(marks, id(marks) == before)   # True — mutated in place

s = "hello"
sid = id(s)
s.upper()                            # return value DISCARDED
print(s, id(s) == sid)               # hello True — original untouched
```

### Key Insight
A list is one name bound to a **contiguous array of references to
independently-typed objects**. "Ordered" = that array never reorders itself;
"mutable" = the same array object gets rewritten by methods. Every behavior
in the rest of this section — indexing math, slicing, `IndexError`,
insert/remove, copying — follows from these two words in the definition.

---

## Unit 2 — Indexing, Slicing, and the `IndexError` Mechanics

### Core Concept
Elements are accessed by **index**, and counting starts at 0 — true for
lists, strings, and tuples alike:
```python
marks[0]   # 54
marks[2]   # 64
mixed[2]   # False
```
Slicing works exactly like strings:
```python
marks[2:4]   # [64, 93]
```
Indexing past the end raises `IndexError`. `mixed` has indices 0–3
(`43, "hello", False, 4.2`), so `mixed[4]` fails — "index out of bound."

### What's Actually Happening

**1. Subscript bytecode (3.14): `BINARY_OP 26 ([])`**
In this CPython version, `lst[i]` is compiled as the subscript form of
`BINARY_OP` (older versions used `BINARY_SUBSCR`). For a slice, the compiler
bakes a `slice(2, 4, None)` **object** into `co_consts` — bounds are never
computed at compile time; a slice object is built and handed to the same
operator:
```
LOAD_NAME marks; LOAD_SMALL_INT 2; BINARY_OP 26 ([])      # marks[2]
LOAD_NAME marks; LOAD_CONST slice(2, 4, None); BINARY_OP 26 ([])   # marks[2:4]
```

**2. The C path: `list_subscript`**
`lst[i]` calls `PyObject_GetItem` → `list_subscript`, which branches on the
key's type:
- **Integer index** (`PyIndex_Check`): negative values are normalized
  (`i += Py_SIZE(self)`), then `list_item` range-checks
  `0 <= i < ob_size`. On success it returns `ob_item[i]` with the refcount
  **incremented**; on failure it raises `IndexError("list index out of
  range")` from C.
- **Slice key**: `PySlice_Unpack` + `PySlice_AdjustIndices` resolve
  defaults (`start=0`, `stop=len`, `step=1`), then a **new list object** is
  allocated and the selected pointers are copied (each incref'd).

**3. O(1) by pointer arithmetic**
`ob_item[i]` is direct C array indexing — no scanning. This is why the
lecture says indexing behaves "just like strings": both are sequences backed
by contiguous arrays implementing the same `sq_item` protocol. (Contrast:
the `.index()` *method* in Lecture 32 is an O(n) value search — different
operation entirely.)

**4. `IndexError` anatomy**
- Class: `IndexError`, a subclass of `LookupError` — raised at **runtime**,
  from C code, not at parse time.
- Message is type-specific: `"list index out of range"` (the lecture's
  comment "index out of bound" is the concept; Python's actual wording is
  "out of range").
- The off-by-one: valid indices are `0 .. len-1`. `mixed[4]` fails because
  index 4 would be the *fifth* element, and `len(mixed) == 4`.

**5. The key asymmetry: indexing is strict, slicing is forgiving**
Out-of-range indices error, but out-of-range **slice** bounds are clipped,
not errors:
```python
marks[99]      # IndexError
marks[2:99]    # [64, 93, 32] — stop silently clamped to len
marks[-99:2]   # [54, 23]     — start clamped to 0
```
This is deliberate: slicing exists for bulk data processing (chunking,
windowing) where boundary checks would be noise; indexing is a precise
"give me exactly this slot" demand.

**6. Slices are shallow**
`marks[2:4]` returns a new list object — mutating the result doesn't touch
the original and vice versa — but the *element pointers* are shared. (Deep
consequences when elements are themselves mutable: a later unit.)

### Minimal Executable Example
```python
marks = [54, 23, 64, 93, 32]
mixed = [43, "hello", False, 4.2]

print(marks[0], marks[2])     # 54 64
print(mixed[2])               # False

print(marks[2:4])             # [64, 93]
print(marks[-1])              # 32 — negative index (normalized in list_subscript)

try:
    mixed[4]                  # valid indices are 0..3
except IndexError as e:
    print(type(e).__name__, "-", e)   # IndexError - list index out of range

print(marks[2:99])            # [64, 93, 32] — sliced bounds clip, never error
print(marks[99])              # IndexError — indexed bounds never clip
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Off-by-one | `mixed[len(mixed)]` | Valid range is `0..len-1`; last element is `len-1` or `-1` |
| Expecting slice errors | `marks[2:99]` | Slice bounds are clipped, not errors |
| Lecture comment vs reality | `# index out of bound` | Python's actual message: "list index out of range" |
| `[i]` vs `.index(i)` | `lst.index(5)` | Subscript is O(1) by *position*; `.index()` is an O(n) *value* search |

### Key Insight
Subscripting a list is C-level pointer arithmetic with a bounds check:
fast, exact, and unforgiving for single indices. Slicing reuses the same
operator with a `slice` key that resolves defaults and clamps — forgiving
by design. This strict/forgiving split is core to Python's sequence
protocol, shared by strings, tuples, and lists.

---

## Unit 3 — Mutability: In-Place Change vs. String Immutability

### Core Concept
The lecture stresses the word **mutable** in "ordered mutable collections":
you can change a list — add elements, remove elements, insert in between —
and *the original list itself changes*. The direct contrast is strings, which
are **immutable**: running a string method returns a *new* string, while the
original remains intact.

### What's Actually Happening

**1. `STORE_SUBSCR`: the bytecode of mutation**
`lst[0] = 99` compiles to `LOAD_SMALL_INT 99; LOAD_NAME lst; LOAD_SMALL_INT
0; STORE_SUBSCR`. `STORE_SUBSCR` invokes `list_ass_subscript` in C, which
overwrites slot `ob_item[0]`:
- the new object is **incref'd** and stored in the slot
- the old occupant is **decref'd** (freed if its refcount hits zero)
- `ob_size` is unchanged for an integer key; a *slice* key can resize the
  array and `realloc` it

This slot rewrite *is* what "mutable" means physically — the array
survives, its contents are replaced.

**2. Same identity, new contents**
```python
lst = [1, 2, 3]
before = id(lst)
lst[0] = 99
print(id(lst) == before)   # True — the object never changed; its contents did
```
Refcount bookkeeping is directly observable:
```python
import sys
a = "hello"
lst = [a, 2, 3]
print(sys.getrefcount(a))   # 5 — includes lst[0]
lst[0] = "other"            # decref old, incref new
print(sys.getrefcount(a))   # 4 — the list dropped its reference
```

**3. String immutability is enforced by the type**
```python
s = "hello"
s[0] = "H"     # TypeError: 'str' object does not support item assignment
```
`str` has no item-assignment slot: `"abc".upper()` allocates a *new*
`PyUnicodeObject` instead. That invariant buys:
- **hash stability** → strings work as dict keys and set members
- **safe sharing** / interning → passing a string never exposes it to mutation
- **thread safety** → no locks needed for reads

**4. Lists are unhashable — by design**
```python
hash([1, 2, 3])   # TypeError: unhashable type: 'list'
```
Hashing needs a value that can never change; mutability and stable hashes
are mutually exclusive. (This is why Lecture 35 keys dictionaries with
immutable types — tuples work, lists don't.)

**5. Aliasing: every name sees the mutation**
```python
a = [1, 2, 3]
b = a            # NOT a copy — a second name for the same object
b[0] = 99
print(a)         # [99, 2, 3] — a changed too!
```
And the `+=` preview — the most dangerous consequence, covered properly in
Lecture 32:
```python
x = [1, 2]
y = x
x += [3]
print(x, y, x is y)   # [1, 2, 3] [1, 2, 3] True — y changed through the alias!
```
List `+=` calls `list___iadd__`, which mutates **in place**, so every alias
observes it. String `+=` builds a new object and rebinds the name:
```python
s1 = "ab"
s2 = s1
s2 += "c"
print(s1, s2, s1 is s2)   # ab abc False
```

**6. Why mutator methods "change the original"**
The lecture's phrasing — "you can run certain functions and the original
list will be changed" — is exactly the C-level story: `list.append(obj)`
receives `self`, writes into `ob_item`, and the caller's variable still
points to the *same* (now longer) list. Mutators conventionally **return
`None`**, which is why the classic beginner bug exists:
```python
lst = [1]
lst = lst.append(2)   # lst is now None!
```

### Why It Matters
- Functions receiving a list can mutate the caller's data — surprising
  unless you expect reference semantics
  (`def f(lst): lst.append(...)` changes the caller's list).
- All aliasing bugs in real code trace to this one mechanism.
- Copies (`lst.copy()`, slicing) exist *only* because of mutability.
- Mutability excludes lists from hash-based containers — a design tradeoff,
  not an oversight.

### Minimal Executable Example
```python
import sys

# 1) Mutation in place, identity stable
lst = [1, 2, 3]
before = id(lst)
lst[0] = 99
print(lst, id(lst) == before)          # [99, 2, 3] True

# 2) Refcount bookkeeping on replacement
a = "hello"
lst = [a, 2, 3]
n_before = sys.getrefcount(a)
lst[0] = "other"
print(n_before, sys.getrefcount(a))    # 5 4

# 3) String immutability enforced by the type
s = "hello"
try:
    s[0] = "H"
except TypeError as e:
    print("TypeError -", e)            # 'str' object does not support item assignment

# 4) Lists are unhashable
try:
    hash([1, 2, 3])
except TypeError as e:
    print("TypeError -", e)            # unhashable type: 'list'

# 5) Aliasing vs rebinding
x, y = [1, 2], None
y = x
x += [3]
print(x, y, x is y)                    # [1, 2, 3] [1, 2, 3] True
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Assuming `b = a` copies | `b = a; b[0] = 99` | `a` changes too — aliasing, not copying |
| `+=` through aliases | `x += [3]` with `y = x` | In-place mutation — `y` changes too |
| Capturing a mutator's return | `lst = lst.append(x)` | Mutators return `None` |
| List as dict key | `{[1]: "a"}` | `TypeError: unhashable type: 'list'` |
| Mutating while iterating | `for v in lst: lst.append(v)` | Infinite loop — preview of an iteration trap |

### Key Insight
Mutability means the object's **slots can be rewritten while its identity
stays fixed** — so every name bound to that object observes every change,
and in-place operators like `+=` propagate through all aliases.
Immutability (strings) is the opposite contract: no slot ever changes, which
is what makes strings hashable and safe to share freely. Everything in
Lecture 32's method list is just specialized ways of rewriting those slots.

---

**End of Lecture 31 — Introduction to Lists**

All 3 units documented. Ready for Lecture 32 (List Methods).
