# Security Scanner - Python Learning Project

A security scanning tool similar to Snyk or secret scanners, built to learn Python!

## Features

- 🔍 **Secret Detection**: Finds API keys, passwords, tokens, AWS credentials, and more
- 🛡️ **Vulnerability Scanning**: Detects SQL injection risks, unsafe eval/exec usage, and other security issues
- 📦 **Dependency Scanning**: Checks packages against OSV database for known vulnerabilities (PyPI, npm, etc.)
- 📁 **Directory Scanning**: Recursively scans code and config files
- 📊 **Multiple Output Formats**: Console (formatted) or JSON output
- 🎯 **Severity Filtering**: Filter findings by severity level

## Project Structure

```
my-python/
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore file
├── src/
│   ├── scanner/          # Scanner modules
│   │   ├── secret_detector.py
│   │   ├── vulnerability_scanner.py
│   │   ├── file_scanner.py
│   │   └── reporter.py
│   ├── patterns/         # Security pattern definitions
│   │   └── rules.py
│   └── scanner_cli.py    # CLI entry point
└── tests/                # Test files
```

## Getting Started

### Option 1: Using Docker (Recommended)

The easiest way to use the scanner is with Docker - no Python setup needed!

**Note:** This project uses **Colima** (lightweight Docker alternative) instead of Docker Desktop. If you don't have Docker running, install Colima:
```bash
brew install colima docker
colima start
```

1. Build the Docker image:
   ```bash
   docker build -t security-scanner .
   ```

2. Scan any directory:
   ```bash
   # Scan a directory (mount it as a volume)
   docker run --rm -v /path/to/your/repo:/scan security-scanner /scan
   
   # Scan current directory
   docker run --rm -v $(pwd):/scan security-scanner /scan
   
   # With options
   docker run --rm -v /path/to/repo:/scan security-scanner /scan --output json --severity high
   ```

3. Or use docker-compose (even easier):
   ```bash
   # Build
   docker-compose build
   
   # Scan current directory
   docker-compose run --rm scanner .
   
   # Scan a specific path
   docker-compose run --rm -v /path/to/repo:/workspace scanner /workspace
   ```

### Option 2: Local Python Setup

1. Make sure Python 3 is installed: `python3 --version`
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the scanner:
   ```bash
   python src/scanner_cli.py <target>
   ```

## Usage

### Basic Usage

```bash
# Scan a file
python src/scanner_cli.py test_security.py

# Scan a directory
python src/scanner_cli.py src/

# Scan with JSON output
python src/scanner_cli.py src/ --output json

# Only scan for secrets (skip vulnerabilities)
python src/scanner_cli.py src/ --no-vulns

# Only show critical and high severity issues
python src/scanner_cli.py src/ --severity high

# Scan dependencies for known vulnerabilities
python src/scanner_cli.py src/ --dependencies

# Scan everything (secrets, vulnerabilities, and dependencies)
python src/scanner_cli.py src/ --dependencies
```

### Options

- `--secrets/--no-secrets`: Enable/disable secret scanning (default: enabled)
- `--vulns/--no-vulns`: Enable/disable vulnerability scanning (default: enabled)
- `--dependencies/--no-dependencies`: Scan dependencies for known vulnerabilities (default: disabled)
- `--output, -o`: Output format - `console` or `json` (default: console)
- `--recursive/--no-recursive`: Scan subdirectories (default: enabled)
- `--severity`: Minimum severity to report - `critical`, `high`, `medium`, `low`, or `all` (default: all)

### Dependency Scanning

The dependency scanner:
- ✅ Parses `requirements.txt` (Python) and `package.json` (Node.js)
- ✅ Checks packages against OSV (Open Source Vulnerabilities) database
- ✅ Reports known CVEs and security advisories
- ✅ Shows vulnerability details, references, and severity

**Example:**
```bash
# Scan dependencies only
docker run --rm -v /path/to/repo:/scan security-scanner /scan --dependencies --no-secrets --no-vulns

# Scan everything including dependencies
docker run --rm -v /path/to/repo:/scan security-scanner /scan --dependencies
```

## Example Output

The scanner will find issues like:
- 🔴 **Critical**: AWS keys, private keys
- 🟠 **High**: API keys, passwords, SQL injection risks, eval/exec usage
- 🟡 **Medium**: Generic tokens, insecure random
- 🔵 **Low**: Hardcoded IPs

## Docker Benefits

Using Docker makes the scanner:
- ✅ **Portable** - Works on any machine with Docker
- ✅ **No setup** - No need to install Python or manage virtual environments
- ✅ **CI/CD ready** - Easy to integrate into pipelines
- ✅ **Consistent** - Same environment everywhere
- ✅ **Easy sharing** - One command to run anywhere

## Development & Updating

### Making Changes

1. **Edit the code** in `src/` directory
2. **Rebuild the Docker image**:
   ```bash
   docker build -t security-scanner .
   ```
   Or use the helper script:
   ```bash
   ./scripts/rebuild.sh
   ```
3. **Test your changes**:
   ```bash
   docker run --rm -v $(pwd):/scan security-scanner /scan/test_security.py
   ```

### Common Enhancements

- **Add new patterns**: Edit `src/patterns/rules.py`
- **Add dependencies**: Update `requirements.txt`, then rebuild
- **Modify scanner logic**: Edit files in `src/scanner/`

See `DEVELOPMENT.md` for detailed development workflow.

## Learning Notes

This project demonstrates:
- Python package structure and modules
- CLI development with Click
- Regular expressions for pattern matching
- File system traversal
- Error handling and reporting
- Virtual environments and dependency management
- Docker containerization

