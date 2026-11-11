# Lecture 49 — Map, filter, and reduce

**Units covered**: 1. `map` — apply a function to every element,
2. `filter` — keep elements where function returns True,
3. `reduce` — collapse iterable to a single value,
4. Lambda functions & readability

---

## Unit 1 — `map` — apply a function to every element

### Core Concept
`map(func, iterable)` applies `func` to every element of the iterable and returns a **map object** (lazy iterator). You must cast it to `list` to see the values.

### What's Actually Happening
```python
numbers = [1, 2, 3, 4, 5, 4, 21]

def square(x):
    return x * x

new = map(square, numbers)
print(new)        # <map object at 0x...> — lazy, not evaluated yet
print(list(new))  # [1, 4, 9, 16, 25, 16, 441] — square applied to each
```

- `map` returns a lazy iterator — memory efficient, computed on demand
- `list(map(...))` forces evaluation and materializes results

### Why It Matters
- Functional alternative to manual `for` loops with `.append()`
- One function applied uniformly across a sequence

### Minimal Executable Example
```python
numbers = [1, 2, 3, 4, 5, 4, 21]

def square(x):
    return x * x

new = map(square, numbers)
print(list(new))   # [1, 4, 9, 16, 25, 16, 441]
```

---

## Unit 2 — `filter` — keep elements where function returns True

### Core Concept
`filter(func, iterable)` keeps only elements where `func(element)` returns `True`, returning a **filter object** (lazy iterator).

### What's Actually Happening
```python
def is_greater_than_nine(x):
    if x > 9:
        return True
    return False

a = [1, 2, 1, 3, 5, 34, 2, 13]  # mixed list

new = filter(is_greater_than_nine, a)
print(new)        # <filter object at 0x...>
print(list(new))  # [34, 13] — only values > 9
```

- The predicate function runs on each element
- Elements returning `True` are accumulated; `False` are discarded
- Non-numeric values work too, as long as the predicate handles them

### Why It Matters
- Declarative filtering — "give me only the elements matching this condition"
- Replaces manual `for` loop with `if` + `.append()`

### Minimal Executable Example
```python
def is_greater_than_nine(x):
    return x > 9

a = [1, 2, 1, 3, 5, 34, 2, 13]
print(list(filter(is_greater_than_nine, a)))   # [34, 13]
```

---

## Unit 3 — `reduce` — collapse iterable to a single value

### Core Concept
`reduce(func, iterable)` applies `func` cumulatively: first to elements 0 and 1, then to the result and element 2, etc., until one value remains. Must be imported: `from functools import reduce`.

### What's Actually Happening
```python
from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

def sum(a, b):
    return a + b

c = reduce(sum, numbers)   # 21
```

### Step-by-step trace
- `sum(1, 2)` → 3
- `sum(3, 3)` → 6
- `sum(6, 4)` → 10
- `sum(10, 5)` → 15
- `sum(15, 6)` → 21

### Why It Matters
- Collapses a sequence into one accumulated result (sum, product, max, concatenation, etc.)
- `func` always takes two arguments: running total + next element

### Minimal Executable Example
```python
from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]
def sum(a, b):
    return a + b

print(reduce(sum, numbers))   # 21
```

---

## Unit 4 — Lambda functions & readability

### Core Concept
Lambda functions are frequently used with `map`/`filter`/`reduce` for one-line throwaway functions. But readability and maintainability come first — don't use lambda if it makes the code harder to understand.

### What's Actually Happening
```python
# Instead of:
# def square(x): return x * x
# map(square, numbers)

# Use:
map(lambda x: x * x, numbers)

# Instead of:
# def is_greater_than_nine(x): return x > 9
# filter(is_greater_than_nine, a)

# Use:
filter(lambda x: x > 9, a)
```

- Same output, fewer lines
- Use `def` when the logic is complex or reused elsewhere; use `lambda` for simple, single-use transformations

### Minimal Executable Example
```python
numbers = [1, 2, 3, 4, 5]
print(list(map(lambda x: x * x, numbers)))      # [1, 4, 9, 16, 25]
print(list(filter(lambda x: x > 2, numbers)))   # [3, 4, 5]
```

---

## Key Insight
`map`, `filter`, and `reduce` are higher-order functions that take a function and an iterable. `map` transforms every element, `filter` keeps elements matching a predicate, `reduce` collapses to one value. All return lazy iterators (except `reduce` which returns a single value), so cast to `list` when you need to materialize results. Lambdas make them concise, but prefer `def` for readability when logic is complex.
