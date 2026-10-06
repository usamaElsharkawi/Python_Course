# Lecture 25 — Function Arguments and Return Values

**Units covered**: 1. Parameters vs arguments, 2. Positional arguments,
3. Default arguments, 4. Keyword arguments

---

## Unit 1 — Parameters vs Arguments

### Core Concept
**Parameters** are the variable names listed in the function definition.
**Arguments** are the actual values passed when the function is called.
This distinction is fundamental to understanding how functions receive
and process data.

### What's Actually Happening

**1. The two sides of a function call**
```python
def add(a, b):       # a, b are PARAMETERS
    return a + b

result = add(3, 5)   # 3, 5 are ARGUMENTS
```

- **Parameters** (`a`, `b`) are local variables inside the function.
  They exist only during the function's execution and are bound to
  whatever arguments are passed.
- **Arguments** (`3`, `5`) are the actual values supplied at the call
  site. They are evaluated first, then bound to the parameters in order.

**2. The binding process**
When `add(3, 5)` is called:
1. Python evaluates `3` and `5` — these are the arguments
2. A new local frame is created
3. `3` is bound to `a`, `5` is bound to `b`
4. The function body executes with these bindings
5. The frame is destroyed when the function returns

**3. The average example from the transcript**
```python
def average(a, b, c):
    return (a + b + c) / 3.0

average(3, 5, 1)    # a=3, b=5, c=1
average(1, 5, 3)    # a=1, b=5, c=3 (different average!)
```

### Why It Matters
- **Clarity**: Understanding the difference prevents confusion when
  reading code.
- **Debugging**: Knowing whether an issue is a parameter binding
  problem or an argument evaluation problem helps isolate errors.
- **Abstraction**: Parameters define the function's **interface**;
  arguments are the **data** that flows into it.

### Minimal Executable Example

```python
def add(a, b):          # a, b = parameters
    x = a + b
    return x

c = add(3, 5)           # 3, 5 = arguments
print(c)                # 8

# Same function, different arguments
print(add(10, 20))      # 30
print(add(100, 200))    # 300
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Confusing the terms | Calling `a, b` "arguments" | They are parameters — the values `3, 5` are arguments |
| Reusing parameter names | `def f(a): ...` then `a = 5; f(a)` | Works, but the outer `a` is shadowed inside the function |
| Mutating arguments | `def f(lst): lst.append(1)` | Lists are mutable, so arguments can be modified (side effect) |

### Key Insight
Parameters are the function's **interface**; arguments are the **data**
that flows into it. The same function can be called many times with
different arguments, each binding producing different results.

---

## Unit 2 — Positional Arguments

### Core Concept
Positional arguments are values passed to a function in a specific
order. Each argument is bound to the corresponding parameter by
position — the first argument goes to the first parameter, the second
to the second, and so on. This is the default and most common way to
call functions.

### What's Actually Happening

**1. Positional binding**
```python
def add(a, b):
    return a + b

add(3, 5)    # 3 → a, 5 → b
add(5, 3)    # 5 → a, 3 → b (different result!)
```

The arguments are matched to parameters left-to-right. The order
matters — swapping arguments changes which value goes to which
parameter.

**2. The transcript example**
```python
def average(a, b, c):
    return (a + b + c) / 3.0

average(3, 5, 1)    # a=3, b=5, c=1
average(1, 5, 3)    # a=1, b=5, c=3 (different average!)
```

### Why It Matters
- **Order sensitivity**: The caller must know the parameter order.
- **Default behavior**: Positional is the default calling convention
  — no special syntax needed.
- **Readability**: Short argument lists are clear, but long lists
  become error-prone. Keyword arguments improve clarity for many
  parameters.

### Minimal Executable Example

```python
def describe(name, age, city):
    return f"{name} is {age} years old and lives in {city}"

# Positional — order matters
describe("Alice", 30, "NYC")
# "Alice is 30 years old and lives in NYC"

# Wrong order — wrong result
describe(30, "Alice", "NYC")
# "30 is Alice years old and lives in NYC" — nonsensical!
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Wrong order | `average(1, 5, 3)` vs `average(3, 5, 1)` | Different results; always check parameter order |
| Too many arguments | `add(1, 2, 3)` for `def add(a, b)` | `TypeError: too many positional arguments` |
| Too few arguments | `add(1)` for `def add(a, b)` | `TypeError: missing required positional argument` |
| Mixing with keywords | `add(a=1, 2)` | `SyntaxError` — positional args cannot follow keyword |

### Key Insight
Positional arguments are bound to parameters in the order they
appear. The caller is responsible for knowing the correct order.

---

## Unit 3 — Default Arguments

### Core Concept
Default arguments are parameters with a pre-assigned value. If the
caller does not provide an argument for that parameter, the default
value is used. Default arguments are **optional** — the caller can
choose to omit them or override them.

### What's Actually Happening

**1. Syntax and behavior**
```python
def add(a, b, plus=0):
    return a + b + plus

add(3, 5)        # plus defaults to 0 → 8
add(3, 5, 2)     # plus overridden to 2 → 10
add(3, 5, plus=2) # same as above, using keyword
```

The default value is evaluated **once** when the function is defined,
not each time it's called. For mutable defaults (lists, dicts), this
means the same object is reused across calls — a common pitfall.

**2. Where defaults can appear**
Default arguments must come **after** all non-default (positional)
arguments:
```python
# Correct — defaults after positional
def f(a, b, c=1, d=2): ...

# Incorrect — SyntaxError
def f(a, b=1, c): ...  # non-default after default
```

### Why It Matters
- **Flexibility**: Functions can have optional behavior without
  requiring the caller to specify everything.
- **Backward compatibility**: Adding a new parameter with a default
  doesn't break existing calls.
- **Convenience**: Common values can be pre-set.

### Minimal Executable Example

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Alice"))           # Hello, Alice!
print(greet("Alice", "Hi"))    # Hi, Alice!
print(greet("Alice", greeting="Hey"))  # Hey, Alice!
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Mutable default | `def f(x=[])` | Same list object shared across all calls |
| Default after non-default | `def f(a=1, b)` | `SyntaxError` — defaults must come last |
| Overriding with keyword | `add(3, 5, plus=2)` | Works, but must use keyword to override a default |
| Implicit None default | `def f(a, b=None)` | Useful when detecting "no argument provided" |

### Key Insight
Default arguments make parameters optional. They must appear after all
required parameters. Use `None` (not mutable objects) when you need a
"fresh" default per call.

---

## Unit 4 — Keyword Arguments

### Core Concept
Keyword arguments allow the caller to specify which argument goes to
which parameter by using `parameter=value` syntax. Arguments can be
passed in **any order**, as long as each keyword matches a parameter
name.

### What's Actually Happening

**1. Syntax and behavior**
```python
def describe(name, age, city):
    return f"{name} is {age} years old and lives in {city}"

# Keyword arguments — any order
describe(name="Alice", age=30, city="NYC")
describe(age=30, city="NYC", name="Alice")   # same result!
describe(city="NYC", name="Alice", age=30)   # same result!
```

Each keyword is matched to the parameter with the same name. The
order doesn't matter because Python looks up the parameter by name.

**2. Mixing positional and keyword**
```python
describe("Alice", 30, city="NYC")    # first two positional, last keyword
describe("Alice", age=30, city="NYC") # first positional, last two keyword
```

**Rules for mixing:**
- Positional arguments must come before keyword arguments
- Each parameter receives exactly one value (no duplicates)

**3. The transcript example**
```python
def add(a, b, plus=0):
    return a + b + plus

add(b=5, a=3)        # a=3, b=5 → 8
add(b=5, a=3, plus=2) # a=3, b=5, plus=2 → 10
```

### Why It Matters
- **Clarity**: `describe(name="Alice", age=30, city="NYC")` is
  self-documenting — you don't need to check the function signature.
- **Flexibility**: You can skip default parameters or change the order.
- **Maintainability**: If parameter order changes, keyword-based
  calls still work.

### Minimal Executable Example

```python
def create_profile(name, age, bio=None, location=None):
    profile = f"Name: {name}, Age: {age}"
    if bio:
        profile += f", Bio: {bio}"
    if location:
        profile += f", Location: {location}"
    return profile

# All keyword — order doesn't matter
create_profile(name="Alice", age=30, bio="Engineer", location="NYC")

# Skip optional parameters
create_profile(name="Bob", age=25)
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Positional after keyword | `describe("Alice", name="Bob")` | `SyntaxError` — positional after keyword |
| Duplicate parameter | `describe(name="Alice", name="Bob")` | `SyntaxError` — keyword repeated |
| Unknown keyword | `describe(name="Alice", foo=1)` | `TypeError` — unexpected keyword argument |
| Missing required | `describe(name="Alice")` | `TypeError` — missing required argument: `age` |

### Key Insight
Keyword arguments make function calls self-documenting and
order-independent. They are especially useful for functions with many
parameters or when omitting default parameters.

---

## Unit 5 — Variable-Length Arguments (`*args` and `**kwargs`)

### Core Concept
To accept **any number** of arguments, use:
- `*args` — collects variable positional arguments into a tuple
- `**kwargs` — collects variable keyword arguments into a dict

### What's Actually Happening

**1. `*args` — variable positional arguments**
```python
def sum_all(*args):
    return sum(args)

sum_all(1, 2, 3)        # args = (1, 2, 3) → 6
sum_all(1, 2, 3, 4, 5)  # args = (1, 2, 3, 4, 5) → 15
```

The `*` tells Python to pack all positional arguments beyond the
fixed ones into a tuple named `args`.

**2. Mixing fixed, default, and varargs**
```python
def greet(greeting, *names):
    for name in names:
        print(f"{greeting}, {name}!")

greet("Hello", "Alice", "Bob", "Charlie")
# Hello, Alice!
# Hello, Bob!
# Hello, Charlie!
```

**3. `**kwargs` — variable keyword arguments**
```python
def show_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

show_info(name="Alice", age=30, city="NYC")
# name: Alice
# age: 30
# city: NYC
```

The `**` tells Python to pack all keyword arguments into a dict named
`kwargs`.

**4. Combining all three (full signature)**
```python
def full_example(a, b, c=0, *args, d, e=10, **kwargs):
    print(f"a={a}, b={b}, c={c}, args={args}, d={d}, e={e}, kwargs={kwargs}")

full_example(1, 2,                    # a=1, b=2 (positional)
             3,                       # c=3 (positional, overrides default)
             4, 5,                    # args=(4, 5)
             d=6,                     # d=6 (required keyword)
             e=7,                     # e=7 (keyword, overrides default)
             extra="x",               # kwargs={'extra': 'x'}
             )
```

### Why It Matters
- **Extensibility**: Functions like `print()`, `sum()`, `max()` accept
  any number of arguments using `*args`.
- **Flexibility**: `**kwargs` allows arbitrary keyword metadata
  without defining every possible parameter.
- **Forwarding**: `*args` and `**kwargs` make it easy to forward
  arguments to other functions: `f(*args, **kwargs)`.

### Minimal Executable Example

```python
# Sum of any numbers
def sum_all(*args):
    return sum(args)

print(sum_all(1, 2))          # 3
print(sum_all(1, 2, 3, 4, 5)) # 15
print(sum_all())              # 0 — empty tuple

# Keyword arguments with **kwargs
def show_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

show_info(name="Alice", age=30)
# name: Alice
# age: 30
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| `*args` as empty tuple | `f()` for `def f(*args)` | `args` is `()`, not `None` |
| `**kwargs` ordering | `f(**kw, "positional")` | `SyntaxError` — `*` and `**` cannot be mixed loosely |
| Unpacking dict into ** | `f(**{"a": 1})` | Works, passes `a=1` as keyword argument |
| Name confusion | `*args` vs `**kwargs` | `*` → tuple, `**` → dict; cannot confuse them |

### Key Insight
`*args` collects extra positional arguments into a tuple; `**kwargs`
collects extra keyword arguments into a dict. Use them to build
flexible APIs, but don't overuse — explicit parameters are clearer for
simple functions.

---