# Lecture 48 — Exception Handling and Custom Errors

**Units covered**: 1. `try`/`except` — preventing crashes,
2. Specific error types & the exception object,
3. `raise` — throwing custom errors,
4. `else` — runs when no error,
5. `finally` — always runs (especially in functions)

---

## Unit 1 — `try`/`except` — Preventing Crashes

### Core Concept
Wrap code that might fail in a `try` block. If an error occurs, Python jumps to the `except` block instead of crashing the program.

### What's Actually Happening
```python
while True:
    try:
        a = int(input("Enter number 1: "))
        b = int(input("Enter number 2: "))
        print(f"The sum is {a + b}")
    except:
        print("Some error occurred")
```

- `int(input(...))` crashes with `ValueError` if the user types "Harry" instead of a number
- Without `try`/`except`, the whole program terminates — bad for multi-user scenarios
- With `try`/`except`, the error is caught, `"Some error occurred"` prints, and the loop continues

### Why It Matters
- Programs stay running even when users input bad data
- Essential for production code (web servers, APIs, data pipelines) where a single bad input shouldn't take down the whole service

### Minimal Executable Example
```python
while True:
    try:
        a = int(input("Enter number 1: "))
        b = int(input("Enter number 2: "))
        print(f"The sum is {a + b}")
    except:
        print("Some error occurred")
```

---

## Unit 2 — Specific Error Types & the Exception Object

### Core Concept
You can catch specific error types (`ValueError`, `ZeroDivisionError`) and handle each differently. You can also capture the exception object (`except Exception as e`) to inspect error details.

### What's Actually Happening
```python
try:
    a = int(input("Enter number 1: "))
    b = int(input("Enter number 2: "))
    print(f"The division is {a / b}")
except ValueError:
    print("Please don't perform bad type casts")
except ZeroDivisionError:
    print("Hey, don't divide by zero")
except Exception as e:
    print("Unknown error occurred", e)
```

- `int("Harry")` → `ValueError` → caught by first `except`
- `5 / 0` → `ZeroDivisionError` → caught by second `except`
- Any other error → caught by `except Exception as e`, where `e` holds the error message

### Why It Matters
- Different errors need different responses (tell the user to type a number vs. don't divide by zero)
- `except Exception as e` is the catch-all for unexpected errors; `e.args` or `str(e)` gives diagnostic info

### Minimal Executable Example
```python
try:
    a = int(input("Enter number 1: "))
    b = int(input("Enter number 2: "))
    print(f"The division is {a / b}")
except ValueError:
    print("Please don't perform bad type casts")
except ZeroDivisionError:
    print("Hey, don't divide by zero")
except Exception as e:
    print("Unknown error occurred", e)
```

---

## Unit 3 — `raise` — Throwing Custom Errors

### Core Concept
`raise` lets you manually trigger an exception. Use it to stop execution and guide users when they're using your program incorrectly.

### What's Actually Happening
```python
b = int(input("Enter number 2: "))
if b == 0:
    raise ValueError("Please don't divide by zero")
print(f"The division is {a / b}")
```

- `raise ValueError("message")` immediately stops execution and propagates the error
- The caller must handle it with `try`/`except`, or the program crashes with your custom message
- Useful for validating inputs before dangerous operations (division by zero, invalid state, etc.)

### Why It Matters
- You control when and why your program fails
- Custom error messages help other developers debug their usage of your code
- Part of defensive programming — fail fast with a clear message

### Minimal Executable Example
```python
b = int(input("Enter number 2: "))
if b == 0:
    raise ValueError("Please don't divide by zero")
print(f"The division is {a / b}")
```

---

## Unit 4 — `else` — Runs When No Error

### Core Concept
The `else` block (paired with `try`/`except`) runs **only if no exception occurred** in the `try` block.

### What's Actually Happening
```python
try:
    result = 345 / 10
except Exception as e:
    print(e)
else:
    print("Hey, I am good")   # runs only if try succeeded
```

- `345 / 10` → no error → `else` runs → `"Hey, I am good"`
- `345 / 0` → `ZeroDivisionError` → `except` runs, `else` is skipped

### Why It Matters
- Code that should only run on success (not on error) goes here
- Cleaner than nesting success logic inside `try` or using flags

### Minimal Executable Example
```python
try:
    result = 345 / 10
except Exception as e:
    print(e)
else:
    print("Hey, I am good")
```

---

## Unit 5 — `finally` — Always Runs

### Core Concept
The `finally` block **always executes** — whether the `try` succeeded, failed, or was caught by `except`. It's critical for cleanup (closing files, database connections) and is guaranteed even across `return` statements in functions.

### What's Actually Happening
```python
try:
    a = int(input("Enter number 1: "))
    b = int(input("Enter number 2: "))
    c = a / b
    print(c)
except Exception as e:
    print(e)
finally:
    print("This is always executed")
```

- Valid input → `try` succeeds → `finally` runs
- `b = 0` → `ZeroDivisionError` → `except` prints it → `finally` still runs

### Why `finally` matters most in functions
```python
def divide(a, b):
    try:
        c = a / b
        print(c)
        return c
    except Exception as e:
        print(e)
        return None
    finally:
        print("This is always executed")   # runs even after return
```

- Python guarantees `finally` runs before the function returns, even if `return` is in `try` or `except`
- Without `finally`, a `return` in `except` might skip cleanup code placed after the `try`/`except` block

### Why It Matters
- Cleanup (close DB connections, close files, release locks) must happen regardless of success/failure
- `finally` is the only construct that guarantees execution across `return`, `break`, `continue`, and exceptions

### Minimal Executable Example
```python
try:
    a = int(input("Enter number 1: "))
    b = int(input("Enter number 2: "))
    c = a / b
    print(c)
except Exception as e:
    print(e)
finally:
    print("This is always executed")
```

---

## Key Insight
`try`/`except` catches errors so programs don't crash. `except ValueError` / `except ZeroDivisionError` let you handle specific errors differently. `raise` lets you trigger errors with custom messages. `else` runs only on success. `finally` always runs — even across `return` — making it the right place for cleanup.
