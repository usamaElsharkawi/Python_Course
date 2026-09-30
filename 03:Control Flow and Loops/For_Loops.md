# Lecture 15: For Loops in Python

## Unit 1: The `for` Loop and `range()` — Iteration Protocol Internals

### The Transcript's Version

> "For loops are used to iterate over a sequence. It can be a list, string, or range."
> 
> "Range function goes from 1 to n minus one."
> 
> ```python
> for i in range(1, 6):
>     print(i)  # 1, 2, 3, 4, 5
> ```

### The Real Version: Iteration Protocol

The `for` loop is **syntactic sugar for the iterator protocol**. What actually happens:

```python
for i in range(1, 6):
    print(i)
```

**Desugars to:**
```python
_iterable = range(1, 6)       # 1. Get the iterable
_iterator = iter(_iterable)   # 2. Call iter() → returns an iterator
while True:
    try:
        i = next(_iterator)   # 3. Call next() → get next item
    except StopIteration:     # 4. StopIteration → exit loop
        break
    print(i)                  # 5. Loop body
```

---

### Real Bytecode (CPython 3.14)

```
  1           LOAD_NAME                0 (range)
              PUSH_NULL
              LOAD_SMALL_INT           1
              LOAD_SMALL_INT           6
              CALL                     2
              GET_ITER                 ← ← ← iter() called HERE
      L1:     FOR_ITER                11 (to L2)
              STORE_NAME               1 (i)

  2           LOAD_NAME                2 (print)
              PUSH_NULL
              LOAD_NAME                1 (i)
              CALL                     1
              POP_TOP
              JUMP_BACKWARD           13 (to L1)   ← ← ← loop back

  1   L2:     END_FOR
              POP_ITER
              LOAD_CONST               1 (None)
              RETURN_VALUE
```

**Key bytecode instructions:**
| Instruction | Purpose |
|-------------|---------|
| `GET_ITER` | Calls `iter()` on the iterable, pushes iterator |
| `FOR_ITER` | Calls `next()` on iterator; jumps to L2 on `StopIteration` |
| `JUMP_BACKWARD` | Unconditional jump back to `FOR_ITER` (the loop) |
| `END_FOR` | Cleanup after loop ends |
| `POP_ITER` | Pops iterator from exception stack |

---

### The `range` Object Is NOT a List

```python
r = range(1, 6)
print(type(r))        # <class 'range'>
print(list(r))        # [1, 2, 3, 4, 5]  — materialized only when needed
```

**`range` is a lazy sequence** — it computes values on demand, doesn't store them all in memory.

```python
# range(1, 1_000_000) uses ~48 bytes, not ~8 MB
import sys
print(sys.getsizeof(range(1, 1_000_000)))  # 48 bytes
print(sys.getsizeof(list(range(1, 1_000_000))))  # ~8 MB
```

**Memory layout of `range`:**
```
range(start, stop[, step]) stores only 3 integers:
  - start
  - stop  
  - step
```
Values computed mathematically: `value = start + index * step`

---

### The Iterator Protocol (How `for` Actually Works)

Any object can be iterated if it implements **one of two protocols**:

#### 1. Iterator Protocol (preferred)
```python
class MyIterator:
    def __iter__(self):
        return self           # returns itself (is an iterator)
    
    def __next__(self):
        if self.exhausted:
            raise StopIteration
        return self.next_value
```

#### 2. Iterable Protocol (older)
```python
class MyIterable:
    def __getitem__(self, index):
        if index >= len(self):
            raise IndexError
        return self.data[index]
```

**`for` tries `__iter__` first**, falls back to `__getitem__` with integer indices 0, 1, 2...

---

### `range` Implements Both

```python
r = range(1, 6)

# Protocol 1: Iterator
it = iter(r)        # returns range_iterator object
print(next(it))     # 1
print(next(it))     # 2

# Protocol 2: Sequence (indexing)
print(r[0])         # 1
print(r[2])         # 3
print(len(r))       # 5
```

---

### The `for` Loop Variables Are Reassigned, Not New

```python
for i in range(3):
    print(i)

# i still exists after loop!
print(i)  # 2 (last value)
```

The loop variable `i` is **reassigned on each iteration** — it's the same name binding, not a new variable each time.

---

### Transcript Example: Multiplication Table

```python
for i in range(1, 11):
    print("5 x", i, "=", 5 * i)
```

**Output:**
```
5 x 1 = 5
5 x 2 = 10
5 x 3 = 15
...
5 x 10 = 50
```

**What happens per iteration:**
| Iteration | `i` | `print` args | Output |
|-----------|-----|--------------|--------|
| 1 | 1 | `"5 x", 1, "=", 5` | `5 x 1 = 5` |
| 2 | 2 | `"5 x", 2, "=", 10` | `5 x 2 = 10` |
| ... | ... | ... | ... |
| 10 | 10 | `"5 x", 10, "=", 50` | `5 x 10 = 50` |

**Note on `print` commas:** Each comma in `print(a, b, c)` adds a space (`sep=' '` by default).

---

### Why `range(1, 6)` Produces 1–5 (Not 1–6)

The transcript says: *"Range function goes from 1 to n minus one"*

**Internally:** `range` implements `__len__` and `__getitem__`:
```python
def __len__(self):
    return max(0, (stop - start + step - 1) // step)

def __getitem__(self, index):
    if index < 0:
        index += len(self)
    if index >= len(self):
        raise IndexError
    return start + index * step
```

**For `range(1, 6)`:**
- `start=1`, `stop=6`, `step=1`
- `len = (6 - 1 + 1 - 1) // 1 = 5`
- Valid indices: `0, 1, 2, 3, 4`
- Values: `1+0*1=1`, `1+1*1=2`, `1+2*1=3`, `1+3*1=4`, `1+4*1=5`

**This is zero-based indexing**, same as lists/strings. The `stop` is **exclusive** because it represents "length from start."

---

### Common Mistakes

#### 1. Off-by-one: `range(10)` gives 0–9, not 1–10
```python
for i in range(10):
    print(i)  # 0, 1, 2, ..., 9
```

#### 2. Modifying the loop variable doesn't affect iteration
```python
for i in range(5):
    i = 100      # Does nothing to the loop
    print(i)     # Prints 100 five times
```

#### 3. `range` is evaluated ONCE at loop start
```python
n = 5
for i in range(n):
    n = 100      # Doesn't change the loop!
    print(i)     # Still 0, 1, 2, 3, 4
```

---

### Key Takeaways

1. **`for` loop = iterator protocol** — `GET_ITER` → `FOR_ITER` → `JUMP_BACKWARD`
2. **`range` is lazy** — stores only start/stop/step, computes values on demand
3. **`StopIteration` ends the loop** — not a boolean flag, an exception
4. **Loop variable is reassigned** — same name binding each iteration
5. **`range(stop)` is exclusive** — zero-based, length = stop
6. **`range(start, stop)` excludes stop** — mathematical length calculation
7. **Iterable evaluated once** — changes to it during loop don't affect iteration

---

### Files Created
- `for_loop_basics.py` — transcript examples
- `for_loop_bytecode.py` — bytecode inspection
- `range_internals.py` — range object exploration