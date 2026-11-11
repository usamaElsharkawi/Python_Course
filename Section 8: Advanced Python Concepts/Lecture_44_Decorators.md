# Lecture 44 — Decorators in Python

**Units covered**: 1. What decorators are & the manual pattern,
2. The `@` syntax (syntactic sugar),
3. Decorators with arguments (triple nesting),
4. Use cases & recap

---

## Unit 1 — What Decorators Are & the Manual Pattern

### Core Concept
A decorator is a function that **takes a function**, creates a new function (a wrapper) using it, and **returns that new function**. This lets you enhance or modify an existing function without changing its original source code.

### What's Actually Happening
```python
def say_hello():
    print("Hello")

def decorator(func):
    def wrapper():
        print("I'm about to execute a function")
        func()           # call the original function
        print("I have executed this function")
    return wrapper       # return the new function
```

- `decorator` receives `say_hello` as `func`
- It defines `wrapper` — a new function that prints before/after calling `func`
- It returns `wrapper` (the function object itself, not called)

### Manual usage
```python
f = decorator(say_hello)   # f is now wrapper, with func=say_hello baked in
f()
# Output:
# I'm about to execute a function
# Hello
# I have executed this function
```

`f` is essentially this:
```python
def f():
    print("I'm about to execute a function")
    print("Hello")          # body of say_hello substituted in
    print("I have executed this function")
```

### Why It Matters
- You can modify behavior (print before/after, log, time, validate) without touching the original function
- The original function (`say_hello`) is unchanged — you create a *new* function that wraps it
- This is just nested functions + first-class functions (functions as arguments/return values)

### Minimal Executable Example
```python
def say_hello():
    print("Hello")

def decorator(func):
    def wrapper():
        print("I'm about to execute a function")
        func()
        print("I have executed this function")
    return wrapper

f = decorator(say_hello)
f()
```

---

## Unit 2 — The `@` Syntax (Syntactic Sugar)

### Core Concept
The `@decorator` syntax is just shorthand for `say_hello = decorator(say_hello)`. It rebinds the name `say_hello` to the wrapper function returned by the decorator. Python applies the decorator **at definition time**, not at call time.

### What's Actually Happening
**Without `@` (manual):**
```python
def say_hello():
    print("Hello")

say_hello = decorator(say_hello)   # rebind name to wrapper
```

**With `@` (sugar):**
```python
@decorator
def say_hello():
    print("Hello")
```

These are **identical**. Python:
1. Defines `say_hello` as a function object
2. Immediately passes it to `decorator(say_hello)`
3. Rebinds `say_hello` to whatever `decorator` returns (the `wrapper` function)

So after decoration, `say_hello` is no longer the original function — it's `wrapper`, which has the original `say_hello` captured as `func` in its closure.

### Why It Matters
- Cleaner, more readable than manual reassignment
- The decoration happens once (at import/definition time), so there's no runtime overhead per call
- It clearly signals "this function is wrapped" right above the `def`
- Commonly used in Flask/Django for routes, auth, middleware

### Minimal Executable Example
```python
def decorator(func):
    def wrapper():
        print("We are about execute the func")
        func()
        print("we have executed the func")
    return wrapper

@decorator
def say_hello():
    print("Hello")

say_hello()
# Output:
# We are about execute the func
# Hello
# we have executed the func

# Proof: say_hello is now wrapper, not the original
print(say_hello.__name__)   # 'wrapper' — not 'say_hello'
```

---

## Unit 3 — Decorators with Arguments (Triple Nesting)

### Core Concept
When a decorator needs arguments (e.g., `@repeat(7)`), you add one more nesting level. The outermost function accepts the decorator arguments and returns the actual decorator, which then accepts the function and returns the wrapper. This is triple nesting: `repeat` → `decorator` → `wrapper`.

### What's Actually Happening
```python
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorator
```

### Call chain for `@repeat(7)` above `def say_hello(a):`
1. `repeat(7)` runs → returns `decorator` (with `n=7` captured in closure)
2. `decorator(say_hello)` runs → returns `wrapper` (with `func=say_hello`, `n=7` captured)
3. `say_hello` is now `wrapper`
4. `say_hello("Harry")` → `wrapper("Harry")` → calls `say_hello("Harry")` seven times

### What each layer holds
| Layer | Parameter | What it captures |
|---|---|---|
| `repeat` | `n` | number of repetitions (7) |
| `decorator` | `func` | the function being decorated (`say_hello`) |
| `wrapper` | `*args, **kwargs` | the actual call arguments (`"Harry"`) |

### Why Three Layers?
- `@repeat` alone would pass `say_hello` as `n` — wrong types
- `repeat(7)` must run **first** to configure `n`, then return a decorator that accepts the function
- Without the outer layer, you can't pass configuration arguments to the decorator

### Why It Matters
- `@repeat(7)`, `@route("/home")`, `@cache(ttl=60)` — configurable decorators are everywhere in Flask/Django/real code
- The same nesting pattern scales: more arguments = more nesting layers
- `*args, **kwargs` in `wrapper` lets the decorated function accept any arguments

### Minimal Executable Example
```python
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(7)
def say_hello(a):
    print(f"Hello {a}")

say_hello("Harry")
# Prints "Hello Harry" 7 times

# Equivalent manual form:
# say_hello = repeat(7)(say_hello)
# say_hello("Harry")
```

---

## Unit 4 — Use Cases & Recap

### Core Concept
Decorators are most often **used**, not created, in day-to-day Python. Common real-world applications: logging, timing, authentication/authorization, caching, rate limiting, input validation, instrumentation, and web framework routing/middleware (Flask, Django).

### What's Actually Happening

| Use Case | What the decorator does |
|---|---|
| **Logging** | Records when a function is called, with what args, and when it returns |
| **Timing** | Wraps `time.perf_counter()` around the call to measure execution time |
| **Auth / Authorization** | Checks user permissions before letting the function run; raises/returns early if unauthorized |
| **Caching** | Stores return values keyed by arguments; returns cached result on repeat calls |
| **Rate limiting** | Tracks call timestamps and rejects calls exceeding a threshold |
| **Input validation** | Validates arguments before passing them to the wrapped function |
| **Instrumentation** | Adds monitoring/profiling hooks (CPU time, call counts) |

In Flask/Django:
- `@app.route("/home")` registers a URL route
- `@login_required` checks authentication before running a view

### Minimal Executable Example
```python
import time
from functools import wraps

def log_calls(func):
    @wraps(func)  # preserves __name__, __doc__ of original
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@log_calls
def add(a, b):
    return a + b

add(3, 4)
# Calling add
# add returned 7
```

**Note:** `functools.wraps` copies `__name__`, `__doc__`, etc. from the original function to the wrapper — otherwise `add.__name__` would be `"wrapper"` after decoration.

### Why It Matters
- **Separation of concerns** — business logic stays in the function; cross-cutting concerns (logging, auth) live in decorators
- **Reusability** — one decorator applies to many functions
- **Frameworks** — Flask/Django rely heavily on decorators; understanding them is essential for web development
- **Transparency** — the decorated function's signature appears unchanged to callers

---

## Key Insight
A decorator is a higher-order function: it takes a function and returns a new function. The `@` syntax is sugar for rebinding the name. With arguments, you add one more nesting layer (outer function captures config, returns the real decorator). `functools.wraps` preserves the original function's metadata on the wrapper.
