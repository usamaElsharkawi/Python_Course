# Study Approach for Python Course

## Methodology

For each lecture/section:

1. **Divide into focused units** — One unit per response, each covering a single coherent concept
2. **Deep internals-first understanding** — Go beyond the lecture transcript:
   - Python object model (`PyObject`, reference counting, memory layout)
   - CPython implementation details where relevant
   - Why the language works this way, not just how
3. **Interactive discussion** — Pause after each unit for questions, clarification, edge cases
4. **Document in lecture folder** — After completing all units for a lecture, consolidate into a `.md` file in the lecture folder with:
   - Unit summaries with key insights
   - Code examples demonstrating internals
   - Common pitfalls / "gotchas"
   - Personal notes / mental models

## Unit Template

Each unit response should cover:
- **Core concept** (what the lecture teaches)
- **What's actually happening** (internals, memory, object model)
- **Why it matters** (bugs, performance, design decisions)
- **Minimal executable examples** you can run and modify

## Workflow

```
Lecture → Split into N units → Discuss Unit 1 → Discuss Unit 2 → ... → Discuss Unit N
                                                             ↓
                                                   Create lecture .md file
```

## Lecture Schedule

| # | Lecture | File | Status |
|---|---------|------|--------|
| 1 | Variables and Data Types in Python | `Variables_and_Data_Types.md` | ✅ Complete |
| 2 | Typecasting in Python | `Typecasting.md` | ✅ Complete |
| 3 | Taking User Input in Python | `Taking_User_Input.md` | ✅ Complete |
| 4 | Comments, Escape Sequences & Print Statement | `Comments_Escape_Sequences.md` | ✅ Complete |
| 5 | Operators in Python | TBD | 🔜 Upcoming |
| 6 | Coding Exercise 2: Understanding Escape Sequence Characters | TBD | 🔜 Upcoming |
| 7 | Practice Set 1 | TBD | 🔜 Upcoming |

## Completed: Lecture 1 — Variables and Data Types in Python

**File**: `02:Python fundamentals/Variables_and_Data_Types.md`

**Units covered**:
1. Variables as memory locations — Python's object model, assignment semantics, reference semantics
2. Dynamic typing — PyObject header, type tags, type inference
3. Variable naming rules — identifier syntax, Unicode, keywords, dunder
4. Built-in scalar types (int, float, str, bool) — internal representation, immutability
5. Collection types overview — mutability, hashability, memory layout

## Completed: Lecture 2 — Typecasting in Python

**File**: `02:Python fundamentals/Typecasting.md`

**Units covered**:
1. What is typecasting? — The concept and why it exists
2. The four typecasting functions — int(), str(), float(), bool() — internal behavior, truncation, edge cases

## Completed: Lecture 3 — Taking User Input in Python

**File**: `02:Python fundamentals/Taking_User_Input.md`

**Units covered**:
1. The input() function — always returns a string, how it works, prompts
2. The string problem — int(input()) pattern, + operator with strings vs integers

## Completed: Lecture 4 — Comments, Escape Sequences & Print Statement

**File**: `02:Python fundamentals/Comments_Escape_Sequences.md`

**Units covered**:
1. Comments — single-line (`#`), multi-line (`'''`), VSCode Ctrl+/
2. Escape Sequences — `\n`, `\t`, `\\`, `\"`, `\'`
3. Print Statement — `sep` and `end` parameters

---

*Next: Lecture 5 — Operators in Python*
