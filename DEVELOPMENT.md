# Development Guide

## Workflow for Enhancing the Scanner

### 1. Make Your Changes

Edit the scanner code in `src/`:
- `src/scanner/` - Scanner modules
- `src/patterns/rules.py` - Security patterns
- `src/scanner_cli.py` - CLI interface

### 2. Rebuild the Docker Image

After making changes, rebuild the image:

```bash
# From the project root
docker build -t security-scanner .
```

The `-t security-scanner` tags it with the same name, so it replaces the old image.

### 3. Test Your Changes

```bash
# Test on the test file
docker run --rm -v $(pwd):/scan security-scanner /scan/test_security.py

# Test on another repo
docker run --rm -v /path/to/repo:/scan security-scanner /scan
```

## Quick Development Workflow

1. **Edit code** → Make changes to scanner
2. **Rebuild** → `docker build -t security-scanner .`
3. **Test** → Run the scanner
4. **Repeat** → Iterate as needed

## Tips

- **Docker layer caching**: Docker caches layers, so if you only change code (not requirements.txt), rebuilds are fast
- **Test locally first**: You can test without Docker using the venv:
  ```bash
  source venv/bin/activate
  python src/scanner_cli.py test_security.py
  ```
- **Version tagging**: For production, tag versions:
  ```bash
  docker build -t security-scanner:v1.0.0 .
  docker build -t security-scanner:latest .
  ```

## Common Enhancements

### Adding New Security Patterns

Edit `src/patterns/rules.py` and add to `SECRET_PATTERNS` or `VULNERABILITY_PATTERNS`:

```python
{
    "name": "New Pattern",
    "pattern": re.compile(r'your-regex'),
    "severity": "high",
    "description": "What it detects"
}
```

Then rebuild: `docker build -t security-scanner .`

### Adding New Dependencies

1. Install in venv: `pip install new-package`
2. Update requirements: `pip freeze > requirements.txt`
3. Rebuild Docker image: `docker build -t security-scanner .`

### Modifying Scanner Logic

Edit files in `src/scanner/` and rebuild.

## Development Scripts

See `scripts/` directory for helper scripts (if created).

