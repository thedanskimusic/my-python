# Security Scanner - Usage Guide

## Quick Start

The scanner can be run from **anywhere** once the Docker image is built!

## Method 1: Direct Docker Command (Works from anywhere)

```bash
# Scan any directory
docker run --rm -v /path/to/target:/scan security-scanner /scan

# Scan current directory
docker run --rm -v $(pwd):/scan security-scanner /scan

# Dependencies
docker run --rm -v $(pwd):/scan security-scanner /scan --dependencies

# With options
docker run --rm -v /path/to/target:/scan security-scanner /scan --severity high --output json
```

## Method 2: Using the Wrapper Script

### Option A: Copy script to your PATH

```bash
# Copy to a directory in your PATH (e.g., /usr/local/bin)
cp scan.sh /usr/local/bin/security-scan
chmod +x /usr/local/bin/security-scan

# Now use from anywhere:
security-scan ~/code/my-other-repo
security-scan . --severity high
```

### Option B: Use from project directory

```bash
# From the my-python directory
./scan.sh ~/code/my-other-repo

# Or add to PATH temporarily
export PATH="$PATH:/Users/danieljbowling/code/my-python"
scan.sh ~/code/my-other-repo
```

## Method 3: Shell Alias (Easiest)

Add to your `~/.zshrc` or `~/.bashrc`:

```bash
# Simple alias
alias security-scan='docker run --rm -v'

# Or more complete (handles current directory)
alias security-scan='f(){ docker run --rm -v "$(pwd)":/scan security-scanner /scan "$@"; }; f'
```

Then reload: `source ~/.zshrc`

Use it:
```bash
security-scan $(pwd):/scan security-scanner /scan
# Or with the complete alias:
security-scan --severity high
```

## Real-World Examples

### Scan Another Repository

```bash
# From anywhere on your machine
docker run --rm -v ~/code/my-other-project:/scan security-scanner /scan
```

### Scan Current Directory

```bash
# Navigate to any project
cd ~/code/some-project
docker run --rm -v $(pwd):/scan security-scanner /scan
```

### Scan with Specific Options

```bash
# Only high/critical issues, JSON output
docker run --rm -v ~/code/my-project:/scan security-scanner /scan --severity high --output json

# Only secrets, no vulnerabilities
docker run --rm -v ~/code/my-project:/scan security-scanner /scan --no-vulns

# Save results to file
docker run --rm -v ~/code/my-project:/scan security-scanner /scan --output json > scan-results.json
```

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Security Scan
  run: |
    docker run --rm -v ${{ github.workspace }}:/scan security-scanner /scan --severity high
```

## Tips

1. **The image is stored locally** - Once built, you can use it from anywhere
2. **Use absolute paths** - More reliable than relative paths
3. **Mount as read-only** - The scanner only reads files (add `:ro` if you want extra safety)
4. **Exit codes** - Exit code 1 means critical/high issues found (useful for CI/CD)

## Where is the Image?

The Docker image is stored in your local Docker registry. You can see it with:
```bash
docker images | grep security-scanner
```

It's available system-wide, so you can use it from any directory!

