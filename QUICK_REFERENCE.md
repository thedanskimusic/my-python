# Quick Reference Guide

## Daily Usage

### Scan Any Repository
```bash
docker run --rm -v /path/to/repo:/scan security-scanner /scan
```

### Scan with Options
```bash
# High/critical only
docker run --rm -v /path/to/repo:/scan security-scanner /scan --severity high

# JSON output
docker run --rm -v /path/to/repo:/scan security-scanner /scan --output json
```

## Development Workflow

### 1. Make Changes
Edit code in `src/` directory

### 2. Rebuild Image
```bash
docker build -t security-scanner .
# OR
./scripts/rebuild.sh
```

### 3. Test
```bash
docker run --rm -v $(pwd):/scan security-scanner /scan/test_security.py
```

## Common Tasks

### Add New Security Pattern
1. Edit `src/patterns/rules.py`
2. Add pattern to `SECRET_PATTERNS` or `VULNERABILITY_PATTERNS`
3. Rebuild: `docker build -t security-scanner .`

### Add New Dependency
1. Install in venv: `pip install package-name`
2. Update requirements: `pip freeze > requirements.txt`
3. Rebuild: `docker build -t security-scanner .`

### Test Locally (Without Docker)
```bash
source venv/bin/activate
python src/scanner_cli.py test_security.py
```

## Helper Scripts

- `./scripts/rebuild.sh` - Quick rebuild
- `./scripts/dev-test.sh` - Rebuild and test
- `./scan.sh` - Wrapper script for scanning

## Docker Commands

```bash
# Check if image exists
docker images | grep security-scanner

# Remove old image (if needed)
docker rmi security-scanner

# View image size
docker images security-scanner
```

