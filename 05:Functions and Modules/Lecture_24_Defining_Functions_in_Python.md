# Lecture 24 — Defining Functions in Python

**Units covered**: 1. Why functions exist: DRY principle and maintainability, 2. Function definition syntax (`def`, parameters, body), 3. Reserved keywords and naming rules

---

## Unit 1 — Why Functions Exist: DRY Principle and Maintainability

### Core Concept
Functions exist to eliminate **code repetition** and improve **maintainability**. Without functions, the same computation logic must be copy-pasted everywhere it's needed, making programs longer and harder to update.

### What's Actually Happening

**1. The problem of repeated code**
The transcript shows computing the average of three numbers twice:
- First set: `average = (a + b + c) / 3`
- Second set: `average1 = (a1 + b1 + c1) / 3`

If the averaging formula changes (e.g., divide by `3.0` instead of `3`), every copy-pasted instance must be updated manually. This is error-prone and doesn't scale for complex logic spanning 50–60 lines.

**2. The DRY principle**
**D**on't **R**epeat **Y**ourself. Functions let you:
- Write the logic **once** in a single place
- Reuse it by **calling** it with different inputs
- Change the implementation in exactly **one** location

**3. Maintainability**
A 500-line program with repeated logic is harder to read, debug, and modify than a program with 50 lines of reusable functions. Functions provide **abstraction**: the caller doesn't need to know the internal implementation, only the function's name and parameters.

### Why It Matters
- **Bug propagation**: A bug in repeated code must be fixed in every copy. With a function, fix it once.
- **Readability**: `average(3, 5, 1)` is self-documenting compared to `(3 + 5 + 1) / 3` scattered throughout code.
- **Testing**: A single function can be unit-tested in isolation.

### Minimal Executable Examples

```python
# Without function — repeated logic
a, b, c = 3, 5, 1
avg1 = (a + b + c) / 3

a1, b1, c1 = 4, 2, 1
avg2 = (a1 + b1 + c1) / 3

print(avg1, avg2)  # 3.0 2.333...

# With function — single definition, multiple calls
def average(x, y, z):
    return (x + y + z) / 3

print(average(3, 5, 1))   # 3.0
print(average(4, 2, 1))   # 2.333...
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Magic numbers | `(a + b + c) / 3` — `3` appears without context | If the divisor changes, every instance must be updated |
| Copy-paste drift | Two copies of the same logic slowly diverge | Bugs appear because one copy was modified and the other wasn't |

### Key Insight
Functions are the primary mechanism for **code reuse** in Python. They transform a program from a linear script into a composition of reusable, testable, and maintainable components.

---

## Unit 2 — Function Definition Syntax (`def`, Parameters, Body)

### Core Concept
A function in Python is defined using the `def` keyword, followed by a name, a parenthesized parameter list, and a colon. The indented block after the colon is the **function body**. Defining a function does not execute it — it only creates a callable object. The function runs only when **called** by name with arguments.

### What's Actually Happening

**1. `def` creates a function object**
When Python executes `def average(a, b, c):`, it:
1. Creates a new function object (`PyFunctionObject`) in memory
2. Binds it to the name `average` in the current namespace (module globals or enclosing scope)
3. Stores the bytecode, defaults, annotations, and closure information inside the function object
4. **Does not execute the body** — the body only runs when the function is called

**2. Parameter binding**
`average(3, 5, 1)` triggers the function call protocol:
- A new **local namespace** (frame) is created
- Positional arguments `3, 5, 1` are bound to parameters `a, b, c` in order
- The function body executes in this new local scope
- When the body finishes, the local frame is destroyed

**3. Bytecode for definition vs call**
```python
>>> import dis
>>> dis.dis("def average(a, b, c):\n    return (a+b+c)/3")
  1           0 LOAD_CONST               0 (<code object average>)
              2 LOAD_CONST               1 ('average')
              4 MAKE_FUNCTION            0
              6 STORE_NAME               0 (average)
              8 RETURN_CONST             1 (None)
```

Notice: the body bytecode is stored as a code object but **not executed** at definition time.

```python
>>> dis.dis("average(3, 5, 1)")
  1           0 LOAD_NAME                0 (average)
              2 LOAD_CONST               0 (3)
              4 LOAD_CONST               1 (5)
              6 LOAD_CONST               2 (1)
              8 CALL                     <function average>
             10 RETURN_VALUE
```

**4. `return` vs `print`**
- `return d` — sends the value `d` back to the caller and **exits the function immediately**. The caller receives this value as the function's result.
- `print(d)` — prints to stdout as a side effect, but the function returns `None` implicitly if there's no `return` statement.

### Why It Matters
- **Function definitions are declarative**: they describe what to do, not when to do it.
- **Calling is what triggers execution**: forgetting to call a function means nothing happens (as the transcript demonstrates).
- **Parameter order matters**: positional arguments are matched left-to-right.

### Minimal Executable Examples

```python
# Function definition — does NOT execute the body
def greet(name):
    print(f"Hello, {name}")

# Nothing printed yet — function is defined but not called

# Function call — now the body executes
greet("Alice")  # Hello, Alice

# Return value vs print
def add(a, b):
    return a + b      # returns value
    print("never runs")  # unreachable after return

result = add(2, 3)  # result = 5

def add_side_effect(a, b):
    print(a + b)     # prints to stdout

result2 = add_side_effect(2, 3)  # prints 5, but result2 = None
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Defining but not calling | `def f(): return 1` — never invokes `f()` | Body never executes |
| Confusing `return` with `print` | `def f(): print(1)` then `x = f()` | `x` is `None`, not `1` |
| Name shadowing built-in | `def sum(a, b): ...` | Shadows built-in `sum()` |
| Wrong parameter count | `average(1, 2)` for `def average(a, b, c)` | `TypeError: missing required argument` |

### Key Insight
`def` creates a callable object and binds it to a name. The body executes only when the function is called. Use `return` to pass a value back; without `return`, the function returns `None`.

---

## Unit 3 — Reserved Keywords and Naming Rules

### Core Concept
Function names must follow the same rules as variable names. Additionally, Python reserves a set of keywords that cannot be used as identifiers (function names, variable names, etc.). `return` and `def` are two such keywords.

### What's Actually Happening

**1. Identifier syntax rules**
A valid function name:
- Starts with a letter (`a–z`, `A–Z`) or underscore (`_`)
- Followed by any combination of letters, digits (`0–9`), or underscores
- Is case-sensitive (`myFunc` ≠ `myfunc`)
- Cannot be a Python reserved keyword

**2. Reserved keywords in Python**
Python reserves 36+ keywords (varies slightly by version). Common ones include:

| Keyword | Purpose |
|---------|---------|
| `def` | Define a function |
| `return` | Return a value from a function |
| `if`, `else`, `elif` | Conditionals |
| `for`, `while`, `break`, `continue` | Loops |
| `class`, `import`, `from`, `as` | OOP/module system |
| `lambda` | Anonymous functions |
| `try`, `except`, `finally` | Exception handling |
| `True`, `False`, `None` | Literals |

If you try to use a keyword as a function name, Python raises a `SyntaxError`:

```python
>>> def return(x):
  File "<stdin>", line 1
    def return(x):
            ^
SyntaxError: invalid syntax
```

**3. `return` as a reserved keyword**
The transcript notes that `return` cannot be used as a variable name because it is a reserved keyword used to exit a function and optionally pass a value back.

**4. Valid vs invalid examples**

```python
# Valid function names
def average(a, b, c): ...
def _helper(): ...
def func1(): ...
def myAverage(): ...

# Invalid function names
def 1func(): ...      # starts with digit
def my-func(): ...    # contains hyphen
def return(): ...     # reserved keyword
def for(): ...        # reserved keyword
```

### Why It Matters
- **Syntax errors at parse time**: Python catches invalid identifiers before execution, preventing subtle runtime bugs.
- **Readability**: Following naming conventions makes code self-documenting.
- **Avoiding shadowing**: Using a keyword or built-in name as an identifier shadows the original meaning, leading to confusing errors.

### Minimal Executable Examples

```python
# Valid
def my_func():
    return 42

print(my_func())  # 42

# Invalid — reserved keyword
# def return(x):
#     return x
# SyntaxError: invalid syntax

# Invalid — starts with digit
# def 1func():
#     pass
# SyntaxError: invalid syntax
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Using reserved keywords | `def class(): ...` | `SyntaxError: invalid syntax` |
| Starting with digit | `def 1avg(): ...` | `SyntaxError` |
| Shadowing built-in | `def list(): ...` | Hides built-in `list`; can cause errors later |
| Confusing naming | `def Avg(): ...` vs `def avg(): ...` | Both valid, but PEP 8 recommends `snake_case` |

### Key Insight
Function names are identifiers and must follow the same syntactic rules as variables. Python's reserved keywords are off-limits. Use descriptive, `snake_case` names to maximize readability and avoid collisions.

---

## Unit 4 — `return` Semantics and the Function Call Protocol

### Core Concept
The `return` keyword sends a value back to the caller and immediately terminates the function. A function without an explicit `return` statement returns `None` by default.

### What's Actually Happening

**1. The call stack and frame creation**
When `average(3, 5, 1)` is called:
1. Python pushes a new **frame** onto the call stack
2. Arguments `3, 5, 1` are bound to local variables `a, b, c`
3. The function body executes in this frame
4. If `return d` is encountered, the value `d` is stored as the call result, the frame is popped, and control resumes at the caller
5. If the body finishes without `return`, Python implicitly returns `None`

**2. `None` as the implicit return value**
Every Python function returns something. If there's no `return`, the return value is `None`:

```python
>>> def no_return():
...     x = 1
...
>>> print(no_return())
None
```

**3. Early return and unreachable code**
`return` exits the function immediately. Any code after `return` in the same block is **unreachable**:

```python
def example():
    return 1
    print("never runs")  # unreachable
```

**4. Multiple return paths**
A function can have multiple `return` statements. The first one encountered during execution determines the return value:

```python
def check(n):
    if n > 0:
        return "positive"
    elif n < 0:
        return "negative"
    return "zero"
```

**5. Returning vs printing**
- `return value` — passes `value` back to the caller as the function's result
- `print(value)` — outputs `value` to stdout as a side effect, but the function's return value remains `None`

### Why It Matters
- **Composability**: Functions that `return` values can be nested in expressions: `add(average(1,2,3), 4)`.
- **Side-effect vs pure functions**: `print` creates output (side effect), `return` produces a value (pure function behavior).
- **Debugging**: If you accidentally use `print` instead of `return`, the function appears to work but returns `None`, causing `TypeError` later when the result is used.

### Minimal Executable Examples

```python
# Returning a value
def average(a, b, c):
    d = (a + b + c) / 3.0
    return d

result = average(3, 5, 1)
print(result)  # 3.0

# Implicit None return
def greet(name):
    print(f"Hello, {name}")

x = greet("Alice")  # prints "Hello, Alice"
print(x)            # None

# Multiple return paths
def sign(n):
    if n > 0:
        return "positive"
    elif n < 0:
        return "negative"
    return "zero"

print(sign(5))   # positive
print(sign(-3))  # negative
print(sign(0))   # zero
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| `print` instead of `return` | `def f(): print(42)` then `x = f()` | `x` is `None`, not `42` |
| Missing `return` | `def f(): x = 1` then `y = f()` | `y` is `None`, not `1` |
| Unreachable code | `return 1; print("hi")` after return | Dead code; never executes |
| Returning from `try/except` | `return` in `try` skips `finally`? | Actually `finally` still runs, but `return` value can be overridden by `finally` |

### Key Insight
`return` terminates the function and passes a value back. Without `return`, the function returns `None`. This is why calling `average(3, 5, 1)` without `return` gives `None` — the function prints the result but returns nothing usable.

---