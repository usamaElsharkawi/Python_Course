# Lecture 31 — Introduction to Lists (transcript code)

# --- Unit 1: Creating lists ---
marks = [54, 23, 64, 93, 32]
mixed = [43, "hello", False, 4.2]

print(marks)   # [54, 23, 64, 93, 32]
print(mixed)   # [43, 'hello', False, 4.2]

# --- Unit 2: Indexing and slicing ---
print(marks[0])    # 54
print(marks[2])    # 64
print(mixed[2])    # False

print(marks[2:4])  # [64, 93]

# mixed[4]  # IndexError: list index out of range

# --- Unit 3: Mutability (interactive demos) ---
import sys

lst = [1, 2, 3]
before = id(lst)
lst[0] = 99
print(lst, id(lst) == before)   # [99, 2, 3] True

a = "hello"
lst = [a, 2, 3]
print(sys.getrefcount(a))       # includes lst[0]
lst[0] = "other"                # decref old, incref new

x, y = [1, 2], None
y = x                           # alias, not copy
x += [3]                        # in-place! y changes too
print(x, y, x is y)             # [1, 2, 3] [1, 2, 3] True
