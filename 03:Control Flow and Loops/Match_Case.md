# Lecture 14: Match Case Statements

## Unit 1: The `match` Statement and Basic Pattern Matching

### What `match` Actually Is

The transcript introduces `match` as "similar to switch case" — that's the *spirit*, but the **mechanism is different**.

In C/Java/JS, `switch` is a jump table: compile-time constant values → O(1) jump table lookup.

Python's `match` is **not** a jump table. It's a **pattern-matching engine** evaluated at runtime, case by case, top to bottom. The first match wins.

---

### Basic Syntax (from transcript)

```python
a = 34
match a:
    case 1:
        print("The value is 1")
    case 3:
        print("The value is 3")
    case 6:
        print("The value is 6")
    case _:
        print("Better luck next time")
```

- `match` evaluates the subject (`a`) **once**
- Each `case` is a pattern to match against
- `case _` is the wildcard/default — matches anything not caught above
- **No parentheses needed** around the subject (optional for complex expressions)

---

### The Real Bytecode Mechanism

```python
num = 3
match num:
    case 1:
        print("one")
    case 2 | 3:
        print("two or three")
    case _:
        print("other")
```

Bytecode (CPython 3.14):
```
  2           LOAD_NAME                0 (num)      ← load the SUBJECT

  3           COPY                     1              ← duplicate subject
              LOAD_SMALL_INT           1
              COMPARE_OP              88 (bool(==))  ← case 1: subject == 1?
              POP_JUMP_IF_FALSE       12 (to L1)      → no → jump to L1
              NOT_TAKEN

  4           POP_TOP
              ...print "one"...
              RETURN_VALUE

  5   L1:     COPY                     1              ← case 2 | 3: duplicate subject
              LOAD_SMALL_INT           2
              COMPARE_OP              88 (bool(==))  ← subject == 2?
              POP_JUMP_IF_FALSE       2 (to L2)
              NOT_TAKEN
              JUMP_FORWARD            10 (to L4)     ← matched 2 → skip to body

      L2:     COPY                     1              ← try 3
              LOAD_SMALL_INT           3
              COMPARE_OP              88 (bool(==))  ← subject == 3?
              POP_JUMP_IF_FALSE       2 (to L3)
              NOT_TAKEN
              JUMP_FORWARD             2 (to L4)

      L3:     POP_TOP
              JUMP_FORWARD            11 (to L5)     ← neither 2 nor 3 → continue

      L4:     POP_TOP
              ...print "two or three"...
              RETURN_VALUE

  7   L5:     NOP
              ...print "other"...
              RETURN_VALUE
```

---

### Key Observations from the Bytecode

#### 1. The subject is evaluated **once**, then copied for each comparison

`COPY 1` duplicates the subject on the stack so each comparison can consume one copy.

#### 2. Each literal case = one equality comparison

```
case 1:       COMPARE_OP (==) 1
case 2 | 3:   COMPARE_OP (==) 2, then COMPARE_OP (==) 3
```

The OR pattern `2 | 3` compiles to **two separate equality checks** with a jump between them.

#### 3. `RETURN_VALUE` after every match body

This is the critical part. **After a match body runs, the function returns immediately.** There's no fall-through, no implicit break, no continuing to the next case.

```python
match num:
    case 1:
        print("one")
    case 2:
        print("two")
```

If `num == 1`, the bytecode hits `RETURN_VALUE` after printing "one" and the function exits. It never reaches the `case 2` check.

#### 4. The wildcard `_` is just the final fallback

```python
case _:
```

Compiles to nothing special — it's just the code after all explicit cases fail. No comparison, no jump, just "if you got here, run this."

---

### The Matching Algorithm (What Actually Happens)

```
SUBJECT = evaluate the expression after `match`

for each CASE in order:
    if PATTERN matches SUBJECT:
        BIND any capture variables
        RUN the case body
        RETURN (function exits)
# If we get here, no case matched
raise MatchError  (if no wildcard _ case)
```

**First match wins. Evaluation stops at the first match. No fall-through.**

---

### The Subject Is Evaluated Once

```python
match get_user_input():
    case "yes":
        ...
    case "no":
        ...
```

`get_user_input()` is called **once**, its result stored, then compared against each case. It's not re-evaluated.

---

### What Counts as a "Match" (Preview of Units 2-3)

| Pattern Type | Example | Matches |
|--------------|---------|---------|
| **Literal** | `case 1:`, `case "hello":` | Exact equality (`==`) |
| **Wildcard** | `case _:` | Everything (binds nothing) |
| **OR** | `case 1 \| 2 \| 3:` | Any of the alternatives |
| **Capture** | `case x:` | Anything, binds to `x` |
| **Guard** | `case x if x > 0:` | Capture + condition |
| **Sequence** | `case [a, b]:` | List/tuple of length 2 |
| **Mapping** | `case {"name": n}:` | Dict with key "name" |
| **Class** | `case Point(x=0, y=0):` | Instance with attrs |

---

### Why It Was Added (Python 3.10)

The transcript says "convenience." The deeper reason: **structural pattern matching** enables concise, readable code for data-driven logic — especially for parsing, AST visitors, command dispatch, and protocol handling — where you're matching *shape* of data, not just values.

```python
# Before: verbose if/elif with manual destructuring
if isinstance(msg, dict) and msg.get("type") == "join":
    room = msg.get("room")
    user = msg.get("user")
    ...

# After: declarative
match msg:
    case {"type": "join", "room": room, "user": user}:
        ...
    case {"type": "leave", "room": room}:
        ...
    case {"type": "msg", "from": user, "text": text}:
        ...
```

---

### Transcript Example Walkthrough

```python
# User enters a lucky number
a = int(input("Enter a number between 1 and 10: "))

match a:
    case 1:
        print("You won a charger!")
    case 3:
        print("You won $3!")
    case 6:
        print("You won a camera!")
    case _:
        print("Better luck next time")
```

**Execution trace for input `3`:**
1. `a = 3` (subject evaluated once)
2. `case 1`: `3 == 1` → False → jump to next
3. `case 3`: `3 == 3` → True → execute body → `RETURN_VALUE` → done
4. Cases 6 and `_` never evaluated

---

### Key Takeaways

1. **`match` is structural pattern matching, not a jump table** — sequential, first-match-wins
2. **Subject evaluated once** — then copied for each pattern comparison
3. **Literal patterns use `==`** — OR patterns expand to sequential equality checks
4. **First match wins, then `RETURN_VALUE`** — no fall-through, function exits
5. **Wildcard `_` is the fallback** — no comparison, just "everything else"
6. **Capture patterns bind variables** — `case x:` binds the subject to `x`
7. **Guards add conditions** — `case x if x > 0:`
8. **Order matters** — specific patterns first, general/wildcard last
9. **`match` is an expression in Python 3.11+** (walrus-style), but statement in 3.10

---

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "It's a switch statement" | No jump table. Sequential pattern matching. |
| "Cases fall through" | **Never.** First match exits the function. |
| "It's just syntax sugar for if/elif" | Different mechanism. `match` does structural pattern matching with binding. |
| "It's only for literals" | Matches data *structure* and binds variables. |

---

### Files Created
- `match_case_demo.py` — transcript example with input
- `match_case_bytecode.py` — bytecode inspection script