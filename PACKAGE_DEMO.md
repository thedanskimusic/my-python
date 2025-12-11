# Package Installation Demo

## What We Just Did

1. **Installed `requests` package** in the virtual environment
2. **Updated `requirements.txt`** with all installed packages
3. **Created an example script** that uses the package

## Key Observations

### ✅ Package Installation Location

The `requests` package (and its dependencies) were installed in:
```
venv/lib/python3.14/site-packages/
```

You can see these folders were created:
- `requests/` - The main package
- `certifi/` - Dependency (SSL certificates)
- `urllib3/` - Dependency (HTTP library)
- `charset-normalizer/` - Dependency (character encoding)
- `idna/` - Dependency (internationalized domain names)

### ✅ Package Isolation

- **In venv (activated)**: `import requests` ✅ Works!
- **In system Python (venv deactivated)**: `import requests` ❌ Would fail!

### ✅ Requirements.txt

The `requirements.txt` file now contains:
```
certifi==2025.11.12
charset-normalizer==3.4.4
idna==3.11
requests==2.32.5
urllib3==2.6.1
```

This file allows anyone to recreate your exact environment:
```bash
pip install -r requirements.txt
```

## Try It Yourself

1. **With venv activated:**
   ```bash
   source venv/bin/activate
   python src/example_requests.py
   ```

2. **With venv deactivated:**
   ```bash
   deactivate
   python3 src/example_requests.py  # This will fail!
   ```

## What This Demonstrates

- Virtual environments keep packages isolated per project
- `requirements.txt` documents your dependencies
- Packages are installed in `venv/lib/python3.14/site-packages/`
- When venv is active, Python looks there first for packages

