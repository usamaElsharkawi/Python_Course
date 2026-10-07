# Lecture 28 — Modules and Pip: Using External Libraries

**Units covered**: 1. What are modules: import and basic usage, 2. Built-in
modules: math, os, json, and the Python Module Index, 3. Creating and
importing your own modules, 4. External modules, pip, and dependency
management

---

## Unit 1 — What Are Modules: Import and Basic Usage

### Core Concept
A **module** is a Python file (`.py`) containing definitions (functions,
classes, variables) that can be imported and reused. Instead of rewriting
common functionality, you import existing code — this is the "don't
reinvent the wheel" principle.

### What's Actually Happening

**1. The `import` statement**
```python
import math
print(math.sqrt(16))  # 4.0
```

When `import math` executes:
1. Python searches `sys.path` for a module named `math`
2. If found, it executes the module's code (creating its namespace)
3. A **module object** is created and bound to the name `math` in the
   current namespace
4. Accessing `math.sqrt` looks up `sqrt` in the `math` module's
   `__dict__`

**2. Module objects**
```python
import math
print(type(math))           # <class 'module'>
print(math.__name__)        # 'math'
print(math.__file__)        # Path to math.py (or .so for C extensions)
```

Modules are first-class objects — they can be assigned, passed to
functions, etc.

**3. Alternative import syntax**
```python
import math as m           # Alias
print(m.sqrt(9))           # 3.0

from math import sqrt      # Import specific name
print(sqrt(25))            # 5.0

from math import *         # Import all public names (discouraged)
```

### Minimal Executable Example

```python
# Using a built-in module
import math
print(math.sqrt(64))      # 8.0
print(math.pi)            # 3.141592653589793

# Alias
import math as m
print(m.factorial(5))     # 120

# Specific import
from math import ceil, floor
print(ceil(4.2))          # 5
print(floor(4.9))         # 4
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Name collision | `import math` then `math = 5` | Overwrites the module reference |
| `from X import *` | Pollutes namespace | Hard to track where names come from; PEP 8 discourages |
| Importing unused | `import os` but never used | VSCode shows grayed-out import; linter warns |
| Circular imports | `a.py` imports `b`; `b.py` imports `a` | `ImportError` or partially initialized modules |

### Key Insight
`import` loads a module **once** per process. Subsequent imports return
the cached module object from `sys.modules`. This is why module-level
code runs only once.

---

## Unit 2 — Built-in Modules: math, os, json, and the Python Module Index

### Core Concept
Python ships with a large **standard library** of built-in modules — no
installation required. These provide common functionality: math
operations, OS interaction, JSON handling, file I/O, networking, etc.
The complete list is documented at the **Python Module Index**
(docs.python.org/3/py-modindex.html).

### What's Actually Happening

**1. Built-in vs external modules**
- **Built-in**: Compiled into the Python interpreter or available as
  `.py` files in the standard library (`Lib/`). Always available.
- **External**: Must be installed via `pip` (e.g., `requests`,
  `pandas`).

```python
import math, os, json, sys, datetime, random, itertools
# All available immediately
```

**2. The transcript highlights: `math` and `os`**
```python
import math
math.sqrt(16)     # 4.0
math.pi           # 3.14159...
math.factorial(5) # 120

import os
os.getcwd()       # Current working directory
os.listdir()      # List directory contents
os.path.join('a', 'b')  # 'a/b' (cross-platform)
```

**3. VSCode unused-import detection**
The transcript notes that unused imports appear **grayed out** in
VSCode. This is a static analysis feature (via Pylance/Pyright) that
warns about `import os` without subsequent `os.*` usage. It doesn't
affect runtime — only code hygiene.

**4. The Python Module Index**
- URL: `https://docs.python.org/3/py-modindex.html`
- Lists every built-in module alphabetically with links to docs
- Updates with each Python version
- You don't memorize it — you explore it when you need a capability

### Minimal Executable Example

```python
# math — mathematical functions
import math
print(math.sqrt(2))       # 1.414...
print(math.ceil(3.1))     # 4
print(math.comb(5, 2))    # 10 (binomial coefficient)

# os — operating system interface
import os
print(os.getcwd())        # /home/user/project
print(os.path.exists(__file__))  # True

# json — serialization
import json
data = {"name": "Alice", "age": 30}
s = json.dumps(data)      # '{"name": "Alice", "age": 30}'
parsed = json.loads(s)    # {'name': 'Alice', 'age': 30}

# sys — interpreter state
import sys
print(sys.version)        # Python version string
print(sys.path)           # Module search paths
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Assuming all modules are built-in | `import requests` without pip install | `ModuleNotFoundError` |
| `os.path` vs `pathlib` | `os.path.join` vs `Path / "file"` | `pathlib` is modern, object-oriented; prefer it |
| Platform-specific paths | `'C:\\Users'` on Linux | Use `os.path.join` or `pathlib` for cross-platform |
| `json` can't serialize all types | `json.dumps({1,2,3})` | Sets aren't JSON-serializable; use `list()` |

### Key Insight
The standard library covers ~300 modules. You don't need to know them
all — when you need a capability (dates, regex, hashing, subprocesses,
etc.), check the Module Index first. Most "common" problems have a
built-in solution.

---

## Unit 3 — Creating and Importing Your Own Modules

### Core Concept
Any `.py` file can be a **module**. You define functions/classes/variables
in one file, then `import` it in another. The imported file's code runs
once (creating its module object), and its public names become available
via `module_name.identifier`.

### What's Actually Happening

**1. Creating a module**
```python
# my_module.py
def hello():
    print("Hello World")

value = 42
```
This file is now a module. When imported, `my_module.hello` and
`my_module.value` become accessible.

**2. Importing a local module**
```python
# main.py
import my_module
my_module.hello()    # Hello World
print(my_module.value)  # 42
```

When `import my_module` executes:
1. Python searches `sys.path` — the current directory is first
2. Finds `my_module.py`, executes it (runs the function/class
   definitions)
3. Creates a module object bound to `my_module` in `main.py`'s
   namespace

**3. VSCode IntelliSense**
The transcript notes: "IDE automatically scans for all the functions in
my module and gives a suggestion." This is the language server
(Pylance) indexing the module's symbols for autocomplete.

**4. `import` vs `from ... import`**
```python
# Import the module
import my_module
my_module.hello()

# Import specific name(s) directly
from my_module import hello
hello()              # No prefix needed

# Import multiple
from my_module import hello, value
```

### Minimal Executable Example

```python
# utils.py
def add(a, b):
    return a + b

PI = 3.14159

# main.py
import utils
print(utils.add(2, 3))   # 5
print(utils.PI)          # 3.14159

# Alternative
from utils import add
print(add(10, 20))       # 30 — no prefix needed
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Importing the wrong file | `my_module.py` in subfolder | Need `from folder import my_module` or `__init__.py` |
| Mutating imported module | `utils.PI = 3.0` | Changes visible to all importers — avoid |
| Circular import | `a.py` imports `b`, `b.py` imports `a` | `ImportError` or partially loaded modules |
| Running module as script | `python my_module.py` | `__name__ == "__main__"` — useful for testing |

### Key Insight
Your own `.py` files are modules exactly like `math` or `os`. The only
difference is that Python looks for them in the current directory (or
package) first. This is how you structure larger programs: break code
into focused `.py` files and import between them.

---

## Unit 4 — External Modules, pip, and Dependency Management

### Core Concept
**External modules** are packages not included in Python's standard
library. They are installed via **pip** (Python's package installer)
from **PyPI** (Python Package Index). Once installed, they import
exactly like built-in modules.

### What's Actually Happening

**1. pip install mechanics**
```bash
pip install requests
```

When this runs:
1. pip connects to PyPI (pypi.org)
2. Resolves the package name to a distribution file (wheel `.whl` or
   source tarball)
3. Downloads the package and **all its dependencies**
4. Extracts and places files in `site-packages/` (e.g.,
   `/usr/local/lib/python3.x/site-packages/`)
5. Updates metadata (version, dependencies) in `dist-info/` folder

**2. Dependency resolution**
The transcript shows `pip install pandas` installing:
- `pandas`
- `numpy` (pandas depends on numpy)
- `python-dateutil`, `pytz`, `six`, `tzdata` (numpy/pandas depend on
  these)

```
pip install pandas
# Collecting pandas
# Collecting numpy>=1.23.2 (from pandas)
# Collecting python-dateutil>=2.8.2 (from pandas)
# Collecting pytz>=2020.1 (from pandas)
# Collecting six>=1.5 (from python-dateutil)
# Collecting tzdata (from pandas)
# Installing collected packages: numpy, python-dateutil, pytz, six, tzdata, pandas
```

**3. Using an external module**
```python
import requests
r = requests.get("https://www.google.com")
print(r.text)   # HTML content
```

`requests` is now in `site-packages/` and imports normally.

**4. Where packages live**
```python
import requests
print(requests.__file__)
# /home/user/.local/lib/python3.11/site-packages/requests/__init__.py

import sys
print(sys.path)  # Includes site-packages directories
```

### Minimal Executable Example

```bash
# Install (run in terminal)
pip install requests
```

```python
# Use it
import requests
r = requests.get("https://httpbin.org/get")
print(r.status_code)    # 200
print(r.json())         # Parsed JSON response

# Check version
import requests
print(requests.__version__)  # e.g., 2.31.0
```

### Common Pitfalls / Gotchas

| Pitfall | Example | Issue |
|---------|---------|-------|
| Global install conflicts | `pip install pandas` in base env | Different projects need different versions |
| Missing dependency | `pip install` fails | Network issues or PyPI down; check `pip --verbose` |
| Version mismatch | `import pandas` → `AttributeError` | Installed version doesn't match code expectations |
| Not in PATH | `pip` command not found | Use `python -m pip` instead |

### Key Insight
**pip + PyPI** is Python's ecosystem engine. External modules live in
`site-packages/`, and `import` finds them via `sys.path`. Every
external module brings its own dependencies — pip resolves the full
dependency graph automatically. For project isolation, use **virtual
environments** (next topic in course).

---

**End of Lecture 28 — Modules and Pip: Using External Libraries**

All 4 units documented. Ready for the next step.