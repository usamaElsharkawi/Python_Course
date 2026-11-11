# Lecture 35 — Dictionaries and Dictionary Methods

**Units covered**: 1. What dictionaries are & fast lookup,
2. Keys, values & the hashability rule, 3. Mutating via assignment,
4. Dictionary methods, 5. Dictionary comprehensions & when to use which

---

## Unit 1 — What Dictionaries Are & Fast Lookup

### Core Concept
Dictionaries store **key-value pairs** and allow fast lookups — like mapping
names to marks:
```python
marks = {"Harry": 34, "Jack": 45, "Lilly": 94}
print(marks)        # the dictionary printed
print(type(marks))  # <class 'dict'>
```
The value for a key is fetched with square brackets:
```python
print(marks["Lilly"])   # 94
```

### What's Actually Happening
- **Key-value means pure mapping**: left side = **key** (Harry/Jack/Lilly),
  right side = **value** (34/45/94). One key → one value, like a real
  dictionary: word → definition.
- **Bytecode**: `{"Harry": 34, "Jack": 45}` compiles to pushing pairs +
  `BUILD_MAP 2` — pairs built at runtime (unlike constant
  tuples/frozensets, because dicts are mutable and must be fresh copies).
- **A dict is the same hash table as a set** (Lecture 34 Unit 4) — but each
  key slot now carries a value pointer: `hash(key) & mask` → slot → compare
  key → return value. That's why "dictionary lookup is very, very fast" —
  O(1), no iteration, unlike scanning a list.
- **Insertion-ordered since Python 3.7** (guaranteed by the language spec):
  iteration follows insertion order — the one thing dicts have that sets
  lack.
- Memory layout (3.6+ "compact dict"): a sparse **indices array**
  (hash → position) plus a dense **entries array** (key hash, key, value
  triples) — keeps the table cache-friendly and insertion order free.

---

## Unit 2 — Keys, Values, and the Hashability Rule

### Core Concept
Any data type can be a key or a value — **but keys must be hashable**:
Python must be able to hash the key internally. Strings, integers, and
tuples are hashable; **lists are not**, so no list keys.

### What's Actually Happening
```python
marks = {"Harry": 34, 1: "int key", (1, 2): "tuple key"}   # all fine
marks[[1, 2]] = "x"
# TypeError: cannot use 'list' as a dict key (unhashable type: 'list')
```
- **Why hashable?** The slot is found by `hash(key)`. A mutable key could
  change after insertion → its hash changes → the entry becomes unfindable →
  the table silently corrupts. Immutability is a correctness requirement,
  not style.
- **Tuple keys are conditionally hashable** — `(1, 2)` works, but
  `(1, [2])` fails because the tuple's hash incorporates its contents. Same
  rule as Lecture 33's "immutable shell, mutable contents."
- **Values are unrestricted** — a value can be a list, dict, set, anything,
  because values are never hashed; they just sit in the slot.
- **Equality unification applies again** (Lectures 32/34): with
  `d[1] = "a"` then `d[True] = "b"`, keys are identified by `==` + hash, so
  `True == 1` means ONE entry — the key stays `1`, the value is replaced:
```python
d = {}
d[1] = "a"
d[True] = "b"
print(d)               # {1: 'b'} — same key, value replaced
```
- **Missing keys raise, loudly**:
```python
marks["Lily"]
# KeyError: 'Lily'      ← prints the offending key — a precise debugging signal
```
The safe non-raising sibling is `.get()` (Unit 4).

---

## Unit 3 — Mutating a Dictionary: Update via Assignment

### Core Concept
You can change a value by assigning through the key:
```python
marks["Harry"] = 3        # was 34, now 3
print(marks)              # Harry's value updated in place
```
Access, modify, update — all allowed. Dicts are mutable (unlike tuples).

### What's Actually Happening
- **Assignment does double duty**: if the key exists → value replaced (same
  entry); if it doesn't → **new entry inserted**. There is no separate
  `insert` method because `=` covers both cases.
- **Bytecode**: `marks["Harry"] = 3` is the same `STORE_SUBSCR` from
  Lecture 31 Unit 3 — but a dict STORE_SUBSCR hashes the key and probes,
  instead of writing a fixed array slot.
- **Values are unrestricted mutability**: the value can be a list/dict that
  you mutate freely, because values are never hashed:
```python
nested = {"a": [1, 2]}
nested["a"].append(3)          # {'a': [1, 2, 3]} — no complaint
```
- **Keys are pinned**: you may never change a key object in place — that
  would break its hash slot (Unit 2). Key replacement = delete old entry +
  insert new one.

---

## Unit 4 — Dictionary Methods

### Core Concept
- `marks.keys()` → all keys: `Harry, Jack, Lily`
- `marks.values()` → all values: `34, 45, 94`
- `marks.pop(key)` → removes that key (pops `Lily` → only Harry and Jack
  left)
- `marks.clear()` → empties the dictionary
- The lecture closes by listing more to explore: `get`, `items`,
  `popitem`, `setdefault` — "run `marks.` and try them"

### What's Actually Happening

**1. `keys()`, `values()`, `items()` return VIEWS, not lists**
```python
ks = marks.keys()
marks["New"] = 50
print(list(ks))        # includes 'New' — the view is LIVE
```
A view is a window onto the dict's internal tables — it reflects
insertions/deletions automatically, iterates in insertion order, and
supports set-like operations (`keys() & other.keys()`). Call `list()` to
snapshot. `items()` yields `(key, value)` **tuples** — which is why
tuple-unpacking from Lecture 33 works:
```python
for name, grade in marks.items(): ...
```

**2. Removal trio: `pop`, `popitem`, `clear`**
- `pop(key)` → removes the entry and **returns its value** (same contract as
  list.pop); missing key → `KeyError`
- `popitem()` → removes and returns the **last inserted** pair (LIFO, 3.7+);
  empty dict → `KeyError: 'pop from an empty dict'`
- `clear()` → removes all entries in one operation

**3. Non-raising lookups: `get` and `setdefault`**
```python
d.get("missing")            # None
d.get("missing", "DEFAULT") # 'DEFAULT'
d.setdefault("k", [])       # returns existing OR inserts the default AND returns it
```
`setdefault` is the classic grouping idiom:
`groups.setdefault(key, []).append(item)` — "get me the bucket, and create
it if this is the first item." It returns the value either way, so it
chains.

**4. Why so few mutators, same story as sets**
The dict is a hash table: insertion/removal are slot operations (probe,
write, tombstone), so there's no position-based API — no `insert`, no
index-based `remove`. The method surface mirrors the structure.

---

## Unit 5 — Dictionary Comprehensions & When to Use Which Structure

### Core Concept
Dict comprehensions mirror list comprehensions (Lecture 32 Unit 4) — key and
value expressions before the `for`:
```python
table_of_five = {i: 5 * i for i in range(1, 11)}
# {1: 5, 2: 10, ..., 10: 50}
squares = {i: i * i for i in range(6)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
```
And the section's closing decision guide — when to use which:

| Structure | Use when | Because | Examples from the lecture |
|---|---|---|---|
| **list** | ordered **and** mutable | keeps order, insert/append anywhere | sequences, dynamic data (first-come-first-store) |
| **tuple** | ordered but **immutable** | safe fixed records; usable as dict keys | coordinates, config rows, hashable composite keys |
| **set** | **unordered + unique** | dedup, O(1) membership, math operations | removing duplicates, ID intersections |
| **dict** | **key → value** mapping | O(1) lookup by key, structured data | names→marks, ages by name, JSON-like records |

The lecture's emphasis: dictionary lookup beats iterating a list —
`marks["Lilly"]` is one hash probe; finding "Lilly" in a list of names is
O(n) scanning.

### What's Actually Happening
- **Comprehension bytecode**: `{i: 5*i for i in range(1, 11)}` compiles to
  `BUILD_MAP 0` + `MAP_ADD` (dict's analog of `LIST_APPEND`) with the same
  PEP 709 inlining and scoped loop variable as list comprehensions — key
  expression and value expression are both evaluated per iteration.
- **Duplicate keys in a comprehension silently keep the last value** —
  collisions don't error, they overwrite.
- Order note: the resulting dict is in **key-insertion order**, which here
  equals `range` order — deterministic, unlike sets.

### Minimal Executable Example
```python
# Creation and lookup
marks = {"Harry": 34, "Jack": 45, "Lilly": 94}
print(marks["Lilly"])                 # 94

# Key rules
marks[1] = "int key OK"
marks[(1, 2)] = "tuple key OK"
try:
    marks[[1, 2]] = "list key"
except TypeError as e:
    print("TypeError -", e)           # cannot use 'list' as a dict key

try:
    marks["Lily"]
except KeyError as e:
    print("KeyError -", e)            # 'Lily'

# Mutation
marks["Harry"] = 3                    # update
marks["New"] = 50                     # insert
print(marks)

# Views (live)
ks = marks.keys()
marks["Another"] = 1
print("Another" in ks)                # True — view reflects it
for name, grade in marks.items():
    pass                              # tuple unpacking at work

# get / setdefault
print(marks.get("X"), marks.get("X", 0))     # None 0
groups = {}
groups.setdefault("evens", []).append(2)
print(groups)                          # {'evens': [2]}

# pop / popitem / clear
print(marks.pop("New"))                # 50 — returns value
print(marks.popitem())                 # last inserted pair
print(marks.clear(), marks)            # None {}

# Dict comprehensions
print({i: 5 * i for i in range(1, 11)})   # {1: 5, 2: 10, ..., 10: 50}
print({i: i * i for i in range(6)})       # {0: 0, 1: 1, ..., 5: 25}
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Mutable key | `{[1]: 'x'}` | `TypeError` — keys must be hashable |
| Typo'd key lookup | `marks["Lily"]` | `KeyError` — use `.get()` when key is optional |
| Expecting lists from views | `marks.keys() + ["x"]` | Views aren't lists — `list(marks.keys()) + ["x"]` |
| Assuming `popitem` is random | like set.pop | Dict `popitem` is **LIFO** (last inserted), not arbitrary |
| Mutating keys after insert | key object is a list/tuple-with-list | Table corruption — keys are pinned at insertion |
| `1`/`True`/`1.0` key collision | `d[1]; d[True]` | One entry (`1 == True == 1.0`) — silent overwrite |

### Key Insight
A dict is a **hash table mapping hashable keys to arbitrary values** with
O(1) lookup, guaranteed insertion order, and `=` assignment doing double
duty as insert-or-update. Every quirk — `KeyError` naming the key, live
views, `get`/`setdefault` non-raising variants, LIFO `popitem`,
comprehensions compiling to `MAP_ADD` — follows from "same table as a set,
plus a value column."

---

**End of Lecture 35 — Dictionaries and Dictionary Methods**

All 5 units documented. Ready for Lecture 36 (Practice Set) — and note
Section 6 is complete once lectures 33's remaining units are finished.
