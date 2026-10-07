# Next Session: Gap Review Plan

## Identified Gaps (from Quiz Results)

### 1. **Mutable Default Arguments** (Question 17 - MISSED)
- **Concept:** Default arguments evaluated once at function definition time
- **Gotcha:** Mutable defaults (lists, dicts) shared across all calls
- **Fix:** Use `None` and create inside function
- **Study:** `function.__defaults__` tuple, when evaluation happens

### 2. **Lambda Late-Binding Closure** (Question 11 - MISSED)
- **Concept:** Lambdas capture variables BY REFERENCE, not value
- **Gotcha:** Loop variable captured, all lambdas see final value
- **Fix:** `lambda i=i: i` (default argument captures value at creation)
- **Study:** Closure mechanics, `__closure__` attribute, late vs early binding

### 3. **Module Import Caching** (Question 14 - initially uncertain)
- **Concept:** Modules cached in `sys.modules`, subsequent imports return same object
- **Gotcha:** Module code runs only once; mutations persist
- **Study:** `sys.modules`, `importlib.reload()`, when module code executes

---

## Review Session Structure (Next Session)

1. **Deep Dive: Mutable Default Arguments** (15 min)
   - Why it happens (function object `__defaults__` tuple)
   - Visualizing the shared object
   - Correct patterns and anti-patterns

2. **Deep Dive: Lambda Late Binding** (15 min)
   - Closure mechanics: capture by reference vs value
   - `__closure__` inspection
   - Default argument capture trick
   - When to use `functools.partial` instead

3. **Deep Dive: Module System** (15 min)
   - `sys.modules` cache
   - `import` vs `from ... import`
   - Circular imports
   - `importlib.reload()`

4. **Practice Quiz** (15 min)
   - 5 targeted questions on these three topics

---

## Practice Quiz Questions (for next session)

### Q1: Mutable Default
```python
def add(x, lst=[]):
    lst.append(x)
    return lst

print(add(1))  # ?
print(add(2))  # ?
```

### Q2: Lambda in Loop
```python
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])  # ?
```

### Q3: Module Import
```python
# mod.py
val = 1

# main.py
import mod
mod.val = 2
import mod
print(mod.val)  # ?
```

### Q4: Function Introspection
```python
def f(a, b=5, *args, **kw):
    pass

print(f.__code__.co_argcount)  # ?
print(f.__defaults__)          # ?
```

### Q5: Closure Inspection
```python
def outer(n):
    def inner(x):
        return x + n
    return inner

f = outer(7)
print(f.__closure__[0].cell_contents)  # ?
```

---

## After Review → Section 6

Section 6 topics (based on typical Python curriculum):
- File I/O (`open`, `with`, `json`, `csv`)
- Exception handling (`try/except/finally/else`)
- Working with external APIs
- Virtual environments & `pip` deeper
- Testing basics (`unittest`, `pytest`)

---

**Ready for next session!**