# Unit 1: Variables and Python's Object Model

## Overview

Variables in Python are **not containers** like kitchen boxes. They are **labels/names** that point to **objects** (actual data) living on the heap.

```python
# WRONG: "variable is container"
age = 34

# RIGHT: "variable is label pointing to object"
# ┌─────────────┐
# │   "age"     │ ──refers to──▶ PyLongObject(34)
# └─────────────┘                    ↓
#                                 type=int
```

## The Model

| Component | What It Is | Analogy |
|-----------|------------|---------|
| **Variable** | Name in a namespace dict | Label on a box |
| **Object** | Actual data on heap + type attached | The box itself |
| **Assignment** | Point name to object | Labeling the box |
| **Type** | Attached to object, not variable | Box label (int, str, etc.) |

## How Python Executes `age = 34`

1. **Object Creation**: Integer `34` is created on heap with type `int` attached
2. **Binding**: Name `"age"` in current namespace (global dict) points to that object

```python
# Internals visualization:
# globals = {"age": <PyLongObject at 0x...>}  
# PyLongObject structure: {value: 34, type: int, refcount: 1}
```

## Core Principles

### 1. Multiple Names → Single Object
```python
# Two names pointing to the SAME list object
a = [1, 2, 3]
b = a
b.append(4)    # Modifies the shared list
print(a)       # [1, 2, 3, 4] ← both a and b see it
```

### 2. Objects Carry Their Type
```python
age = 34
print(type(age))  # <class 'int'>
name = "Harry"   
print(type(name)) # <class 'str'>
```

Variables don't have types — objects do.

### 3. Immutability vs. Mutability
```python
# Immutable: Create new object on "modification"
x = 10
y = x
x = 20  # Creates new int object, x now points to new object
print(y)  # 10 ← y still points to original

# Mutable: Changes affect all names
mylist = [1, 2]
other = mylist
other.append(3)
print(mylist)  # [1, 2, 3] ← both see changes
```

## The "Container" Analogy Fixed

| Lecture Model | Python Reality |
|---------------|----------------|
| Variable = container holding value | Variable = label pointing to object |
| Assignment = put value in container | Assignment = stick label on object |
| Multiple variables = multiple containers | Multiple names = multiple labels on same object |

## Comparison: Python vs JavaScript/TypeScript

### Variables
```python
# Python: name points to object
x = 10
y = x
```

```javascript
// JavaScript: primitives are copied
let x = 10;
let y = x;  // y gets VALUE 10, not reference
```

### Objects
```python
# Python: everything is an object
data = "hello"  # String object
```

```javascript
// JavaScript: primitives vs objects
let num = 10;    // primitive value
let str = "hi";  // primitive value
let obj = {};    // object reference
```

### Type System
```python
# Python: types on objects at runtime
a: int = 34    # Type annotation, runtime ignored
print(type(a)) # <class 'int'>
```

```typescript
// TypeScript: types erased at runtime
let a: number = 34;
// After compilation: let a = 34;
```

## Common Pitfalls

### 1. Mutable Default Arguments
```python
# DANGEROUS
def bad_func(items=[]):
    items.append("new")
    return items

print(bad_func())  # ["new"]
print(bad_func())  # ["new", "new"] ← Same list reused!
```

### 2. Thinking Variables Have Types
```python
# OK but misleading
a = 10
print(type(a))  # <class 'int'>

a = "now a string"  # Reassignment, creates new object
print(type(a))       # <class 'str'>
```

### 3. Reference Counting Confusions
```python
import sys

x = [1, 2, 3]
print(sys.getrefcount(x))  # 2 (from x + from getrefcount call)
y = x
print(sys.getrefcount(x))  # 3

# When last reference is deleted, object is immediately freed
```

## Memory Management

- **Reference Counting**: Every object has `refcount` (track how many names point to it)
- **Immediate Cleanup**: When `refcount` hits 0, object is freed
- **Heap Storage**: All objects live on heap, not stack
- **Frames**: Execution contexts containing namespace dicts

## Key Takeaways

1. **Variables are labels, not containers**
2. **Objects carry their type, variables don't**
3. **Multiple names can point to same object**
4. **Immutable vs mutable behavior differs**
5. **No variable type declarations at runtime**
6. **Memory is managed via reference counting**

## Exercises

1. Explain `a = b = [1, 2, 3]`
2. Why `a = 5; b = a; a = 10` doesn't affect `b`
3. Demonstrate mutable vs immutable reassignment
4. Show how `type()` reveals object type, not variable type
5. Explain reference counting with simple examples

---

**Next: Unit 2** — Dynamic Typing and PyObject Internals