# Lecture 4: Comments, Escape Sequences & Print Statement

---

## Unit 1: Comments — Single-Line, Multi-Line, and VSCode Shortcuts

### Core Truth
**Comments are ignored by the Python interpreter.** They exist solely for human readers — developers documenting, explaining, or temporarily disabling code. The `#` character marks everything after it as a comment until the end of the line.

### Single-Line Comments

```python
# This is a comment — Python ignores everything after #
print("Hello")  # This is also a comment — after the code on the same line
```

```
Memory:
┌─────────────────────────────────────────────┐
│ # This is a comment                        │  ← NOT stored, NOT processed
│ print("Hello")  # inline comment           │  ← Only "Hello" is processed
└─────────────────────────────────────────────┘
```

**The `#` character tells the tokenizer to skip everything until the next newline.**

### Multi-Line Comments — Triple Single Quotes

```python
# Method 1: Multiple # comments
# Line 1
# Line 2
# Line 3

# Method 2: Triple single quotes
'''
This is a multi-line comment.
Python ignores everything between these triple quotes.
'''
```

```
Memory:
┌─────────────────────────────────────────────┐
│ '''                                        │  ← NOT stored
│ This is a multi-line comment.              │  ← NOT stored
│ Python ignores everything between...       │  ← NOT stored
│ '''                                        │  ← NOT stored
└─────────────────────────────────────────────┘
```

**Key insight**: Triple-quoted strings (`'''...'''`) that are not assigned to a variable are treated as **docstrings** — they're technically string literals but not bound to anything, so they're effectively ignored.

### VSCode Shortcut — Ctrl+/

```python
# Before commenting:
print("Hello")
print("World")

# After Ctrl+/:
# print("Hello")
# print("World")
```

**VSCode adds `#` to the beginning of each selected line.** This is a VSCode feature, not a Python feature.

### Why Comments Exist

```python
# For other developers reading the code
# Arjun, please finish this code
# Rohan, please review what Arjun has done

# For temporarily disabling code
# print("Debug: this line is disabled")
```

**Comments are for humans, not the interpreter.** The Python interpreter never sees them.

### Under the Hood

```python
# When Python tokenizes this:
x = 5  # comment

# The tokenizer produces:
# Token: NAME 'x'
# Token: OP '='
# Token: NUMBER '5'
# Token: COMMENT '# comment'  ← ignored by parser
# Token: NEWLINE '\n'
```

The `COMMENT` token is generated but **discarded by the parser** — it never becomes part of the AST (Abstract Syntax Tree).

### Key Takeaways

1. **`#` marks single-line comments** — everything after `#` to end of line is ignored
2. **`'''...'''` marks multi-line comments** — everything between triple quotes is ignored
3. **Ctrl+/** is a VSCode shortcut** — adds/removes `#` on selected lines
4. **Comments are for developers** — the interpreter never processes them
5. **Comments can disable code** — temporarily comment out lines to test
6. **Comments don't exist in bytecode** — they're stripped during tokenization

---

**Next: Unit 2** — Escape Sequences — `\n`, `\t`, `\\`, `\"`, `\'` — How They Work Internally and Why They Exist

---

### Unit 2: Escape Sequences — `\n`, `\t`, `\\`, `\"`, `\'`

#### Core Truth
**Escape sequences are special character combinations that represent characters impossible or difficult to type directly in a string.** The backslash `\` is an escape character that modifies the meaning of the character that follows it.

#### The Problem Escape Sequences Solve

```python
# Problem 1: Can't span a string across multiple lines
print("Hey, how are you?
I am good")  # SyntaxError: unterminated string literal

# Problem 2: Can't print a literal double quote inside double-quoted string
print("He said "hello"")  # SyntaxError: unexpected character after string literal

# Problem 3: Can't print a literal backslash
print("C:\new folder")  # \n gets interpreted as new line!
```

**Escape sequences solve all three problems.**

#### How Escape Sequences Work

```python
# The backslash \ tells Python: "the next character has a special meaning"
# \n → new line character (ASCII 10)
# \t → tab character (ASCII 9)
# \\ → literal backslash
# \" → literal double quote
# \' → literal single quote
```

```
Memory:
┌─────────────────────────────────────────────┐
│ "Hey, how are you?\nI am good"            │
│                                              │
│ \n is ONE character (ASCII 10, LF)         │
│ NOT two characters (\ and n)               │
└─────────────────────────────────────────────┘
```

**Key insight**: `\n` is a **single character** in memory — the newline character (Unicode U+000A). It's not two characters.

#### `\n` — New Line

```python
print("Hey, how are you?\nI am good")
# Output:
# Hey, how are you?
# I am good
```

```
Memory:
┌─────────────────────────────────────────────────────────────┐
│ PyUnicodeObject("Hey, how are you?\nI am good")          │
│                                                              │
│ H e y ,   h o w   a r e   y o u ? \n I   a m   g o o d   │
│                                    │                       │
│                              ASCII 10 (LF)                  │
└─────────────────────────────────────────────────────────────┘
```

**When printed**, `\n` causes the cursor to move to the beginning of the next line.

#### `\t` — Tab

```python
print("Name\tAge\tCity")
print("Alice\t25\tCairo")
print("Bob\t30\tAlexandria")
```

```
Output:
Name    Age    City
Alice   25     Cairo
Bob     30     Alexandria
```

**`\t` inserts a tab character** (ASCII 9), aligning text in columns.

#### `\\` — Literal Backslash

```python
# Without escape: \n is interpreted as new line
print("C:\new folder")
# Output: C:
#         ew folder  ← \n created a new line!

# With escape: \\ is a literal backslash
print("C:\\new folder")
# Output: C:\new folder
```

```
Memory comparison:
┌─────────────────────────────────────────────┐
│ "C:\new folder"                           │
│   \n → ASCII 10 (new line)               │
│                                              │
│ "C:\\new folder"                          │
│   \\ → ASCII 92 (single backslash)       │
│   n  → ASCII 110 (letter n)              │
└─────────────────────────────────────────────┘
```

**`\\` produces ONE backslash character** (ASCII 92). The first `\` escapes the second `\`.

#### `\"` and `\'` — Literal Quotes

```python
# Double quote inside double-quoted string
print("He said \"hello\"")
# Output: He said "hello"

# Single quote inside single-quoted string
print('It\'s a test')
# Output: It's a test
```

```
Memory:
┌─────────────────────────────────────────────┐
│ "He said \"hello\""                       │
│                                              │
│ He said "hello"                            │
│         ↑ ASCII 34 (double quote)          │
│         ↑ escaped by \"                     │
└─────────────────────────────────────────────┘
```

**`\"` produces ONE double quote character** (ASCII 34). Without the escape, Python thinks the string ended at the first `"`.

#### Complete Escape Sequence Table

| Escape Sequence | Character | ASCII | Example | Output |
|----------------|-----------|-------|---------|--------|
| `\n` | New line | 10 | `"A\nB"` | `A` on line 1, `B` on line 2 |
| `\t` | Tab | 9 | `"A\tB"` | `A` [tab] `B` |
| `\\` | Backslash | 92 | `"A\\B"` | `A\B` |
| `\"` | Double quote | 34 | `"say \"hi\""` | `say "hi"` |
| `\'` | Single quote | 39 | `'say \'hi\''` | `say 'hi'` |
| `\r` | Carriage return | 13 | `"A\rB"` | `B` overwrites `A` |
| `\b` | Backspace | 8 | `"AB\bC"` | `AC` |

#### The Critical Distinction — `\n` vs `\\n`

```python
# \n → ONE character: new line
print("A\nB")
# Output:
# A
# B

# \\n → TWO characters: backslash + letter n
print("A\\nB")
# Output: A\nB
```

```
Memory:
┌─────────────────────────────────────────────┐
│ "A\nB"                                    │
│   \n → U+000A (single char)              │
│   3 characters total: A, LF, B            │
│                                              │
│ "A\\nB"                                   │
│   \\ → ASCII 92 (backslash)              │
│   n  → ASCII 110 (letter n)              │
│   4 characters total: A, \, n, B          │
└─────────────────────────────────────────────┘
```

**This is the most common source of confusion.** `\n` is one character. `\\n` is two characters.

#### Under the Hood — Tokenization

```python
# When Python tokenizes "A\nB":
# Token: STRING "A\nB"
# The tokenizer converts \n to the actual newline character (U+000A)
# The string object stores: ['A', '\n', 'B'] (3 characters)

# When Python tokenizes "A\\nB":
# Token: STRING "A\\nB"
# The tokenizer converts \\ to \ and keeps n as-is
# The string object stores: ['A', '\\', 'n', 'B'] (4 characters)
```

```c
// Simplified CPython tokenizer
// When reading a string literal:
//   '\n' → converts to Unicode character U+000A
//   '\\' → converts to Unicode character U+005C (backslash)
//   '\"' → converts to Unicode character U+0022 (double quote)
```

#### Raw Strings — `r"..."`

```python
# Raw strings disable escape sequences entirely
print(r"C:\new folder")
# Output: C:\new folder  ← \n is NOT interpreted as new line
```

**Raw strings** prefix the string with `r`. Everything inside is treated literally — no escape processing.

```
Memory:
┌─────────────────────────────────────────────┐
│ r"C:\new folder"                          │
│                                              │
│ C : \ n e w   f o l d e r                  │
│              ↑ literal backslash             │
│              ↑ literal letter n              │
└─────────────────────────────────────────────┘
```

#### Common Pitfalls

##### 1. Confusing `\n` with `\\n`
```python
print("A\nB")   # A on line 1, B on line 2
print("A\\nB")  # A\nB on one line
```

##### 2. Forgetting to Escape Quotes
```python
print("He said "hello"")  # SyntaxError
print("He said \"hello\"")  # Works
```

##### 3. Windows Paths
```python
# Wrong:
path = "C:\new folder\file.txt"
# \n → new line, \f → form feed, \t → tab!

# Right:
path = r"C:\new folder\file.txt"  # Raw string
# OR
path = "C:\\new folder\\file.txt"  # Double backslashes
```

##### 4. `\r` — Carriage Return
```python
print("Hello\rWorld")
# Output: World (overwrites Hello)
```

#### Key Takeaways

1. **`\n`** — new line character (ASCII 10), ONE character in memory
2. **`\t`** — tab character (ASCII 9), aligns text in columns
3. **`\\`** — literal backslash (ASCII 92), produces ONE backslash
4. **`\"`** — literal double quote (ASCII 34), escapes double quotes
5. **`\'`** — literal single quote (ASCII 39), escapes single quotes
6. **`\n` ≠ `\\n`** — one is a newline, the other is backslash + n
7. **Escape sequences are processed at tokenization** — converted to actual Unicode characters
8. **Raw strings (`r"..."`)** disable escape processing entirely
9. **The backslash `\` is the escape character** — it modifies the next character's meaning
10. **All escape sequences produce single characters** in memory

---

**Next: Unit 3** — Print Statement — `sep` and `end` Parameters, How `print()` Formats Output with Multiple Arguments

---

### Unit 3: Print Statement — `sep` and `end` Parameters

#### Core Truth
**`print()` has two hidden parameters that control formatting: `sep` (separator between arguments) and `end` (what's printed after the last argument).** By default, `sep=' '` (space) and `end='\n'` (newline).

#### How `print()` Works with Multiple Arguments

```python
print("Hello", "world", 5)
# Output: Hello world 5
```

```
Memory:
┌─────────────────────────────────────────────────────────────┐
│ PyUnicodeObject("Hello")  PyUnicodeObject("world")  PyLongObject(5) │
│         │                    │                    │              │
│         └──────────┬─────────┘────────────────────┘              │
│                    ▼                                             │
│              print()                                             │
│         sep=' ' (default)                                       │
│         end='\n' (default)                                      │
│                    ▼                                             │
│    Output: "Hello world 5\n"                                    │
└─────────────────────────────────────────────────────────────┘
```

**`print()` joins all arguments with `sep` and appends `end` at the end.**

#### The `sep` Parameter — Separator Between Arguments

```python
# Default sep is a space
print("Hello", "world")
# Output: Hello world

# Custom sep
print("Hello", "world", sep="-")
# Output: Hello-world

print("Hello", "world", sep=", ")
# Output: Hello, world

print("Hello", "world", sep="/")
# Output: Hello/world
```

```
Memory:
┌─────────────────────────────────────────────────────────────┐
│ print("Hello", "world", sep=", ")                          │
│                                                              │
│ Arguments: ["Hello", "world"]                               │
│ sep: ", " (comma space)                                      │
│                                                              │
│ Join: "Hello" + ", " + "world"                             │
│ Result: "Hello, world"                                      │
│ + end: "\n"                                                  │
│ Final: "Hello, world\n"                                     │
└─────────────────────────────────────────────────────────────┘
```

**`sep` controls what goes BETWEEN arguments.** Default is `' '` (space).

#### The `end` Parameter — What's Printed After

```python
# Default end is newline
print("Hello")
# Output: Hello\n

# Custom end
print("Hello", end="")
# Output: Hello (no newline)

print("Hello", end=" ")
# Output: Hello (space instead of newline)

print("Hello", end="---")
# Output: Hello---
```

```
Memory:
┌─────────────────────────────────────────────────────────────┐
│ print("Hello", end="---")                                  │
│                                                              │
│ Arguments: ["Hello"]                                        │
│ sep: ' ' (default, not used with 1 arg)                     │
│ end: "---"                                                   │
│                                                              │
│ Result: "Hello---"                                          │
└─────────────────────────────────────────────────────────────┘
```

**`end` controls what's printed AFTER the last argument.** Default is `'\n'` (newline).

#### `sep` and `end` Together

```python
print("Hello", "world", sep=", ", end="---")
# Output: Hello, world---
```

```
Memory:
┌─────────────────────────────────────────────────────────────┐
│ Arguments: ["Hello", "world"]                               │
│ sep: ", "                                                    │
│ end: "---"                                                   │
│                                                              │
│ Join: "Hello" + ", " + "world" = "Hello, world"            │
│ + end: "---"                                                 │
│ Final: "Hello, world---"                                    │
└─────────────────────────────────────────────────────────────┘
```

#### Multiple `print()` Statements — Automatic Newlines

```python
print("Hello")
print("World")
# Output:
# Hello
# World
```

**Why?** Because each `print()` has `end='\n'` by default. The first `print()` outputs `"Hello\n"`, the second outputs `"World\n"`.

```python
# Same as:
print("Hello\nWorld\n")
```

#### The Lecture's Example — Full Breakdown

```python
# Default behavior
print("Hello world", "Harry", 5)
# Output: Hello world Harry 5
# sep=' ' (space), end='\n'

# With sep override
print("Hello world", "Harry", 5, sep=",")
# Output: Hello world,Harry,5
# sep=',' (comma)

# With end override
print("Hello world", end="")
# Output: Hello world (no newline)
```

```
Memory layout for print("Hello world", "Harry", 5, sep=","):

┌─────────────────────────────────────────────────────────────┐
│ Arguments: ["Hello world", "Harry", 5]                      │
│ sep: ","                                                     │
│ end: "\n"                                                    │
│                                                              │
│ Join: "Hello world" + "," + "Harry" + "," + "5"           │
│ = "Hello world,Harry,5"                                     │
│ + end: "\n"                                                  │
│ Final: "Hello world,Harry,5\n"                              │
└─────────────────────────────────────────────────────────────┘
```

#### Under the Hood — `print()` Function Signature

```python
# print() is actually a built-in function, not a statement
print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)
```

```c
// Simplified CPython (Python/bltinmodule.c)
PyObject* builtin_print(PyObject *self, PyObject *args, PyObject *kwargs) {
    // Parse arguments
    // sep = kwargs["sep"] or " " (default space)
    // end = kwargs["end"] or "\n" (default newline)
    
    // Join all objects with sep
    // Append end
    // Write to file (stdout)
}
```

**`print()` is a function** — it accepts `*args` (variable arguments), `sep`, `end`, `file`, and `flush` parameters.

#### The `sep` and `end` Default Values

```python
# These are equivalent:
print("Hello", "world")
print("Hello", "world", sep=' ', end='\n')
```

**Default values:**
- `sep=' '` — space character
- `end='\n'` — newline character

#### Common Patterns

| Pattern | Output | Explanation |
|---------|--------|-------------|
| `print("A", "B")` | `A B` | Default sep and end |
| `print("A", "B", sep=",")` | `A,B` | Custom separator |
| `print("A", end="")` | `A` | No newline |
| `print("A", end=" ")` | `A ` | Space instead of newline |
| `print("A", "B", sep="→", end="!")` | `A→B!` | Both custom |
| `print("A", end="\n\n")` | `A\n\n` | Double newline |

#### Common Pitfalls

##### 1. Forgetting `end=""` for Same-Line Output
```python
# Wrong: prints on separate lines
print("Loading", end="")
print("...")
# Output: Loading...

# Without end="":
print("Loading")
print("...")
# Output:
# Loading
# ...
```

##### 2. Confusing `sep` with `end`
```python
# sep is BETWEEN arguments
print("A", "B", sep=",")  # A,B

# end is AFTER all arguments
print("A", "B", end=",")  # A B,
```

##### 3. `sep` Only Works with Multiple Arguments
```python
print("Hello", sep=",")  # Hello (sep has no effect with 1 argument)
```

#### Key Takeaways

1. **`print()` is a function** — not a statement — with parameters `sep`, `end`, `file`, `flush`
2. **`sep`** controls what goes BETWEEN arguments (default: `' '`)
3. **`end`** controls what's printed AFTER the last argument (default: `'\n'`)
4. **Multiple `print()` statements** each add a newline by default
5. **`print("A", "B", sep=",")`** → `A,B`
6. **`print("A", end="")`** → no newline after A
7. **`sep` only matters with 2+ arguments** — ignored with 1 argument
8. **Both `sep` and `end` can be overridden simultaneously**
9. **`print()` writes to `sys.stdout`** by default (the `file` parameter changes this)
10. **The defaults are `sep=' '` and `end='\n'`** — these are the "ideal scenario" values

---

**Lecture 4 complete!** All 3 units documented. Ready for **Lecture 5: Operators in Python** whenever you are!
