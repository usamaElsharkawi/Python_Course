# Lecture 34 — Sets and Set Methods

**Units covered**: 1. What sets are & creation, 2. Set methods
(`add`, `remove`, `discard`, `pop`), 3. Set operations
(`union`, `intersection`, and friends), 4. Why sets behave this way:
the hash table

---

## Unit 1 — What Sets Are & Creation

### Core Concept
A set is an **unordered, unique collection** — the mathematical notion of
"well-defined objects with no repeats." Any element added twice is stored
only once. Creation uses curly braces:
```python
s = {32, 32, 11}          # two 32s collapse to one
print(s, type(s))         # a set; class 'set'
```
The immediate discovery: **`s[0]` fails**
```
TypeError: 'set' object is not subscriptable
```
Why? There is no order — no `s0`, `s1`, `s2`. A set is a *basket*, not a
sequence: Python stores elements "in random order," and insertion order is
not maintained.

### What's Actually Happening
- **Bytecode**: `{32, 32, 11}` compiles to `BUILD_SET 0` +
  `LOAD_CONST frozenset({...})` + `SET_UPDATE` — the compiler bakes the
  constant elements as an *immutable* frozenset, then copies them into a
  fresh mutable set. Same constant-sharing trick as tuples, with a mutable
  copy-out like lists.
- **`{}` is a dict, not an empty set!** The empty set must be written
  `set()`. This is a deliberate disambiguation — one syntax can't be both.
- **Duplicates are physically impossible**, not merely "ignored":
  `add`/literal construction probes the hash table for an *equal* element
  before inserting, so the second `32` never gets a slot.
- **Elements must be hashable**: `{[1, 2]}` →
  `TypeError: cannot use 'list' as a set element (unhashable type: 'list')`
  — mutable objects can't be set members (Lecture 31 Unit 3's hashability
  rule, enforced at insertion).

---

## Unit 2 — Set Methods: `add`, `remove`, `discard`, `pop`

### Core Concept
- `s.add(32)` — adds if not present (adding a duplicate silently does
  nothing)
- `s.remove(x)` — removes; **raises `KeyError` if x is not present**
- `s.discard(x)` — removes **only if present**, silent otherwise — the
  "safe remove"
- `s.pop()` — removes an **arbitrary** element (rarely useful)

### What's Actually Happening
- `remove(99)` on `{1, 2, 3}` → `KeyError: 99` — note: **KeyError**, the
  dict-family exception, because sets are hash tables like dicts (not
  IndexError — no indices exist!)
- `discard` = same lookup, missing branch returns quietly
- `add` of a duplicate computes the hash, finds the equal element already
  occupying a slot, and returns — **no error, no second copy**
- `pop` scans the table from slot 0 and removes the first occupied slot →
  which element that is depends on hash values, not on you. Empty set →
  `KeyError: 'pop from an empty set'`
- These are the only four mutators — there is **no `insert` and no
  `append`** (no positions exist), and unlike lists there's no
  `sort`/`reverse` (no order to exploit)

---

## Unit 3 — Set Operations: `union`, `intersection`, and friends

### Core Concept
With `A = {22, 2, 55, 1}` and `B = {2, 55, 1, 99}`:
- **Union** `A | B` (or `A.union(B)`) → every element from both, duplicates
  collapse: `{1, 2, 22, 55, 99}`
- **Intersection** `A & B` (or `A.intersection(B)`) → only elements in
  **both**: `{1, 2, 55}`
- The lecture also mentions **difference** and notes there's a full
  mathematical toolkit

### What's Actually Happening
- **Operators call the C slot directly; methods are the general form.**
  `A | B` requires both operands be sets; `A.union(B)` accepts **any
  iterable** (`A.union([1, 2])` works) — same dual-syntax split as
  `+`/`.extend()` in Lecture 32.
- Operations come in **binary (new set)** and **in-place (`|=`, `&=`)** forms
  — the in-place ones mutate the left operand (aliasing applies again!).
- The complete relation algebra Python provides:

| Operation | Operator | Method | Result (A={22,2,55,1}, B={2,55,1,99}) |
|---|---|---|---|
| Union | `A \| B` | `union` | `{1, 2, 22, 55, 99}` |
| Intersection | `A & B` | `intersection` | `{1, 2, 55}` |
| Difference | `A - B` | `difference` | `{22}` |
| Symmetric difference | `A ^ B` | `symmetric_difference` | `{22, 99}` |
| Subset / superset | `<=`, `>=` | `issubset`, `issuperset` | bool |

- **Implementation asymmetry worth knowing**: `&` iterates the *smaller*
  set and probes membership in the larger — O(min(n, m)) — while `|` and
  `-` build a new table of combined size.

---

## Unit 4 — Why Sets Behave This Way: the Hash Table

### Core Concept
"Unordered, unique, unsubscriptable, arbitrary pop" isn't four rules — it's
one data structure: the **hash table**.

### What's Actually Happening
1. **A set is a hash table of keys** (a dict with the values deleted).
   `PySetObject` keeps an array of slots; a slot index is computed as
   `hash(element) & mask` where `mask = table_size - 1` (table size is
   always a power of 2).
2. **Adding** = hash the element, probe for a free slot (open addressing, up
   to 9 linear probes then a "perturb" jump), insert if free, **no-op if an
   equal key is already there** — that's the dedup mechanism and the O(1)
   `add`.
3. **Membership testing is one hash + a few probes** — `x in s` is O(1)
   regardless of set size. On a 1,000,000-element list, the same test is
   O(n). *This* is why you use sets.
4. **"Unordered" means slot order, and slot order is hash order.** For small
   ints, `hash(n) == n`, so they land near their own value —
   `{32, 32, 11}` may *look* vaguely sorted. For strings, hashes are
   **randomized per process** (`PYTHONHASHSEED`), so iteration order can
   change between runs:

```
run 1: {'banana', 'cherry', 'apple'}
run 2: {'apple', 'cherry', 'banana'}
run 3: {'cherry', 'banana', 'apple'}
```

5. **`pop` returns "the first occupied slot,"** i.e. the first surviving
   probe target — deterministic for a given table state, arbitrary from your
   perspective.
6. **Hashable elements only** (from Unit 1): `1 == 1.0 == True` means
   `{1, 1.0, True}` is a **single-element set** — same unification rule as
   `list.remove` from Lecture 32 Unit 2.
7. **`frozenset`** is the immutable sibling: unchangeable, therefore
   **hashable**, therefore usable as a set member or dict key — exactly the
   tuple-to-list relationship.

### Why It Matters
- Never iterate a set in an order-dependent way, never index it — the
  TypeError is Python protecting you from a promise the type can't make.
- Use sets for **membership-heavy** work (de-duplication, "seen?" filters,
  intersections of IDs) and lists/tuples when order matters.
- `PYTHONHASHSEED` randomization is also a security feature (prevents
  hash-collision DoS attacks), not a bug.

### Minimal Executable Example
```python
# Creation, dedup, and the {} trap
s = {32, 32, 11}
print(s, type(s))                    # duplicates collapsed
print(type({}))                      # <class 'dict'> — empty set is set()

try:
    s[0]
except TypeError as e:
    print("TypeError -", e)          # 'set' object is not subscriptable

try:
    {[1, 2]}
except TypeError as e:
    print("TypeError -", e)          # cannot use 'list' as a set element

# Methods
t = {1, 2, 3}
t.add(32); t.add(3)                  # second add: silent no-op
print(t)
t.remove(1)                          # KeyError if missing
t.discard(99)                        # silent
popped = t.pop()                     # arbitrary element

# Operations
A = {22, 2, 55, 1}
B = {2, 55, 1, 99}
print(A | B)     # union          {1, 2, 22, 55, 99}
print(A & B)     # intersection   {1, 2, 55}
print(A - B)     # difference     {22}
print(A ^ B)     # sym. diff      {22, 99}
print(A.union([7, 8]))             # methods accept any iterable

# O(1) membership vs list O(n)
big_set = set(range(1000000))
print(999999 in big_set)            # True — one probe

# Equality unification
print({1, 1.0, True})               # {1}
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| `{}` for empty set | `s = {}; s.add(1)` | `AttributeError` — that's a **dict**; use `set()` |
| Any indexing | `s[0]`, `s[1:2]` | `TypeError: 'set' object is not subscriptable` |
| Mutable members | `{[1], {2:3}}` | `TypeError` — unhashable; use `frozenset` or tuples |
| Reliance on iteration order | `list(s)[0]` as "the first element" | Truly arbitrary — and varies per run for strings |
| `remove` vs `discard` | `s.remove(x)` on maybe-missing | `KeyError` crash risk — `discard` when unsure |

### Key Insight
A set is a **dict without values**: hash-table storage where lookup is
O(1), duplicates are impossible by construction, order is whatever the hash
function produces (randomized for strings, per-process), and only hashable
objects may enter. Every set behavior — not subscriptable, arbitrary `pop`,
`KeyError` on `remove`, dedup, the math operators — falls out of that one
design.

---

**End of Lecture 34 — Sets and Set Methods**

All 4 units documented. Ready for Lecture 35 (Dictionaries).
