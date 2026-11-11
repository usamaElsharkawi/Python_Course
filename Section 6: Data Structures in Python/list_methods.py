# Lecture 32 — List Methods (transcript code + demos)

# --- Unit 1: append, insert, extend ---
marks = [52, 21, 5, 7]

marks.append(63)
print(marks)                     # [52, 21, 5, 7, 63]

marks.insert(1, 77)
print(marks)                     # [52, 77, 21, 5, 7, 63]

extra_marks = [53, 23, 32]
marks.extend(extra_marks)
print(marks)                     # [52, 77, 21, 5, 7, 63, 53, 23, 32]

# marks.sort()
# marks.reverse()
# marks.pop()
# marks.remove(...)
# marks.index(...)
# marks.count(...)
# marks.copy()
# marks.clear()
# # type marks. <TAB> to explore all methods

# --- Unit 2: pop and remove ---
m2 = [52, 21, 5, 7]
print(m2.pop())                 # 7 — returned, removed
print(m2.pop(0))                # 52
m2.remove(21)
print(m2)                       # [5]

# --- Unit 3: sort and reverse ---
m3 = [52, 21, 5, 7]
m3.sort()
print(m3)                       # [5, 7, 21, 52]
m3.reverse()
print(m3)                       # [52, 21, 7, 5]

# --- Unit 4: List comprehensions ---
a = 5
table = []
for i in range(1, 11):
    table.append(5 * i)
print(table)                    # [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

# Shortcut: list comprehension
table = [5 * i for i in range(1, 11)]
print(table)                    # identical output, one line
