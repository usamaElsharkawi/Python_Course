# Lecture 29 — Variable Scope and Docstrings

**Units covered**: 1. Scope and lifetime of variables, 2. The `global` keyword,
3. Docstrings: documenting functions, classes, and modules

---

## Unit 1 — Scope and Lifetime of Variables

### Core Concept
**Scope** defines where a variable can be accessed; **lifetime** defines how
long it exists in memory. In Python:
- **Local variables** — created inside a function, exist only during that
  function's execution
- **Global variables** — created at module level, exist for the program's
  duration

### What's Actually Happening

**1. Function call creates a local frame**
When `sum(4, 6)` is called:
1. Python creates a new **local namespace** (frame) for the call
2. Arguments `4, 6` are bound to parameters `a, b` in this frame
3. Local variable `c = a + b` is created in the same frame
4. `return c` passes the value back
5. The frame is **destroyed** — `a`, `b`, `c` cease to exist

```python
def sum(a, b):
    c = a + b
    return c

print(sum(4, 6))  # 10
print(c)          # NameError: name 'c' is not defined
```

**2. Global variables live in the module namespace**
```python
z = 8              # Module-level = global
def sum(a, b):
    print(z)       # Can READ global z

sum(4, 6)          # Prints 8
print(z)           # 8 — unchanged
```

**3. Assignment creates locals by default**
```python
z = 8
def sum(a, b):
    z = 1          # Creates NEW local z, shadows global
    return z

print(sum(4, 6))   # 1 (local)
print(z)           # 8 (global unchanged)
```

**4. Multiple scopes with same name**
```python
z = 8              # Global
def sum(a, b):
    z = 1          # Local to sum
def greet():
    z = 32         # Local to greet
```
Three different `z` variables coexist in different scopes.

### Minimal Executable Example

```python
# Global variable
counter = 0

def increment():
    local_var = counter + 1  # Reads global, creates local
    return local_var

print(increment())  # 1
print(counter)      # 0 (global unchanged)
print(local_var)    # NameError
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Reading before assignment | `def f(): print(x); x = 1` | `UnboundLocalError` — Python treats `x` as local due to assignment |
| Shadowing built-ins | `list = [1,2,3]` | Hides built-in `list()` globally in module |
| Modifying mutable global | `lst = []; def f(): lst.append(1)` | Works (mutation), but confusing — prefer return values |
| Nested function scope | `def outer(): x=1; def inner(): print(x)` | `inner` sees `outer`'s `x` (enclosing scope, next lecture) |

### Key Insight
Python's **LEGB rule** (Local → Enclosing → Global → Built-in) determines
name lookup. Assignment (`x = ...`) makes `x` **local** to the current
scope unless declared `global` or `nonlocal`. Function frames are
ephemeral — they exist only during the call.

---

## Unit 2 — The `global` Keyword: Modifying Globals from Inside Functions

### Core Concept
The `global` keyword tells Python: "When I assign to this name inside the
function, use the **module-level** binding, not a new local one." Without
it, assignment creates a local variable that shadows the global.

### What's Actually Happening

**1. Default behavior: assignment creates a local**
```python
z = 8
def sum(a, b):
    z = 1          # New local z, shadows global
    return z

print(sum(4, 6))   # 1
print(z)           # 8 (global untouched)
```

**2. `global` declaration changes the binding**
```python
z = 8
def sum(a, b):
    global z
    z = 1          # Modifies the GLOBAL z
    return z

print(sum(4, 6))   # 1
print(z)           # 1 (GLOBAL changed!)
```

When `global z` is executed:
1. Python marks `z` as a global name in the current function's bytecode
2. `STORE_NAME` for `z` writes to the module's `__dict__` instead of the
   local frame
3. Any subsequent `z = ...` modifies the module-level `z`

**3. Reading doesn't need `global`**
```python
z = 8
def f():
    print(z)   # Works — reads global
```
Only **assignment** (or `del`) requires `global`. The `LOAD_NAME` opcode
resolves via LEGB automatically.

**4. The transcript's example**
```python
z = 3
def sum(a, b):
    global z
    z = 0        # Modifies global z
    return a + b

print(sum(3, 12))  # 15
print(z)           # 0 (global changed from 3 to 0)
```

### Why It Matters
- **Intentional mutation**: `global` makes the side effect explicit — "I'm
  changing module state"
- **Interview question**: "Can you modify a global inside a function?" →
  Yes, with `global`
- **Debugging risk**: If multiple functions modify the same global,
  tracing who changed it becomes hard

### Minimal Executable Example

```python
# Counter using global
count = 0

def increment():
    global count
    count += 1
    return count

def reset():
    global count
    count = 0

print(increment())  # 1
print(increment())  # 2
print(count)        # 2 (global modified)
reset()
print(count)        # 0
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Forgetting `global` | `def f(): x = 1` when `x` is global | Creates local `x`, global unchanged |
| `global` on non-module name | `def f(): global x; x = 1` if no module `x` | Works (creates module `x`), but confusing |
| Overusing `global` | Multiple functions modifying same global | Spaghetti state — hard to debug |
| `global` with `nonlocal` | `global x` in nested function | `SyntaxError` — can't be both |

### Key Insight
`global` changes **binding semantics** for a name within a function:
`STORE_NAME` targets the module dictionary instead of the local frame.
Use sparingly — prefer passing values as arguments and returning
results to keep functions pure and testable.

---

## Unit 3 — Docstrings: Documenting Functions, Classes, and Modules

### Core Concept
A **docstring** is a string literal placed as the **first statement** in
a function, class, module, or method. It becomes the `__doc__` attribute
of that object, accessible at runtime and used by tools (help(), IDEs,
documentation generators).

### What's Actually Happening

**1. Syntax and placement**
```python
def add(a, b):
    """Return the sum of two numbers."""
    return a + b

print(add.__doc__)   # "Return the sum of two numbers."
help(add)            # Shows docstring in formatted help
```

**2. How it works internally**
- When Python compiles the function, the first statement if it's a
  string literal → stored in the code object's `co_consts`
- At function creation, this string is assigned to the function object's
  `__doc__` attribute
- `help(obj)` and `obj.__doc__` retrieve it at runtime

**3. Multi-line docstrings (PEP 257 convention)**
```python
def add(a: int, b: int) -> int:
    """Return the sum of two integers.

    Args:
        a: The first integer.
        b: The second integer.

    Returns:
        The sum of a and b.

    Example:
        >>> add(2, 3)
        5
    """
    return a + b
```

**4. Module and class docstrings**
```python
# my_module.py
"""This module provides math utilities."""

class Calculator:
    """A simple calculator class."""
    
    def add(self, a, b):
        """Add two numbers."""
        return a + b
```

### Why It Matters
- **Runtime introspection**: `help()`, `obj.__doc__`, `inspect.getdoc()`
  work dynamically
- **IDE support**: VSCode/PyCharm show docstrings on hover (the
  transcript notes this)
- **Documentation generation**: Sphinx, pdoc, mkdocstrings extract
  docstrings for HTML docs
- **API contracts**: Documents parameters, return types, exceptions,
  examples

### Minimal Executable Example

```python
def greet(name: str) -> str:
    """Return a greeting for the given name.
    
    Args:
        name: The person's name.
        
    Returns:
        A greeting string.
        
    Raises:
        ValueError: If name is empty.
    """
    if not name:
        raise ValueError("Name cannot be empty")
    return f"Hello, {name}!"

print(greet.__doc__)
# Return a greeting for the given name.
#     Args:
#         name: The person's name.
#     ...

help(greet)
# Help on function greet in module __main__:
# greet(name: str) -> str
#     Return a greeting for the given name.
#     ...
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Not first statement | `def f(): x = 1; """doc"""` | Not a docstring — just a string expression |
| Missing closing quotes | `"""doc` | `SyntaxError` |
| Indentation in multi-line | `""" line1\n line2"""` | Extra spaces in `__doc__`; use textwrap.dedent or align |
| Confusing with comments | `# comment` vs `"""doc"""` | Comments are ignored; docstrings are metadata |

### Key Insight
Docstrings are **executable metadata** — they live on the object at
runtime (`__doc__`), enabling dynamic help and tooling. They're not
comments (which are discarded by the parser). Every public
function/class/module should have a docstring describing *what it does*,
*args*, *returns*, and *raises*.

---

**End of Lecture 29 — Variable Scope and Docstrings**

All 3 units documented. Ready for the next step.