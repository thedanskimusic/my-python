# Security Scanner Guide

## What It Does

This security scanner helps you find security issues in your code, similar to tools like:
- **Snyk** - Security vulnerability scanning
- **GitGuardian** - Secret detection
- **TruffleHog** - Credential scanning

## How It Works

### 1. Secret Detection

The scanner uses regex patterns to find:
- API keys (various formats)
- AWS credentials (Access Keys, Secret Keys)
- Passwords and tokens
- Private keys
- Database connection strings
- GitHub tokens

### 2. Vulnerability Scanning

Detects common security issues:
- SQL injection risks (string concatenation in queries)
- Dangerous code execution (`eval()`, `exec()`)
- Shell command injection
- Insecure random number generation
- Hardcoded IP addresses

### 3. File Scanning

- Automatically finds code files (`.py`, `.js`, `.java`, etc.)
- Scans config files (`.json`, `.yaml`, `.env`, etc.)
- Ignores common directories (`venv/`, `node_modules/`, `.git/`, etc.)

## Testing

A test file `test_security.py` is included with intentional security issues to demonstrate the scanner's capabilities.

Run it:
```bash
python src/scanner_cli.py test_security.py
```

## Extending the Scanner

### Adding New Patterns

Edit `src/patterns/rules.py` to add new detection patterns:

```python
{
    "name": "My New Pattern",
    "pattern": re.compile(r'your-regex-pattern'),
    "severity": "high",
    "description": "What this pattern detects"
}
```

### Customizing File Types

Modify `CODE_FILE_EXTENSIONS` and `CONFIG_FILE_EXTENSIONS` in `src/patterns/rules.py` to scan additional file types.

### Adding New Scanners

Create a new scanner class similar to `SecretDetector` or `VulnerabilityScanner` and integrate it into `scanner_cli.py`.

## Exit Codes

- `0`: No critical or high severity issues found
- `1`: Critical or high severity issues detected

This makes it easy to integrate into CI/CD pipelines!

