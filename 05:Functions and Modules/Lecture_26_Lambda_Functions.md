# Lecture 26 — Lambda Functions in Python

**Units covered**: 1. Lambda syntax and basic usage, 2. Equivalence with
`def` and use cases

---

## Unit 1 — Lambda Syntax and Basic Usage

### Core Concept
A **lambda** in Python is a way to create a small, anonymous function
inline. The syntax is:

```
lambda parameter_list: expression
```

Unlike `def`, no `return` keyword is needed — the `expression` is
implicitly returned.

### What's Actually Happening

**1. `lambda` is a reserved keyword**
Same as `return`, `def`, `if`, etc. Python recognizes `lambda` as part
of the language, not a function or variable name.

**2. Syntax breakdown**
```python
square = lambda x: x * x
```
- `lambda` — keyword signaling anonymous function creation
- `x` — parameter(s) for the function
- `:` — separates parameters from the expression
- `x * x` — the expression that is **implicitly returned** (no `return`
  keyword needed)

**3. Assignment creates a callable object**
When Python evaluates `lambda x: x * x`, it creates a function object
(stored in `__main__` with a `repr` like `<function <lambda> at
0x...>`) and binds it to the variable `square`. Because the function
has no name, it's called **anonymous**.

**4. Multi-argument lambdas**
```python
sum_func = lambda x, y: x + y
sum_func(6, 3)  # 9
```

The same rules apply — parameters on the left of `:`, expression on the
right.

### Minimal Executable Example

```python
# Single argument
square = lambda x: x * x
print(square(3))  # 9

# Multi-argument
add = lambda x, y: x + y
print(add(6, 2))  # 8

# Using in print directly — immediately invoked
print((lambda x: x * x)(5))  # 25

# Compare with def
def square_def(x):
    return x * x
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| No body, only expression | `lambda x: return x + 1` | `SyntaxError` — `return` not allowed in lambda |
| Multi-statement | `lambda x: print(x); return x` | `SyntaxError` — lambda body is a single expression |
| Anonymous nature | `print(square)` | Shows `<function <lambda> at 0x...>`, not the name `square` |
| Assignment "discouraged" by PEP 8 | `f = lambda x: x` | PEP 8 recommends `def` for named functions |

### Key Insight
`lambda` creates an **anonymous** function from a single expression.
It is immediately assigned to a variable, which becomes the function
object's name in the namespace. The expression after `:` is the
implicit return value.

---

## Unit 2 — Equivalence with `def` and Use Cases

### Core Concept
A lambda is **semantically equivalent** to a `def`-defined function
with a single expression body. Lambdas are used for **convenience**
when you need a short, one-line function — especially when **passing
functions as arguments** to other functions.

### What's Actually Happening

**1. Equivalence with `def`**

The transcript states:
```python
square = lambda x: x * x
```
is **as good as** writing:
```python
def square(x):
    return x * x
```

Both create a function object that:
- Takes one parameter `x`
- Returns `x * x`
- Has the same `__call__` behavior

The difference is purely syntactic:
- `def` creates a **named** function with its own block
- `lambda` creates an **anonymous** function from a single expression

**2. Lambda as a callable object**
When `square = lambda x: x * x` executes:
1. Python evaluates the lambda expression, creating a function object
2. The function object is bound to the name `square`
3. You can inspect it just like a `def` function:

```python
square = lambda x: x * x
print(type(square))  # <class 'function'>
print(square)        # <function <lambda> at 0x...>
print(square(5))     # 25
```

**3. Passing functions as arguments**
This is the transcript's key insight: "sometimes we want to pass a
function to a function." Many Python built-ins accept callable
arguments:

```python
data = [1, 2, 3, 4, 5]

# Pass lambda to map() — apply function to each element
squared = list(map(lambda x: x ** 2, data))
# [1, 4, 9, 16, 25]

# Pass lambda to filter() — select elements
evens = list(filter(lambda x: x % 2 == 0, data))
# [2, 4]

# Pass lambda to sorted() — customize sort
words = ["apple", "pie", "banana"]
sorted_words = sorted(words, key=lambda w: len(w))
# ['pie', 'apple', 'banana'] — sorted by length
```

In each case, the lambda **is** the function — it gets called
internally by `map`/`filter`/`sorted`.

### Why It Matters
- **Higher-order functions**: `map`, `filter`, `sorted`, `reduce`,
  pandas `.apply()` all expect a function argument. Lambdas are the
  idiomatic way to provide small callbacks.
- **Inline, no pollution**: Writing `def` for a 1-expression function
  that's used once adds noise to the module namespace. Lambda keeps it
  inline.
- **No separate statement needed**: You can define and use a function in
  a single expression context (e.g., inside
  `sorted(data, key=lambda x: ...)`).

### Minimal Executable Examples

```python
data = [1, 2, 3, 4, 5]

# map — apply to each
squared = list(map(lambda x: x ** 2, data))
print(squared)  # [1, 4, 9, 16, 25]

# filter — keep matching
evens = list(filter(lambda x: x % 2 == 0, data))
print(evens)   # [2, 4]

# sorted — custom key
words = ["apple", "pie", "banana"]
sorted_by_len = sorted(words, key=lambda w: len(w))
print(sorted_by_len)  # ['pie', 'apple', 'banana']

# Equivalent def — more verbose
def square(x):
    return x * x

# Same behavior — lambda is just shorthand
square_lambda = lambda x: x * x
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| PEP 8 discourages assignment | `f = lambda x: x` | Linter warning — use `def` instead for named functions |
| No docstrings | `lambda x: x ** 2` | Can't add a docstring — harder to introspect |
| Single expression limit | `lambda x: x; y` | `SyntaxError` — semicolons or statements not allowed in expression context |
| Readability | `lambda x, y, z: x + y * z` | Complex lambdas hurt readability — use `def` for non-trivial logic |
| IIFE confusion | `(lambda x: x + 1)(2)` | "Immediately invoked function expression" — valid but confusing for beginners |

### Key Insight
Lambda = anonymous + single-expression + convenience. Use it for
**short throwaway functions**, especially as arguments to `map`,
`filter`, `sorted`, etc. For any function with a meaningful name or
multi-line logic, prefer `def`.

---

**End of Lecture 26 — Lambda Functions in Python**

All 2 units documented. Ready for the next step.