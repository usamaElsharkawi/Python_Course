# Lecture 50 — Walrus Operator

**Units covered**: 1. What the walrus operator is (`:=`),
2. Avoiding repeated function calls (optimization),
3. `while` loop with input (idiomatic use case),
4. When to use it (readability tradeoff)

---

## Unit 1 — What the walrus operator is (`:=`)

### Core Concept
The walrus operator (`:=`), added in Python 3.8, is an **assignment expression**. It assigns a value to a variable *within* an expression — unlike `=` which is a statement and can't appear inside expressions.

### What's Actually Happening
```python
# Regular assignment (statement) — can't be used inside expressions
data = input("Enter value: ")   # works, but is a statement

# Walrus operator (expression) — can be used inside other expressions
while (data := input("Enter value: ")) != "q":
    print(data)
```

- `(data := input(...))` calls `input()`, assigns the result to `data`, *and* the whole expression evaluates to that value
- The `while` condition checks the evaluated value against `"q"`
- The name "walrus" comes from `:=` resembling a walrus with tusks

### Why It Matters
- Lets you assign and use a value in the same expression
- Reduces repetitive code where you'd otherwise assign first, then check

### Minimal Executable Example
```python
while (data := input("Enter value: ")) != "q":
    print(data)
```

---

## Unit 2 — Avoiding repeated function calls (optimization)

### Core Concept
Without walrus, if you call a function in a condition and then use its result again in the body, the function runs twice. Walrus captures the result once.

### What's Actually Happening
```python
def very_slow_func():
    print("something")   # simulates expensive work
    return 70

# WITHOUT walrus — function called TWICE
if very_slow_func() > 10:
    print(very_slow_func())   # second call!

# WITH walrus — function called ONCE
if (a := very_slow_func()) > 10:
    print(a)   # reuse captured value
```

- Without walrus: `very_slow_func()` runs in the `if` condition, then again in `print()` → "something" prints twice
- With walrus: `(a := very_slow_func())` runs once, stores 70 in `a`, then `print(a)` reuses it → "something" prints once

### Why It Matters
- Critical when the function is expensive (API calls, database queries, heavy computation)
- Eliminates redundant execution while keeping the value available for reuse

### Minimal Executable Example
```python
def very_slow_func():
    print("something")
    return 70

if (a := very_slow_func()) > 10:
    print(a)
```

---

## Unit 3 — `while` loop with input (idiomatic use case)

### Core Concept
The most common walrus pattern: `while (var := input()) != sentinel:` — collect input and test it in one expression.

### What's Actually Happening
```python
while (data := input("Enter the value: ")) != "q":
    print(data)
```

- `input("Enter the value: ")` prompts and returns the user's string
- `:=` assigns it to `data`
- The expression value (the string) is compared to `"q"`
- If not `"q"`, loop body runs with `data` already populated
- If `"q"`, loop exits — `data` still holds `"q"` but body doesn't run
- Blank input → `data = ""` → `"" != "q"` is True → loop continues (user must type `"q"` to quit)

### Why It Matters
- Cleaner than the old pattern:
  ```python
  data = input("Enter value: ")
  while data != "q":
      print(data)
      data = input("Enter value: ")   # duplicate input call
  ```
- Single input call, value immediately available in loop body

### Minimal Executable Example
```python
while (data := input("Enter the value: ")) != "q":
    print(data)
```

---

## Unit 4 — When to use it (readability tradeoff)

### Core Concept
Walrus makes code more concise, but it's not always better. Use it when it removes repetition and improves clarity; avoid it when it makes the expression dense and hard to read.

### What's Actually Happening

| Good use | Bad use |
|---|---|
| `(n := len(items)) > 10` then use `n` | `(x := foo(bar(baz()))) + (x := qux())` — confusing double assignment |
| `while (line := f.readline()) != "":` | Walrus inside a list comprehension with side effects |
| `if (match := pattern.search(text)):` then use `match.group()` | Deeply nested walrus assignments obscuring flow |

### Why It Matters
- Conciseness ≠ readability
- The lecture emphasizes maintainability: code should be understandable by other programmers
- Walrus shines when it eliminates a repeated expensive call or a duplicated `input()` in a loop

### Minimal Executable Example (good use)
```python
# Clean: assign once, reuse
if (n := len(items)) > 10:
    print(f"List has {n} items")
```

---

## Key Insight
The walrus operator (`:=`) is an assignment expression introduced in Python 3.8. It lets you assign a value to a variable within an expression, making it ideal for avoiding repeated expensive function calls and for `while` loops that read input. Use it when it improves clarity — not just to save lines.
