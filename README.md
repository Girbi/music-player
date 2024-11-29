
# Music Player Python

## Setup and Installation

### 1. Create a Virtual Environment
### Method 1: Use the VSCode Python Extension to create Virtual Environments

### Method 2:
To create a virtual environment in the project directory:
```bash
python -m venv venv
```

### 2. Activate the Virtual Environment
- **Linux/MacOS:**
  ```bash
  source venv/bin/activate
  ```
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```

### 3. Install Project Dependencies
After activating the virtual environment:
```bash
pip install -r requirements.txt
```

---

## Development Commands

### 1. (Optional) Adding a New Dependency
Install a new package and add it to `requirements.txt`:
```bash
pip install <package_name>
pip freeze > requirements.txt
```

### 2. Run the Project
If the project has an entry point script (e.g., `app.py`):
```bash
python app.py
```
---

## Maintenance

### 1. Deactivate the Virtual Environment
To deactivate the virtual environment:
```bash
deactivate
```
---

## Tips

- Ensure `requirements.txt` is always up to date after installing or upgrading packages.
- Use `pip list` to view installed packages within the virtual environment.
- To create an isolated environment for testing, consider using `tox`.
