# Lecture 27 — Recursion in Python

**Units covered**: 1. Recursion definition and base case, 2. How recursion works: the breakdown and resolution process, 3. Importance and risks (stack overflow, tree algorithms)

---

## Unit 1 — Recursion Definition and Base Case

### Core Concept
**Recursion** occurs when a function calls itself to solve a problem.
Each recursive call should bring the problem closer to a **base case** —
a condition where the function stops calling itself and returns a direct
answer. Without a base case, the function recurses infinitely until the
program crashes (stack overflow).

### What's Actually Happening

**1. Self-referential function calls**
```python
def fib(n):
    if n == 0 or n == 1:     # Base case
        return n
    return fib(n-2) + fib(n-1)  # Recursive calls
```

When `fib(6)` is called:
1. Python creates a frame for `fib(6)`
2. Since `6 ≠ 0` and `6 ≠ 1`, the function calls `fib(4)` and `fib(5)`
3. Each of those calls creates its own frame
4. Eventually, the calls reach `fib(0)` and `fib(1)`, which hit the
   **base case** and return `0` and `1` respectively
5. The results propagate back up the call stack

**2. The base case prevents infinite recursion**
```python
def countdown(n):
    if n <= 0:        # Base case — stops recursion
        return
    print(n)
    countdown(n - 1)  # Recursive call with smaller problem

countdown(5)
# 5
# 4
# 3
# 2
# 1
```

Without the `if n <= 0: return` check, `countdown` would call itself
with `-1`, `-2`, `-3`, … forever, until the call stack overflows
(`RecursionError`).

**3. CPython call stack and recursion limit**
Each function call adds a **frame object** to the **call stack**.
CPython has a default recursion limit (typically 1000 frames).
Exceeding it raises `RecursionError`.

```python
import sys
print(sys.getrecursionlimit())  # Usually 1000
sys.setrecursionlimit(2000)     # Can increase, but risky
```

### Minimal Executable Example

```python
def factorial(n):
    """Recursive factorial."""
    if n <= 1:      # Base case
        return 1
    return n * factorial(n - 1)

print(factorial(5))  # 120
print(factorial(0))  # 1

# Without base case — infinite recursion
def broken(n):
    return broken(n - 1)

# broken(5)  # RecursionError: maximum recursion depth exceeded
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Missing base case | `def fib(n): return fib(n-1) + fib(n-2)` | `RecursionError` — infinite recursion |
| Wrong base case | `if n == 0: return` for `fib(1)` | `fib(1)` recurses indefinitely |
| Mutating argument | `def f(n): n = n+1; f(n)` | Doesn't help — each call gets a new binding |
| Exponential blowup | Naive Fibonacci | `fib(n)` makes 2 recursive calls → O(2ⁿ) time complexity |

### Key Insight
Every recursive function has:
1. A **base case** — the stopping condition
2. A **recursive case** — the function calls itself with a "smaller" or
   "simpler" input

Without both parts, the function either won't work (`RecursionError`)
or can't make progress.

---

---

## Unit 2 — How Recursion Works: The Breakdown and Resolution Process

### Core Concept
When a recursive function is called, Python builds up a **call tree** of
nested frames. Each call with a non-base-case argument spawns additional
calls until base cases are reached. The final result is computed by
**unwinding** the call stack — small results bubble back up to produce
the final answer.

### What's Actually Happening

**1. The trace of `fib(6)` — building the call tree**
```
fib(6)
├── fib(4)
│   ├── fib(2)
│   │   ├── fib(0) = 0  ← Base case
│   │   └── fib(1) = 1  ← Base case
│   │   → 0 + 1 = 1
│   └── fib(3)
│       ├── fib(1) = 1  ← Base case
│       └── fib(2)
│           ├── fib(0) = 0
│           └── fib(1) = 1
│           → 0 + 1 = 1
│       → 1 + 1 = 2
│   → 1 + 2 = 3
└── fib(5)
    ├── fib(3) → (as above) = 2
    └── fib(4) → (as above) = 3
    → 2 + 3 = 5
→ 3 + 5 = 8
```

The trace from the transcript:
1. `fib(6)` → `fib(4) + fib(5)`
2. `fib(4)` → `fib(2) + fib(3)`
3. `fib(2)` → `fib(0) + fib(1)` → `0 + 1 = 1`
4. `fib(3)` → `fib(1) + fib(2)` → `1 + 1 = 2`
5. `fib(4)` → `1 + 2 = 3`
6. `fib(5)` → `fib(3) + fib(4)` → `2 + 3 = 5`
7. `fib(6)` → `3 + 5 = 8`

**2. CPython frame stacking**
Each `fib(n)` call pushes a **frame** onto the call stack:
1. `CALL_FUNCTION` opcode triggers evaluation
2. A new `PyFrameObject` is allocated for the callee
3. Arguments are bound to local variables
4. Local variables and instruction pointer are saved in the frame
5. When `return` executes, the frame is popped, and the return value is
   passed back

**3. The "smaller problem" principle**
Each recursive call reduces the problem size:
- `fib(n)` depends on `fib(n-1)` and `fib(n-2)`
- These are strictly smaller than `n`
- The base cases (`n=0`, `n=1`) terminate the chain

### Minimal Executable Example

```python
def fib(n):
    if n == 0 or n == 1:  # Base case
        return n
    return fib(n-2) + fib(n-1)  # Recursive case

# Trace visualization
for i in range(7):
    print(f"fib({i}) = {fib(i)}")
# Output: fib(0)=0, fib(1)=1, fib(2)=1, fib(3)=2, fib(4)=3, fib(5)=5, fib(6)=8

# Counting call depth
depth = 0
def traced_fib(n):
    global depth
    indent = "  " * depth
    print(f"{indent}fib({n})")
    depth += 1
    if n <= 1:
        depth -= 1
        return n
    result = traced_fib(n-2) + traced_fib(n-1)
    depth -= 1
    return result

traced_fib(4)
# Shows the full tree traversal with indentation
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Exponential time complexity | `fib(35)` | Takes seconds — 2³⁵ function calls |
| Same value computed multiple times | `fib(4)` computed in multiple branches | No memoization → redundant work |
| Stack depth confusion | Deep recursion with many branches | Risk of `RecursionError` for large inputs |
| Confusing return points | Return value from recursive call ignored | `fib(n-1)` call without `return fib(n-1)` |

### Key Insight
Recursion works by repeatedly breaking a problem into smaller instances
of the same problem. The call stack tracks each recursive invocation.
When a base case is hit, control unwinds back through the stack,
combining partial results into the final answer.

---

## Unit 3 — Importance and Risks of Recursion

### Core Concept
Recursion is a **direct** way to solve problems that are naturally
self-referential (like Fibonacci, factorials, tree traversal). However,
recursive solutions can exhaust the call stack if the base case is
missing, and can be exponentially slow if the same subproblems are
recomputed.

### What's Actually Happening

**1. Why we use recursion**
Problems that fit a recursive structure:
- **Mathematical sequences**: `fib(n) = fib(n-1) + fib(n-2)` — the
  definition itself is recursive.
- **Tree traversal**: A tree node's children are themselves trees.
- **Divide-and-conquer**: Binary search splits the problem in half at
  each step.

Recurrence relations map directly to recursive functions:
```
F(n) = F(n-1) + F(n-2)  →  def fib(n): return fib(n-1) + fib(n-2)
```

**2. The stack overflow risk**
The transcript warns: "if you don't have this base case, this will
keep on running for negative values... your memory will be full and
your program will be crashed."

Without a base case:
- Each call adds a frame to the call stack
- The stack grows until it hits the OS-level limit
- Python raises `RecursionError: maximum recursion depth exceeded`

**3. Mitigation strategies**
```python
import sys
sys.getrecursionlimit()   # Check current limit (default ~1000)

# For deep recursion, consider iteration instead
def fib_iterative(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

**4. Memoization** to avoid recomputation
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)  # Now O(n) instead of O(2ⁿ)
```

### Why It Matters
- **Direct translation**: Recursive problems have an elegant,
  human-readable recursive formulation.
- **Algorithmic technique**: Recursion is foundational for tree
  traversal, graph DFS, backtracking, and divide-and-conquer.
- **Danger zone**: The same elegance can hide exponential complexity or
  stack overflow — every recursive function must have a terminating
  base case and a "smaller problem" argument.

### Minimal Executable Example

```python
# Risk: infinite recursion without base case
def broken(n):
    return broken(n - 1)

# broken(5)   # RecursionError: maximum recursion depth exceeded

# Safe: with base case
def factorial(n):
    if n <= 1:      # Base case
        return 1
    return n * factorial(n - 1)  # Smaller problem

print(factorial(5))  # 120

# Alternative: iterative (no stack growth)
def factorial_iter(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

print(factorial_iter(5))  # 120
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Forgetting base case | `def f(n): f(n-1)` | `RecursionError` — never stops |
| Wrong base case logic | `if n == 1` instead of `n <= 0` | May skip or miss the correct termination |
| Exponential slowdown | Naive `fib(n)` | O(2ⁿ) time; use memoization or iteration |
| Stack limit for deep recursion | `fib(1000)` | Even with base case, may hit `RecursionError` |
| Confusing the return chain | `f(n-1)` without `return` | Result lost — function returns `None` |

### Key Insight
Recursion is powerful for problems with a natural self-similar structure,
but it requires careful attention to two rules: **always have a base
case** (to avoid infinite recursion and stack overflow), and **always
make progress toward the base case** (each call must use a "smaller"
input). When these rules are followed, recursion provides an elegant,
direct solution to complex problems.

---

**End of Lecture 27 — Recursion in Python**

All 3 units documented. Ready for the next step.