# Lecture 51 — `*args` and `**kwargs`

**Units covered**: 1. `*args` — variable positional arguments (tuple),
2. `**kwargs` — variable keyword arguments (dict),
3. Combining `*args` and `**kwargs` (order: args first, kwargs second)

---

## Unit 1 — `*args` — variable positional arguments (tuple)

### Core Concept
`*args` collects all extra positional arguments into a **tuple**. This lets a function accept any number of positional arguments without defining a fixed parameter for each.

### What's Actually Happening
```python
def sum(*args):
    total = 0
    for item in args:       # args is a tuple — iterable
        total += item
    return total

print(sum(342, 2, 7))       # 351 — 342 + 2 + 7
print(sum(342, 2, 7, 9))    # 360 — works with any count
```

- `*args` gathers `342, 2, 7` into `args = (342, 2, 7)` — a tuple
- You can iterate it with `for item in args`, index it (`args[0]`), or use `len(args)`
- `total` starts at 0, accumulates each item, returns the sum

### Why It Matters
- Functions become flexible — accept 2, 3, 5, or any number of arguments
- No more `TypeError: takes 2 positional arguments but 3 were given`

### Minimal Executable Example
```python
def sum(*args):
    total = 0
    for item in args:
        total += item
    return total

print(sum(342, 2, 7))   # 351
print(sum(342, 2, 7, 9))  # 360
```

---

## Unit 2 — `**kwargs` — variable keyword arguments (dict)

### Core Concept
`**kwargs` collects all extra keyword arguments (name=value) into a **dictionary**. Keys are the argument names, values are the argument values.

### What's Actually Happening
```python
def marks(**kwargs):
    for item in kwargs.keys():
        print(f"The max of {item} is {kwargs[item]}")

marks(Shubham=34, Vikranth=54, Jack=34, Maddie=90)
# The max of Shubham is 34
# The max of Vikranth is 54
# The max of Jack is 34
# The max of Maddie is 90
```

- `**kwargs` gathers `Shubham=34, Vikranth=54, ...` into `kwargs = {"Shubham": 34, "Vikranth": 54, "Jack": 34, "Maddie": 90}` — a dict
- `.keys()` gives the names; `kwargs[item]` gives the score
- You can add unlimited key-value pairs at call time

### Why It Matters
- Flexible named arguments — perfect for optional/config-style parameters
- Callers pass `name=value` pairs; the function receives them as a dict

### Minimal Executable Example
```python
def marks(**kwargs):
    for item in kwargs.keys():
        print(f"The max of {item} is {kwargs[item]}")

marks(Shubham=34, Vikranth=54, Jack=34, Maddie=90)
```

---

## Unit 3 — Combining `*args` and `**kwargs` (order matters)

### Core Concept
You can combine both in one function, but **`*args` must come before `**kwargs`** in the parameter list. `*args` collects positional extras into a tuple; `**kwargs` collects keyword extras into a dict.

### What's Actually Happening
```python
def func_one(*args, **kwargs):
    print(args)      # tuple of positional extras
    print(kwargs)    # dict of keyword extras

func_one(1, 2, 4, 5, Jack=34, Jill=32, Mary=31)
# (1, 2, 4, 5)
# {'Jack': 34, 'Jill': 32, 'Mary': 31}
```

- `args = (1, 2, 4, 5)` — positional arguments after the named ones
- `kwargs = {"Jack": 34, "Jill": 32, "Mary": 31}` — keyword arguments
- `func_one(Jack=34, 1, 2)` → `SyntaxError` — positional after keyword not allowed
- `def func_one(**kwargs, *args)` → `SyntaxError` — `*args` must precede `**kwargs`

### Why It Matters
- Best of both worlds: flexible positional args + flexible named config
- Order rule (`*args` before `**kwargs`) is enforced by Python syntax

### Minimal Executable Example
```python
def func_one(*args, **kwargs):
    print(args)
    print(kwargs)

func_one(1, 2, 4, 5, Jack=34, Jill=32, Mary=31)
```

---

## Key Insight
`*args` collects extra positional arguments into a tuple; `**kwargs` collects extra keyword arguments into a dict. Used together (`*args` before `**kwargs`), they let functions accept any combination of positional and named arguments — essential for flexible APIs and decorators.
