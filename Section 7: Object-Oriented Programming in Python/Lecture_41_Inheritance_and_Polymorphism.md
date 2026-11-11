# Lecture 41 — Inheritance and Polymorphism

**Units covered**: 1. Inheritance: parent & child classes,
2. Method overriding & `super()`,
3. Polymorphism & inherited class attributes

---

## Unit 1 — Inheritance: Parent & Child Classes

### Core Concept
Inheritance lets you create a **child class** that reuses attributes and methods from a **parent class**, without rewriting the code. It's like a family tree — the child inherits traits from the parent.

### What's Actually Happening
```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print("Generic animal sound")

class Dog(Animal):   # Dog inherits from Animal
    pass
```

- `class Dog(Animal)` — the parentheses name the parent class. `Dog` becomes a subclass; `Animal` is the superclass/parent.
- `Dog` automatically gets `__init__`, `speak`, and any other attributes/methods defined on `Animal`.
- `d = Dog("Bruno")` creates a `Dog` instance with `name = "Bruno"` (via inherited `__init__`).
- `d.speak()` → `"Generic animal sound"` (inherited, not overridden yet).

### Why It Matters
- **Code reuse** — define shared behavior once in the parent; children inherit it automatically.
- **Specialization** — a child class is a specialized version of the parent (a Dog *is an* Animal).
- No copying/pasting — the child references the parent's code directly.

### Minimal Executable Example
```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print("Generic animal sound")

class Dog(Animal):
    pass

d = Dog("Bruno")
print(d.name)      # Bruno — inherited __init__ ran
d.speak()          # Generic animal sound — inherited method
```

---

## Unit 2 — Method Overriding & `super()`

### Core Concept
A child class can **override** a parent method — replace it with its own version. `super()` lets you call the parent's version of a method from inside the child, so you can extend rather than completely replace the parent's behavior.

### What's Actually Happening
```python
class Dog(Animal):
    def speak(self):
        super().speak()     # call parent's speak
        print("Woof")
```

- `d.speak()` → first runs `Animal.speak` (via `super()`), then prints `"Woof"`.
- `super()` returns a proxy object that lets you access methods on the parent class. `super().speak()` means "find `speak` on `Dog`'s parent (`Animal`) and call it with the current `self`."

### Why It Matters
- **Method overriding** — customize behavior for the child while keeping the same method name.
- **`super()`** — call the parent's implementation when you want to *add* to it, not replace it entirely.
- Especially critical in `__init__`: `super().__init__(name)` initializes the parent's part of the child object.

### Minimal Executable Example
```python
class Animal:
    def speak(self):
        print("Generic animal sound")

class Dog(Animal):
    def speak(self):
        super().speak()   # extend parent behavior
        print("Woof")

d = Dog("Bruno")
d.speak()                 # Generic animal sound / Woof
```

---

## Unit 3 — Polymorphism & Inherited Class Attributes

### Core Concept
**Polymorphism** means objects of different classes respond to the same method name in their own way. `animal.speak()` and `dog.speak()` use the same interface but produce different output. Class attributes (like `location = "Australia"`) are also inherited — the child sees them unless it shadows them.

### What's Actually Happening
```python
class Animal:
    location = "Australia"   # class attribute — inherited by Dog

    def __init__(self, name):
        self.name = name

    def speak(self):
        print("Generic animal sound")

class Dog(Animal):
    def speak(self):
        print("Woof")
```

- `d.location` → `"Australia"` — inherited class attribute, no instance shadowing.
- `a = Animal("Generic"); d = Dog("Bruno")`
- `a.speak()` → `"Generic animal sound"`; `d.speak()` → `"Woof"` — same method name, different behavior per class = polymorphism.

### Why It Matters
- Polymorphism lets you write code that works with any object having a `speak()` method, without knowing its exact class.
- Inherited class attributes reduce duplication — shared constants live on the parent.
- Together, inheritance + polymorphism are the foundation of OOP design (Lectures 42–43 build on this: overriding, operator overloading, practice set).

### Minimal Executable Example
```python
class Animal:
    location = "Australia"

    def __init__(self, name):
        self.name = name

    def speak(self):
        print("Generic animal sound")

class Dog(Animal):
    def speak(self):
        print("Woof")

a = Animal("Generic")
d = Dog("Bruno")

print(d.location)   # Australia — inherited class attribute
a.speak()           # Generic animal sound
d.speak()           # Woof — same method name, different behavior (polymorphism)
```

---

## Key Insight
A child class (`class Dog(Animal)`) automatically gains the parent's attributes and methods. You can override methods to specialize behavior, and `super()` lets you call the parent's version when you want to extend it. Polymorphism means the same method call behaves differently depending on the actual object's class.
