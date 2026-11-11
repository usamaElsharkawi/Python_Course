# Lecture 35 — Dictionaries (transcript code)

# --- Unit 1: Creating dictionaries, fast lookup ---
marks = {"Harry": 34, "Jack": 45, "Lilly": 94}

print(marks)
print(type(marks))          # <class 'dict'>

print(marks["Lilly"])       # 94 — lookup by key

# --- Unit 2: Key rules ---
marks2 = {1: "int key", (1, 2): "tuple key", "s": 1}
# marks2[[1, 2]] = "list key"   # TypeError: unhashable type: 'list'
# marks2["Lily"]                # KeyError: 'Lily'

# --- Unit 3: Mutation via assignment ---
marks["Harry"] = 3          # update value
marks["New"] = 50           # insert new key
print(marks)

# --- Unit 4: Dictionary methods ---
m = {"Harry": 34, "Jack": 45, "Lilly": 94}
print(m.keys())             # dict_keys([...])
print(m.values())           # dict_values([...])
print(m.get("X"))           # None — no KeyError
print(m.pop("Lilly"))       # 94 — removes and returns
print(m.popitem())          # last inserted pair
# m.clear()                  # empties the dict
m.setdefault("group", [])

for name, grade in m.items():
    pass                    # tuple unpacking in loops

# --- Unit 5: Dict comprehensions ---
table_of_five = {i: 5 * i for i in range(1, 11)}
print(table_of_five)        # {1: 5, 2: 10, ..., 10: 50}

squares = {i: i * i for i in range(6)}
print(squares)              # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
