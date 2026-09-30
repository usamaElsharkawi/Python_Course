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