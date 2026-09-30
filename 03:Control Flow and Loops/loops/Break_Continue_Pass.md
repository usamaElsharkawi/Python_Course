# Lecture 17: Break, Continue, and Pass Statements

## Unit 1: Loop Control — `break`, `continue`, `pass` Internals

### The Transcript's Version

> **break:** "Cancel the execution of this loop" — stops loop entirely
> **continue:** "Skip this iteration... go to the next iteration" — skips rest of current iteration
> **pass:** "Placeholder that does nothing" — syntax requirement filler

---

### Real Bytecode Analysis

#### `break` — Jump FORWARD Past the Loop

```python
for i in range(21):
    if i == 11:
        break
    print(i)
```

**Bytecode (relevant part):**
```
  3           LOAD_NAME                1 (i)
              LOAD_SMALL_INT          11
              COMPARE_OP              88 (bool(==))
              POP_JUMP_IF_FALSE        3 (to L2)   ← if i != 11, skip break
              NOT_TAKEN

  4           POP_TOP
              JUMP_FORWARD            12 (to L4)   ← ← ← BREAK: jump PAST loop end
```

**`break` = `JUMP_FORWARD` to after `END_FOR`** (label L4). Exits loop entirely.

---

#### `continue` — Jump BACKWARD to `FOR_ITER`

```python
for i in range(1, 20):
    if i == 10:
        continue
    print(i)
```

**Bytecode (relevant part):**
```
  9           LOAD_NAME                1 (i)
              LOAD_SMALL_INT          10
              COMPARE_OP              88 (bool(==))
              POP_JUMP_IF_FALSE        3 (to L6)   ← if i != 10, skip continue
              NOT_TAKEN

 10           JUMP_BACKWARD           12 (to L5)   ← ← ← CONTINUE: jump to FOR_ITER
```

**`continue` = `JUMP_BACKWARD` to `FOR_ITER`** (label L5). Starts next iteration immediately.

---

#### `pass` — Literal `NOP` (No Operation)

```python
for i in range(5):
    if i == 3:
        pass
    print(i)
```

**Bytecode (relevant part):**
```
  2           LOAD_NAME                1 (i)
              LOAD_SMALL_INT           3
              COMPARE_OP              88 (bool(==))
              POP_JUMP_IF_FALSE        2 (to L2)   ← if i != 3, skip pass block
              NOT_TAKEN

  3           NOP                              ← ← ← PASS: does nothing
```

**`pass` = `NOP`** — a single bytecode instruction that does absolutely nothing.

---

### Visual Comparison

```
┌─────────────────────────────────────────────────────────────┐
│ FOR_ITER (get next item)                                    │
│   ↓                                                         │
│ LOOP BODY                                                   │
│   ├── if condition:                                         │
│   │     break    ──→ JUMP_FORWARD ──→ AFTER LOOP (exit)    │
│   │     continue ──→ JUMP_BACKWARD ─→ FOR_ITER (next iter) │
│   │     pass     ──→ NOP (fall through)                    │
│   └── rest of body                                          │
│   ↓                                                         │
│ JUMP_BACKWARD → FOR_ITER                                    │
└─────────────────────────────────────────────────────────────┘
```

| Statement | Bytecode | Effect |
|-----------|----------|--------|
| `break` | `JUMP_FORWARD` to after `END_FOR` | Exit loop entirely |
| `continue` | `JUMP_BACKWARD` to `FOR_ITER` | Start next iteration |
| `pass` | `NOP` | Do nothing, fall through |

---

### Key Insights

#### `break` and `continue` Only Affect the **Innermost** Loop

```python
for i in range(3):
    for j in range(3):
        if j == 1:
            break      # Only breaks INNER loop
        print(i, j)
```

Output:
```
0 0
1 0
2 0
```

The outer loop continues.

---

#### `pass` Is Required Because Python Has No Empty Blocks

```python
if condition:
    # SyntaxError: expected statement
    pass  # OK: valid empty block

while waiting:
    pass  # Busy-wait loop (burns CPU!)

class Placeholder:
    pass  # Valid empty class

def todo():
    pass  # Valid empty function
```

---

#### `else` Clause on Loops (Bonus — Not in Transcript)

```python
for i in range(5):
    if i == 3:
        break
else:
    print("Loop completed without break")
```

**Output:** (nothing — `break` skipped `else`)

```python
for i in range(5):
    if i == 10:
        break
else:
    print("Loop completed without break")
```

**Output:** `Loop completed without break`

**Bytecode:** `FOR_ITER` on normal exhaustion jumps to `else` block; `break` jumps past it.

---

### Key Takeaways

1. **`break` = `JUMP_FORWARD`** — exits loop, continues after loop
2. **`continue` = `JUMP_BACKWARD` to `FOR_ITER`** — skips to next iteration
3. **`pass` = `NOP`** — literally does nothing, satisfies syntax
4. **All three only affect innermost loop**
5. **`else` on loop** runs only if loop *wasn't* broken out of

---

### Files Created
- `break_continue.py` — transcript examples with bytecode
- `pass_stmt.py` — pass statement bytecode
---

# Unit 2: Practical Patterns — Search, Validation, Retry, Nested Control

---

## 1. Search Loop — `break` + `else`

```python
items = ["apple", "banana", "cherry", "date"]
target = "cherry"

for item in items:
    if item == target:
        print(f"Found: {item}")
        break
else:
    print("Not found")
```

**Why `else` on loop?** Runs only if loop *completed* without `break`. Cleaner than a `found` flag.

---

## 2. Input Validation — `while True` + `continue` + `break`

```python
while True:
    age = input("Enter age (or 'q' to quit): ")
    if age == 'q':
        break
    if not age.isdigit():
        print("Please enter a number")
        continue
    age = int(age)
    if age < 0 or age > 150:
        print("Unrealistic age")
        continue
    print(f"Valid age: {age}")
    break
```

**Pattern:** `while True` + `continue` for validation + `break` on success.

---

## 3. Retry Logic — `for` + `continue` + `else`

```python
import time

max_retries = 3
for attempt in range(1, max_retries + 1):
    try:
        result = risky_operation()
        print("Success!")
        break
    except ConnectionError:
        print(f"Attempt {attempt} failed")
        if attempt < max_retries:
            time.sleep(1)
            continue
else:
    print("All retries exhausted")
```

**`else` on `for`** — runs only if all retries failed (no `break`).

---

## 4. Filter in Loop — `continue` as Guard

```python
numbers = [1, -2, 3, -4, 5, 0, 6]

for n in numbers:
    if n <= 0:
        continue          # skip negatives and zero
    print(f"Processing {n}")
```

Output:
```
Processing 1
Processing 3
Processing 5
Processing 6
```

---

## 5. Nested Loop Control — Breaking Outer Loop

```python
# Problem: break only exits inner loop
for i in range(3):
    for j in range(3):
        if i == 1 and j == 1:
            break        # Only breaks inner!
    print(f"Outer: {i}")
```

**Solutions:**

```python
# Option 1: Flag variable
found = False
for i in range(3):
    for j in range(3):
        if i == 1 and j == 1:
            found = True
            break
    if found:
        break

# Option 2: Function with return
def search():
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                return (i, j)

# Option 3: Exception (rare but valid)
class Found(Exception):
    pass

try:
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                raise Found((i, j))
except Found as e:
    print(e.args[0])
```

---

## 6. `pass` as Structural Placeholder

```python
# Skeleton code - implement later
def process_user(user):
    if user.is_admin:
        pass  # TODO: admin logic
    elif user.is_premium:
        pass  # TODO: premium logic
    else:
        pass  # TODO: basic logic

# Abstract base class
class Animal:
    def speak(self):
        pass  # Subclasses must override
```

---

## 7. Infinite Loop with `break` — Menu Pattern

```python
while True:
    print("\n1. View\n2. Edit\n3. Quit")
    choice = input("Choose: ")
    
    if choice == '1':
        view_data()
    elif choice == '2':
        edit_data()
    elif choice == '3':
        break
    else:
        print("Invalid choice")
```

Clean, readable, standard Python pattern.

---

## Key Patterns Summary

| Pattern | Keywords | Use Case |
|---------|----------|----------|
| Search + `else` | `break`, `else` | Find item, handle not-found |
| Validation loop | `while True`, `continue`, `break` | Input sanitization |
| Retry with `else` | `for`, `continue`, `break`, `else` | Network/IO retries |
| Filter in loop | `continue` | Skip unwanted items |
| Nested break | Flag / function / exception | Exit multiple levels |
| Skeleton | `pass` | Placeholder for later |

---

## Key Takeaways (Unit 2)

1. **`break` + `else`** — idiomatic search pattern, avoids flag variables
2. **`while True` + `continue`** — standard validation loop
3. **`for` + `else`** — retry logic, runs `else` only if no `break`
4. **`continue` as guard clause** — filter early, reduce nesting
5. **Nested `break`** — needs flag, function, or exception (no labeled break)
6. **`pass` for scaffolding** — TODO markers, abstract methods

---

### Files Created (Unit 2)
- `patterns.py` — all practical patterns above
