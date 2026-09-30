# Lecture 16: While Loops in Python

## Unit 1: The `while` Loop — Condition-Checked Iteration

### The Transcript's Version

> "While loop runs until this condition is true."
> 
> ```python
> i = 1
> while i < 6:
>     print(i)
>     i = i + 1
> ```
> 
> Dry run: i=1 → check 1<6 ✓ → print 1 → i=2 → check 2<6 ✓ → print 2 → ... → i=6 → check 6<6 ✗ → exit

---

### The Real Version: Bytecode Mechanism

```python
i = 1
while i < 6:
    print(i)
    i = i + 1
```

**Bytecode (CPython 3.14):**
```
  1           LOAD_SMALL_INT           1
              STORE_NAME               0 (i)

  2   L1:     LOAD_NAME                0 (i)       ← top of loop: load i
              LOAD_SMALL_INT           6
              COMPARE_OP              18 (bool(<)) ← i < 6 ?
              POP_JUMP_IF_FALSE       20 (to L2)    ← False → exit loop
              NOT_TAKEN

  3           LOAD_NAME                1 (print)
              PUSH_NULL
              LOAD_NAME                0 (i)
              CALL                     1
              POP_TOP

  4           LOAD_NAME                0 (i)
              LOAD_SMALL_INT           1
              BINARY_OP                0 (+)        ← i + 1
              STORE_NAME               0 (i)         ← store back to i
              JUMP_BACKWARD           26 (to L1)    ← ← unconditional jump to top

  2   L2:     LOAD_CONST               1 (None)
              RETURN_VALUE
```

**Key difference from `for` loop:**
| `for` loop | `while` loop |
|------------|--------------|
| `GET_ITER` → `FOR_ITER` (auto next + StopIteration) | Manual condition check: `COMPARE_OP` → `POP_JUMP_IF_FALSE` |
| Iterator protocol | Arbitrary boolean expression |
| `JUMP_BACKWARD` to `FOR_ITER` | `JUMP_BACKWARD` to condition label (L1) |

---

### The Condition Is Re-Evaluated Every Iteration

Unlike `for` where the iterable is fixed at start, `while` re-evaluates the **entire condition expression** each time:

```python
n = 5
while n > 0:
    print(n)
    n = 100  # Changes condition for NEXT iteration!
```

Output:
```
Iteration 1: n=5, 5>0 ✓, print 5, n=100
Iteration 2: n=100, 100>0 ✓, print 100, n=100
Iteration 3: n=100, 100>0 ✓, print 100... infinite!
```

The condition is **live** — changes to variables inside the loop affect the next check.

---

### `while True` — The Intentional Infinite Loop

```python
while True:
    print(i)
    i = i + 1
```

**Bytecode:**
```
  2   L1:     NOP                       ← no condition check!
  3           LOAD_NAME                1 (print)
              ...
              JUMP_BACKWARD           20 (to L1)   ← unconditional jump forever
```

- `True` is a constant → compiler optimizes away the check entirely
- Just `NOP` (no-op) at loop top
- Pure `JUMP_BACKWARD` — runs until `break`, `return`, `sys.exit()`, or `Ctrl+C`

---

### Accidental Infinite Loop (Transcript Example)

```python
i = 1
while i < 6:
    print(i)
    i + 1        # BUG: missing assignment! i never changes
```

**What happens:**
1. `i` stays `1` forever
2. Condition `1 < 6` always True
3. `print(1)` runs infinitely
4. `i + 1` computes `2` but discards it
5. System hangs → need `Ctrl+C` or kill terminal

**The fix:** `i = i + 1` (or `i += 1`)

---

### While vs For — When to Use Which

| Scenario | Use |
|----------|-----|
| Known number of iterations / iterating a sequence | `for` |
| Unknown iterations / condition-based | `while` |
| "Repeat until X happens" | `while` |
| Iterator protocol available | `for` |
| Complex condition involving multiple variables | `while` |

```python
# For: definite iteration
for i in range(10): ...

# While: indefinite iteration
while not done:
    done = check_condition()

# While: complex condition
while x > 0 and y < 100 and not flag:
    ...
```

---

### Key Takeaways

1. **`while` = condition check + jump back** — `COMPARE_OP` → `POP_JUMP_IF_FALSE` → body → `JUMP_BACKWARD`
2. **Condition re-evaluated every iteration** — live, not fixed like `for`'s iterable
3. **`while True` compiles to unconditional jump** — `NOP` + `JUMP_BACKWARD`, no check
4. **Missing variable update = infinite loop** — most common `while` bug
5. **No automatic iteration** — you control everything (initialization, condition, update)
6. **Use `for` when possible** — harder to write infinite loops accidentally

---

### Files Created
- `while_loop_basics.py` — transcript examples
- `while_loop_bytecode.py` — bytecode inspection
- `infinite_loop.py` — infinite loop demonstration