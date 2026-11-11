# Lecture 34 — Sets (transcript code)

# --- Unit 1: Creating sets ---
s = {32, 32, 11}          # duplicate collapses — sets are unique
print(s)
print(type(s))            # <class 'set'>

# s[0]  # TypeError: 'set' object is not subscriptable — no order, no indices

# --- Unit 2: Set methods ---
s2 = {1, 2, 3}
s2.add(32)                # 32 added anywhere
s2.add(32)                # duplicate — silent no-op
print(s2)

s2.remove(1)              # removes 1; KeyError if not present
s2.discard(99)            # silent — removes only if present
s2.pop()                  # removes an arbitrary element

# --- Unit 3: Set operations ---
A = {22, 2, 55, 1}
B = {2, 55, 1, 99}

C = A.union(B)            # {1, 2, 22, 55, 99} — all elements, no duplicates
D = A.intersection(B)     # {1, 2, 55} — common elements
print(C, D)

# A - B   (difference)
# A ^ B   (symmetric difference)
# A.issubset(B), A.issuperset(B)
