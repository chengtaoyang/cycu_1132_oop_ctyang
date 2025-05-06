To build a Python package using a `.toml` file, you typically use a `pyproject.toml` file. This file replaces the older `setup.py` and `setup.cfg` approach, providing a standardized way to define build system requirements and package metadata. Here's how to use it:

---

## 🧱 Step-by-Step Guide to Building a Python Package with `pyproject.toml`

### 1. **Create Your Project Structure**

```text
your_project/
│
├── src/
│   └── your_package/
│       ├── __init__.py
│       └── your_module.py
│
├── pyproject.toml
└── README.md
```

> 📝 Note: Using a `src/` layout is optional but recommended for better isolation.

---

### 2. **Write `pyproject.toml`**

Here’s a minimal example using [setuptools](https://setuptools.pypa.io):

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "your-package-name"
version = "0.1.0"
description = "A short description of your package"
readme = "README.md"
requires-python = ">=3.7"
authors = [
    { name="Your Name", email="your.email@example.com" }
]
license = { text = "MIT" }
dependencies = [
    "requests >=2.25",
    "numpy >=1.20"
]

[project.urls]
"Homepage" = "https://your-homepage-url.com"
"Source" = "https://github.com/your-username/your-repo"
```

---

### 3. **Build the Package**

You need `build` installed:

```bash
pip install build
```

Then run:

```bash
python -m build
```

This will generate:

```
dist/
├── your_package_name-0.1.0.tar.gz
└── your_package_name-0.1.0-py3-none-any.whl
```

---

### 4. **Install or Publish the Package**

* **Install locally**:

  ```bash
  pip install dist/your_package_name-0.1.0-py3-none-any.whl
  ```

* **Upload to PyPI** (use [twine](https://twine.readthedocs.io)):

  ```bash
  pip install twine
  twine upload dist/*
  ```

---

## 🧩 Optional Additions

* **Add entry points (CLIs):**

```toml
[project.scripts]
your-command = "your_package.module:main"
```

* **Use `setuptools` dynamic versioning:**

```toml
[tool.setuptools.dynamic]
version = {attr = "your_package.__version__"}
```

* **Include additional files:**

```toml
[tool.setuptools.package-data]
"your_package" = ["data/*.json"]
```

---

Would you like a template with `tests/` or `GitHub Actions` for CI/CD included?
