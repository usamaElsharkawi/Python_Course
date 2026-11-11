# Lecture 32 — List Methods

**Units covered**: 1. The "grow" family: `append`, `insert`, `extend`,
2. The removers: `pop`, `remove`,
3. In-place algorithms: `sort`, `reverse`,
4. List comprehensions

---

## Unit 1 — The "Grow" Family: `append`, `insert`, `extend`

### Core Concept
Three ways to add elements to a list, demonstrated on `marks = [52, 21, 5, 7]`:
- `marks.append(63)` — adds 63 **at the end** → `[52, 21, 5, 7, 63]`
- `marks.insert(1, 77)` — inserts 77 **before index 1** → `[52, 77, 21, 5, 7]`
- `marks.extend(extra_marks)` where `extra_marks = [53, 23, 32]` — appends
  **each element** of another list → `[52, 21, 5, 7, 53, 23, 32]`

The lecture also stresses self-exploration: type `marks.` and the IDE lists
every method available on lists.

### What's Actually Happening

**1. `append` — amortized O(1) thanks to over-allocation**
`list_append` checks capacity first:
- If `ob_size < allocated`: store the pointer at `ob_item[ob_size]`,
  `ob_size++`, incref — **no reallocation at all**
- If full: reallocate with the geometric growth formula
  `new_allocated = newsize + (newsize >> 3) + (newsize < 9 ? 3 : 6)`, then store

The growth is visible in `sys.getsizeof`:
```
[]           → 56   (header, 0 slots)
append(1st)  → 88   → 4 slots   (1 + 0 + 3)
...
append(5th)  → 120  → 8 slots   (5 + 0 + 3)
append(9th)  → 184  → 16 slots  (9 + 1 + 6)
```
Because capacity grows geometrically while appends are linear, **n appends
cost O(n) total** — each individual append is O(1) *amortized* (one in every
~8 pays for a realloc that moves the whole array). `append` **returns
`None`** — the `lst = lst.append(x)` trap from Lecture 31 lives here too.

**2. `insert` — O(n) because of `memmove`**
`list_insert` normalizes the index (negatives wrap, out-of-range clamps),
then uses C `memmove` to shift every slot **after** the insertion point one
to the right, writes the new pointer, and increments `ob_size`. Best case at
the end (`insert(len(l), x)` ≡ `append`), worst case at the front. The
memmove is fast C, but it's still O(n) work:

```
insert(0) on a 1000-element list: ~8.4 µs per call
append    on a 1000-element list: ~0.01 µs per call   (~700x faster)
```

**3. `extend` — the iterator protocol, not a "list-only" method**
`list_extend` calls `PyObject_GetIter(arg)` — so it consumes **any
iterable**: lists, tuples, strings, generators, ranges:
```python
l.extend("ab")                  # [1, 'a', 'b']
l.extend(x*x for x in range(3)) # [1, 0, 1, 4]
```
It also uses the argument's length hint (`__length_hint__`) to resize
**once**, instead of n reallocations. And the equivalence that ties back to
Lecture 31's aliasing demo:

```python
marks += extra_marks      # bytecode: INPLACE_ADD → list___iadd__ → list_extend
marks.extend(extra_marks) # IDENTICAL operation — one is syntax, one is the method
```
`+=` mutates in place, so it propagates through every alias — exactly the
Unit 3 gotcha.

**4. `append` vs `extend`: the nested-list trap**
`append` adds **one** element (the object itself, whatever it is); `extend`
adds each *element of the iterable*:
```python
l = [1]
l.append([2, 3])   # [1, [2, 3]]  — the list became ONE element
l.extend([2, 3])   # [1, 2, 3]    — elements spliced in individually
```

### Why It Matters
- Append-heavy code is fast by design; **insert-at-front-heavy code is slow**
  — use `collections.deque` when you actually need FIFO/LIFO behavior.
- `extend` accepting any iterable means you can splice generators/sets
  without materializing them first.
- The append-vs-extend confusion creates silently wrong nested structures —
  `[[1,2],[3,4]]` when you meant `[1,2,3,4]`.

### Minimal Executable Example
```python
import sys, timeit

marks = [52, 21, 5, 7]
marks.append(63)
print(marks)                     # [52, 21, 5, 7, 63]

marks.insert(1, 77)
print(marks)                     # [52, 77, 21, 5, 7, 63]

extra = [53, 23, 32]
marks.extend(extra)
print(marks)                     # [52, 77, 21, 5, 7, 63, 53, 23, 32]

# append vs extend
l = [1]
l.append([2, 3]);  print(l)      # [1, [2, 3]]
m = [1]
m.extend([2, 3]);  print(m)      # [1, 2, 3]

# extend takes any iterable
g = [1]; g.extend(x*x for x in range(3)); print(g)   # [1, 0, 1, 4]

# += IS extend
a, b = [1], [2]
mem_before = id(a)
a += b
print(a, id(a) == mem_before)    # [1, 2] True — mutated in place

# The O(1) vs O(n) cost
print(timeit.timeit("l.append(1)", "l=[0]*1000", number=100000))
print(timeit.timeit("l.insert(0,1)", "l=[0]*1000", number=100000))
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Capturing append's return | `lst = lst.append(5)` | Returns `None` — list destroyed |
| `append` for splicing | `a.append(b)` for two lists | Creates nested `[x, [y...]]` — use `extend` |
| `insert(0)` in loops | building via `insert(0, x)` | O(n²) overall — append + `reverse`, or `deque` |
| Forgetting `+=` mutates | `a += b` with `c = a` | `c` changes too — in-place extend |

### Key Insight
All three methods just rewrite `ob_item`/`ob_size` with different cost
profiles: `append` is amortized O(1) via over-allocation, `insert` is O(n)
via `memmove`, `extend` is O(k) for k new elements with a single allocation.
They return `None` because they *are* the mutation — the object you called
them on is the result.

---

## Unit 2 — The Removers: `pop` and `remove`

### Core Concept
- `marks.pop()` — the IDE tooltip: *"remove and return item at index;
  defaults to the last element."* The transcript shows `7` removed from
  `[52, 21, 5, 7]`.
- `marks.remove(...)` — the transcript says *"remove the element at an
  index"* — this is a mislabel; `remove` takes a **value**, not an index.

### What's Actually Happening

**1. `pop` — steals a slot, shrinks the tail, RETURNS the value**
`list_pop` in CPython:
- No argument → `i = ob_size - 1` (the last slot). Empty list →
  `IndexError: pop from empty list`
- With an index → negative values wrap, out-of-range →
  `IndexError: pop index out of range`
- The chosen pointer is **ownership-transferred** out of the array (no
  incref — the list hands off its reference), the tail slots are `memmove`d
  left one position, `ob_size` decrements
- The array may even **shrink its allocation** (`list_resize` down-sizes
  when size drops below half of capacity)

Cost profile: `pop()` at the end needs **no memmove** — pure O(1). `pop(0)`
shifts everything: O(n).

This is the only removal method that returns the removed item — the Python
idiom for stacks:
```python
x = lst.pop()        # remove AND use the value in one step
```
`append` + `pop()` together are the entire stack protocol (LIFO).

**2. `remove` — linear search by VALUE, then shift**
`list_remove` does two passes of work:
1. **Scan** `ob_item` left to right comparing each element with
   `PyObject_RichCompare(Py_EQ)` until the first match
2. **Shift** the tail left with `memmove`, decref the removed object,
   `ob_size--`

Two consequences:
- **O(n) always** — even removing the last element requires the full scan
  first.
- Not found → `ValueError: list.remove(x): x not in list` (not IndexError!).
  The exception type *tells you which operation you used*: index-based
  failures raise `IndexError`, value-based failures raise `ValueError`.

**3. Correcting the lecture: `remove` is by value, `pop`/`del` are by index**
```python
l = [1, 2, 3, 2]
l.remove(2)      # [1, 3, 2] — first matching VALUE of 2, not "element at index 2"
```
"Remove the element at index" describes `pop(i)` and the `del` statement.
`del lst[1]` is a third removal path — a *statement*, not a method, backed
by `list_ass_subscript` with a null value (and `del lst[a:b]` removes a
whole slice range):
```python
d = [10, 20, 30]
del d[1]         # [10, 30]
```

**4. The equality trap: value-matching uses `==`, not identity**
Because `1 == 1.0 == True` in Python's numeric tower, `remove` happily
deletes an element that's a *different type but equal value*:
```python
m = [1, 0, True]
m.remove(1)      # [0, True] — removed the int 1 (first == match); True is also == 1
```
If the list were `[True, 1]`, `remove(1)` would remove `True` instead.
Removing "what you see" and "what Python compares" can be different objects.

### Why It Matters
- `pop` returning the value is what makes stack/queue-by-list code natural —
  and why `pop` on an empty list (`IndexError`) is the standard "underflow"
  signal.
- Choosing `remove` when you meant `pop(i)` is a live bug: `lst.remove(2)`
  deletes the *first value equal to 2 anywhere*, not position 2.
- `del` covers index and slice removal that methods don't express well.

### Minimal Executable Example
```python
marks = [52, 21, 5, 7]

last = marks.pop()          # 7 — returned!
print(last, marks)          # 7 [52, 21, 5]

first = marks.pop(0)        # 52 — O(n) memmove
print(first, marks)         # 52 [21, 5]

try:
    [].pop()
except IndexError as e:
    print("IndexError -", e)   # pop from empty list

l = [1, 2, 3, 2]
l.remove(2)
print(l)                       # [1, 3, 2] — first VALUE match only

try:
    l.remove(99)
except ValueError as e:
    print("ValueError -", e)   # list.remove(x): x not in list

m = [1, 0, True]
m.remove(1)
print(m)                       # [0, True] — == matching across types

d = [10, 20, 30]
del d[1]
print(d)                       # [10, 30]
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| `remove` thinking it takes an index | `lst.remove(1)` to delete index 1 | Deletes the first *value equal to 1* anywhere — use `pop(i)` or `del lst[i]` |
| Wrong exception expectation | `try: lst.remove(x)` / `except IndexError` | Raises `ValueError` — index ops raise `IndexError`, value ops raise `ValueError` |
| `pop(0)` in a loop | queue pattern with `pop(0)` | O(n²) overall — use `collections.deque` |
| Equality surprises | `[True, 2].remove(1)` | `True == 1` → removes `True` |

### Key Insight
`pop` and `remove` both shrink `ob_item` with a `memmove`, but they differ
in *what they search by* and *what they give back*: `pop` takes an index, is
O(1) at the end, and **returns** the removed object; `remove` scans by `==`
equality, is always O(n), returns `None`, and signals failure with
`ValueError` while `pop` signals with `IndexError`. `del` is the
statement-level escape hatch for index and slice deletion.

---

## Unit 3 — `sort` and `reverse`: In-Place Algorithms

### Core Concept
From the "try these yourself" list:
- `marks.sort()` — "it will sort it for you" (ascending, numbers or strings)
- `marks.reverse()` — "it will reverse the original list"

Both are emphasized as **in-place**: the original list is rearranged, not a
copy returned.

### What's Actually Happening

**1. TimSort — not quicksort, not bubble sort**
`list.sort()` calls CPython's **Timsort** (Tim Peters' algorithm, since
Python 2.3), a hybrid of **merge sort + insertion sort** engineered for
real-world data:
- Divides the list into short **runs** (natural ascending/descending
  subsequences); descending runs are simply reversed in place (free work on
  nearly-sorted-descending data)
- Sorts short runs with **binary insertion sort**
- Merges runs with a stack-based merge policy that maintains invariants (run
  lengths follow a Fibonacci-like ratio) — bounding merge cost to O(n log n)
  worst case
- Allocates a **temporary buffer** for merging (up to n/2 elements), then
  copies back — that's why sort needs O(n) auxiliary space

The killer property — **stability**: elements that compare equal keep their
original relative order:
```python
students = [("Ali", 85), ("Sara", 85), ("Omar", 90)]
students.sort(key=lambda s: s[1])   # by grade
# Ali still before Sara — stability preserved
```

**2. Best case is already O(n) — the "natural run" detection**
If the list is already sorted (or sorted in reverse), run detection consumes
it in one pass: sorting an already-sorted list is **O(n)**, not O(n log n).
This is why TimSort dominates adaptive sorts on partially-ordered data —
extremely common in practice (logs, timestamps).

**3. `key=` — a completely different cost model**
`key=` applies the function **once per element** (the internal
"decorate-sort-undecorate" pattern), so `key=len` on n strings is O(n) calls
+ O(n log n) comparisons on the results. Without `key=`, every comparison
would call the function. `reverse=True` doesn't re-sort backwards — it
**inverts the comparison** during the same merge pass (still stable, still
one sort).

**4. `reverse()` — swap pointers, in place**
`list_reverse` swaps `ob_item[i] ↔ ob_item[n-1-i]` up to the middle — O(n)
time, O(1) space, **no comparisons**. Contrast: the **`reversed()`** built-in
returns a *lazy iterator* and leaves the list untouched:
```python
lst.reverse()          # mutates in place, returns None
rev = reversed(lst)    # new lazy iterator, original untouched
```

**5. `sort` vs `sorted`**
`sorted(lst)` is the built-in that returns a **new sorted list** —
implemented by copying the list, then calling the exact same `list.sort()`
on the copy. Same algorithm, different mutation contract. Strings get
`sorted()` but no `.sort()` (immutability again — Lecture 31 Unit 3).

### Why It Matters
- Stability is the reason `key=` sorts compose cleanly and why
  database-style "ORDER BY multiple fields" maps to one sort with a tuple
  key.
- TimSort's adaptivity means *don't* pre-shuffle or "help" the sort — data
  with natural order sorts faster.
- `sort` being in-place + returning `None` repeats the mutator contract;
  `lst = lst.sort()` sets `lst` to `None`.

### Minimal Executable Example
```python
marks = [52, 21, 5, 7]
marks.sort()
print(marks)                    # [5, 7, 21, 52]

marks.reverse()
print(marks)                    # [52, 21, 7, 5]

# Stability demo
students = [("Ali", 85), ("Sara", 85), ("Omar", 90)]
students.sort(key=lambda s: s[1])
print(students)                 # Ali before Sara — equal keys preserve input order

# reverse=True is still ONE pass and still stable
data = [("a", 1), ("b", 1), ("c", 0)]
data.sort(key=lambda x: x[1], reverse=True)
print(data)                     # [('a', 1), ('b', 1), ('c', 0)]

# reversed() is lazy and non-mutating
lst = [1, 2, 3]
r = reversed(lst)
print(lst, list(r), next(reversed(lst)))   # [1, 2, 3] [3, 2, 1] 3

# sorted() = copy + list.sort; strings have no .sort()
print(sorted("banana"))         # ['a', 'a', 'a', 'b', 'n', 'n']
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Capturing sort's return | `lst = lst.sort()` | Returns `None` — list lost |
| Assuming sort is unstable | relying on interleaved orderings | TimSort **is** stable — cross-call key differences break expectations, not sort itself |
| Sorting mixed types | `[1, "a"].sort()` | `TypeError: '<' not supported` — comparisons must be total |
| `reverse()` vs `reversed()` | expecting `reverse()` to return a list | In-place, returns `None`; use `reversed()` for a lazy iterator |
| `reverse=True` after sorting | `lst.sort(); lst.reverse()` | Two passes; use `sort(reverse=True)` |

### Key Insight
`sort()` is **adaptive, stable TimSort** — merge sort's worst-case
guarantee plus insertion sort's speed on short runs, with free reversing of
descending runs and O(n) on already-ordered data. `reverse()` is just
pointer swaps. Both mutate; their copy-returning siblings are `sorted()` and
`reversed()`.

---

## Unit 4 — List Comprehensions

### Core Concept
The problem: build the table of 5. The verbose way:
```python
table = []
for i in range(1, 11):
    table.append(5 * i)
print(table)          # [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
```
The shortcut — **list comprehension**:
```python
table = [5 * i for i in range(1, 11)]
```
Same output, one line. Rule of thumb: *single-line loop body → comprehension
is fine and readable*. The acknowledged counter-argument: the loop form
scales when you need more statements in the body.

### What's Actually Happening

**1. The comprehension has its own scope — the variable doesn't leak**
```python
exec("t = [i for i in range(3)]")
print(i)    # NameError: name 'i' is not defined
```
Since Python 3, the loop variable is scoped to the comprehension. (In
Python 2 it *did* leak — a famous wart.) The mechanism changed in 3.12
(PEP 709): comprehensions are **inlined** into the enclosing code object
instead of compiled as a hidden `<listcomp>` function, and isolation is now
done by save/restore bytecodes:

```
GET_ITER
LOAD_FAST_AND_CLEAR  0 (i)     # save any outer 'i', clear the slot
...
FOR_ITER, STORE_FAST i, LOAD_FAST_BORROW i, BINARY_OP 5 (*)
LIST_APPEND          2        # append WITHOUT a method call
...
STORE_FAST           0 (i)    # restore the outer 'i' afterward
```

**2. `LIST_APPEND` is the performance story**
In the equivalent loop, `table.append(...)` compiles to a load +
`LOAD_METHOD append` + `CALL`. The comprehension replaces that entire call
sequence with the single `LIST_APPEND` opcode — a direct C append onto the
list being built. Measured (100k elements × 100 runs):

```
append loop:   0.372 s
comprehension: 0.277 s   (~25% faster)
```
The speedup comes from *removed overhead per iteration* (no attribute
lookup, no call frame setup, fast local slots), not from a fundamentally
different algorithm — it's the same O(n) build.

**3. Two optional clauses complete the syntax**
- **Filter** — `if` after the loop: `[x for x in lst if x % 2 == 0]` (skips
  elements *before* the expression runs)
- **Conditional expression** — `if/else` before the loop:
  `[x if x >= 0 else 0 for x in lst]` (a ternary *inside* the element
  expression — the element must exist either way)

The rule the transcript implies: exactly **one expression** is allowed — a
comprehension cannot grow a second statement. That's precisely where you go
back to the `for` loop.

**4. Nesting mirrors nested loops**
```python
[[j for j in range(i)] for i in range(3)]   # [[], [0], [0, 1]]
```
Read the clauses left-to-right as you'd read nested `for` loops. Three or
more levels and readability collapses — a fair point in favor of the
transcript's stance of keeping comprehensions simple.

### Why It Matters
- It's not a micro-optimization gimmick: `LIST_APPEND` + inlined frame make
  it consistently faster than the manual loop, *and* it signals intent
  ("I'm building a list from an iterable") at a glance.
- The scoping difference from Python 2 means comprehensions can be safely
  typed in shared scripts without clobbering a variable named `i`.
- Knowing the one-expression limit tells you *when a comprehension becomes
  the wrong tool* — unreadable cleverness is a real cost.

### Minimal Executable Example
```python
# The lecture's problem, both ways
a = 5
table_loop = []
for i in range(1, 11):
    table_loop.append(5 * i)
table_comp = [5 * i for i in range(1, 11)]
print(table_loop == table_comp)          # True

# Loop variable stays inside
exec("t = [i for i in range(3)]")
try:
    print(i)
except NameError as e:
    print("NameError -", e)

# Filter vs conditional expression
nums = [3, -1, 4, -5, 0]
print([x for x in nums if x > 0])        # [3, 4] — filter
print([x if x > 0 else 0 for x in nums]) # [3, 0, 4, 0, 0] — ternary

# Nested comprehension = nested loops
print([[j for j in range(i)] for i in range(4)])   # [[], [0], [0, 1], [0, 1, 2]]

# Speed comparison
import timeit
loop = "t=[]\nfor i in range(100000): t.append(i)"
comp = "t = [i for i in range(100000)]"
print("loop:", timeit.timeit(loop, number=100))
print("comp:", timeit.timeit(comp, number=100))
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Expecting Python-2 leak | comprehension using `i` then reading `i` | `NameError` in Py3 — scoped to the comprehension |
| Cramming logic in | nested ternaries in one comprehension | One expression only — past two conditions, use a loop |
| Thinking it builds lazily | `[x for x in huge]` | Builds the **entire list in memory** — for lazy, use a generator expression `(x for x in huge)` |
| Side effects inside | `[print(x) for x in lst]` | Works but abuses the syntax — use a loop for effects |

### Key Insight
A list comprehension is a **declarative, scoped, single-expression list
builder**: the compiler inlines it (PEP 709) with save/restore scoping,
replaces method-call appends with the `LIST_APPEND` opcode, and enforces
exactly one expression — which is both the reason it's faster and the
boundary where you should return to a `for` loop.

---

**End of Lecture 32 — List Methods**

All 4 units documented. Ready for Lecture 33 (Tuples).
