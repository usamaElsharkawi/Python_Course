# Lecture 13: If-Else Conditional Statements

---

## Unit 1: The `if` Statement and Indentation

### The Transcript's Version

> "These four spaces are telling the Python interpreter that this line is inside the if statement. This is called indentation."

### The Real Version

Indentation isn't a formatting convention you should follow. **It's part of the syntax.**

Python has no `{}` braces, so whitespace is the *only* mechanism that defines a block. The tokenizer literally emits `INDENT` and `DEDENT` tokens:

```python
if age > 18:      ← NEWLINE
    print(...)    ← INDENT token (4 spaces)
    print(...)
print("End")      ← DEDENT token closes the block
```

The parser builds the `if` body from the span between `INDENT` and `DEDENT`. That's why `print("End of program")` runs regardless — the `DEDENT` already closed the block before it.

### Real Token Stream

Verified output from Python 3.14's `tokenize` module for:

```python
age = 32
if age > 18:
    print("You can drive")
    print("Thank you")
print("End of program")
```

```
NAME     'age'
OP       '='
NUMBER   '32'
NEWLINE  '\n'
NAME     'if'
NAME     'age'
OP       '>'
NUMBER   '18'
OP       ':'
NEWLINE  '\n'
INDENT   '    '          ← ← ← a real TOKEN
NAME     'print'
OP       '('
STRING   '"You can drive"'
OP       ')'
NEWLINE  '\n'
NAME     'print'
OP       '('
STRING   '"Thank you"'
OP       ')'
NEWLINE  '\n'
DEDENT   ''             ← ← ← and this one
NAME     'print'
OP       '('
STRING   '"End of program"'
OP       ')'
NEWLINE  '\n'
```

`INDENT` and `DEDENT` are first-class tokens with numeric type codes, sitting alongside `NAME`, `NUMBER`, and `OP`.

**How the tokenizer decides:**

1. Measure the line's leading whitespace
2. Compare it to a stack of open indent levels
3. Deeper → emit `INDENT`
4. Shallower → emit `DEDENT` (possibly several, to unwind multiple levels)
5. Same → emit nothing

The parser then builds a block node from everything between an `INDENT` and its matching `DEDENT`.

```
Line 3:  INDENT   ──┐
Line 4:            ├──▶ this span becomes the "suite" (body) of the if
Line 5:  DEDENT   ──┘

Line 6 is OUTSIDE, because its DEDENT already closed the block.
```

### Why Python Works This Way

Guido van Rossum designed Python this way deliberately. C-family languages use braces and treat indentation as optional sugar:

| Language | Block delimiter | Indentation |
|----------|----------------|-------------|
| C, Java, JS | `{ }` | Cosmetic, optional |
| **Python** | **None** | **Mandatory, structural** |

Deleting the braces means the whitespace *must* carry structural meaning. The cost is strictness (`IndentationError`); the benefit is that blocks are unambiguous and the language reads like plain English.

### Indentation Errors Are Parse Errors

They happen **before your program runs**, not during:

```python
if True:
print("no indent")
```
```
IndentationError: expected an indented block after 'if' statement on line 1
```

```python
if age > 18:
    print("drive")
  print("oops")   # 2 spaces instead of 4
```
```
IndentationError: unindent does not match any outer indentation level
```

Neither program executed a single statement. The failure happened during **parsing**.

**Rules:**
- Use 4 spaces per level (the convention; tabs also work but never mix them in one file)
- Indent consistently — a jump back to a *shallower but previously-used* level is legal, any other jump is an error
- A block header ending in `:` **must** be followed by an indented suite

### What the Condition Actually Does

The condition doesn't have to be a boolean. Python calls `PyObject_IsTrue()` on it — the **truthiness** rule from the Operators lecture — then jumps.

Real CPython bytecode for:

```python
age = 32
if age > 18:
    print("You can drive")
```

```
  2           LOAD_NAME                0 (age)
              LOAD_SMALL_INT          18
              COMPARE_OP             148 (bool(>))     ← produces True/False
              POP_JUMP_IF_FALSE       17 (to L1)       ← jumps past block if False
              NOT_TAKEN

  3           LOAD_NAME                1 (print)
              PUSH_NULL
              LOAD_CONST               1 ('You can drive')
              CALL                     1
              POP_TOP
```

**Key points:**

1. `COMPARE_OP` performs the `>` and produces a real `bool`
2. `POP_JUMP_IF_FALSE` is the actual branch — a **jump instruction**
3. There is **no runtime `IfStatement` object** in memory holding a condition
4. The compiler resolved the branch at **compile time**

So the `if` is not a value, not an object, not a container. It's control flow encoded as an offset in the instruction stream.

### Truthiness Applies Here Too

Because `PyObject_IsTrue()` is used, any object works as a condition:

```python
if "hello":     # non-empty string → truthy
    ...

if 0:           # zero → falsy
    ...         # skipped

if []:          # empty list → falsy
    ...         # skipped

if None:        # falsy
    ...         # skipped
```

This is the **same mechanism** as `bool()`, `and`, `or`, and `not` from Lecture 5.

### The Body Is Called a "Suite"

In Python's grammar it's a *suite*, and it can contain **any number of statements**:

```python
if age > 18:
    print("You can drive")     # statement 1 in the suite
    print("Thank you")         # statement 2 in the suite
    print("Anything else")      # statement 3 — all three are conditional
    x = 10                      # assignments are fine too
    y = x * 2                   # still the suite
```

No limit. They all run together, or none of them do.

### The `if` With No `else`

The transcript's first example had no `else` — and that's valid. When the condition is false, the suite is simply skipped and execution continues with whatever comes after the block:

```python
age = 12
if age > 18:
    print("You can drive")     # skipped
    print("Thank you")         # skipped
print("End of program")        # always runs
```

Output:
```
End of program
```

**An `if` without `else` is a complete, valid statement.** `else` is optional.

### Key Takeaways

1. Indentation is **grammar**, not style — `INDENT`/`DEDENT` are real tokens
2. `DEDENT` is what "exits" a block, which is why code after it always runs
3. Wrong indentation = `IndentationError` at parse time, before execution
4. The condition uses **truthiness** (`PyObject_IsTrue()`), not just `True`/`False`
5. The `if` compiles to a **jump instruction**, not a runtime object
6. The body is a *suite* — unlimited statements, all-or-nothing
7. Python has no braces — whitespace is the only block delimiter
8. `else` is optional; a bare `if` is a complete statement
9. Use 4 spaces per level; never mix tabs and spaces in one file

---

# Unit 2: `else` — The Second Branch

## Core Truth

`if`/`else` is **exhaustive**: exactly one of the two suites runs. Always. There's no third outcome, and neither can both run.

## What `else` Costs at the Bytecode Level

Real CPython output for the transcript's program:

```python
age = int(input("Enter age: "))
if age > 18:
    print("You can drive")
else:
    print("You cannot drive")
print("End of program")
```

```
  2           LOAD_NAME                2 (age)
              LOAD_SMALL_INT          18
              COMPARE_OP             148 (bool(>))
              POP_JUMP_IF_FALSE       10 (to L1)      ← false → go to else
              NOT_TAKEN

  3           LOAD_NAME                3 (print)      ← the IF body
              PUSH_NULL
              LOAD_CONST               1 ('You can drive')
              CALL                     1
              POP_TOP
              JUMP_FORWARD             8 (to L2)      ← ← ← skip the else

  5   L1:     LOAD_NAME                3 (print)      ← the ELSE body
              PUSH_NULL
              LOAD_CONST               2 ('You cannot drive')
              CALL                     1
              POP_TOP

  6   L2:     LOAD_NAME                3 (print)      ← code after
              PUSH_NULL
              LOAD_CONST               3 ('End of program')
              CALL                     1
              POP_TOP
              LOAD_CONST               4 (None)
              RETURN_VALUE
```

**Compare with Unit 1.** There was no `JUMP_FORWARD`, because there was no `else` to skip over. Adding `else` introduces exactly one extra instruction.

The logic reads:

> If the condition is false, jump to the else body. Otherwise fall through into the if body, run it, then **jump forward past the else** so the else never runs.

That `JUMP_FORWARD` is the entire cost of `else`. It exists purely to prevent falling into the second branch.

```
        condition
       /         \
    [TRUE]      [FALSE]
       |           |
    if body     else body
       |           |
       └─────>  <───┘
           join point (L2)
```

## Exactly One Branch Always Runs

The transcript tested this with real input:

| Input | Output |
|-------|--------|
| 45 | `You can drive` |
| 65 | `You can drive` |
| 15 | `You cannot drive` |
| 1 | `You cannot drive` |

There's no scenario where both print, and no scenario where neither prints.

## When to Omit `else` — And When Not To

The transcript showed both patterns, and said the bare `if` is fine. That's right, but the choice isn't arbitrary. The question is:

> **"Is there a meaningful second case, or is 'otherwise, do nothing' the real behavior?"**

**Keep `else` when the two cases are genuinely different actions:**

```python
if age > 18:
    print("You can drive")
else:
    print("You cannot drive")
```

Removing `else` here would lose information. "Not old enough" is a real state worth responding to.

**Omit `else` when the alternative is genuinely nothing:**

```python
if age > 18:
    print("You can drive")
    print("Thank you")
print("End of program")
```

Here there's no meaningful second case — a 12-year-old just... doesn't get those two lines. Adding `else: pass` would be noise.

**The rule:** if you'd be tempted to write `else: pass`, omit the `else`.

## The Common Mistake: Branches That Do the Same Thing

This is the trap in the lecture's framing of "either if or else is executed." A branch is pointless if it does what the fall-through already does:

```python
age = 34

if age > 18:
    print("You can drive")
else:
    print("You can drive")     # same work — this branch is dead weight
```

Correct form — no conditional at all:

```python
age = 34
print("You can drive")
```

More generally, whenever both branches are identical, the condition is irrelevant and should be deleted. A condition should only exist to *choose between different behaviors*.

## A Subtlety: `else` Attaches to the Nearest `if`

Without `elif`, nesting produces surprising results:

```python
if a:
    if b:
        print("both")
    else:
        print("only a")     # ← this else binds to `if b`, NOT `if a`
```

Readers almost always assume it binds to the outer `if`. Python binds it to the inner one. This is the classic **dangling else**, and it's the reason `elif` exists — which is exactly Unit 3.

## Key Takeaways

1. `if`/`else` is **exhaustive** — exactly one suite runs, always
2. `else` compiles to a jump target plus one extra `JUMP_FORWARD`
3. The `JUMP_FORWARD` exists to skip the else body after the if body runs
4. Without `else` there is nothing to skip, so no extra jump
5. Omit `else` when the real alternative is "do nothing"
6. Keep `else` when the two cases are genuinely different actions
7. If both branches do the same work, **delete the conditional entirely**
8. `else` binds to the **nearest** `if` — the dangling-else problem

---

# Unit 3: `elif` Ladders — First Match Wins
