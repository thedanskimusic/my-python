# Docker Usage Guide

## Quick Start

### 1. Build the Image

```bash
docker build -t security-scanner .
```

### 2. Use It to Scan Any Directory

```bash
# Scan a directory (replace /path/to/repo with your target)
docker run --rm -v /path/to/repo:/scan security-scanner /scan

# Scan current directory
docker run --rm -v $(pwd):/scan security-scanner /scan

# Scan with JSON output
docker run --rm -v /path/to/repo:/scan security-scanner /scan --output json

# Only show high/critical issues
docker run --rm -v /path/to/repo:/scan security-scanner /scan --severity high
```

## Using Docker Compose

### Build and Run

```bash
# Build the image
docker-compose build

# Scan current directory
docker-compose run --rm scanner .

# Scan a specific directory (mount it first)
docker-compose run --rm -v /path/to/repo:/workspace scanner /workspace

# With options
docker-compose run --rm scanner . --output json --severity critical
```

## Real-World Examples

### Scan Another Repository

```bash
# Scan a different project
docker run --rm -v ~/code/my-other-project:/scan security-scanner /scan

# Scan only the src directory of another project
docker run --rm -v ~/code/my-other-project:/scan security-scanner /scan/src
```

### CI/CD Integration

```yaml
# Example GitHub Actions workflow
- name: Security Scan
  run: |
    docker build -t security-scanner .
    docker run --rm -v ${{ github.workspace }}:/scan security-scanner /scan --severity high
```

### Save Results to File

```bash
# Save JSON output to a file
docker run --rm -v $(pwd):/scan security-scanner /scan --output json > scan-results.json

# Save console output to a file
docker run --rm -v $(pwd):/scan security-scanner /scan > scan-report.txt
```

## Tips

1. **Always use `--rm`** - Automatically removes the container after it exits
2. **Mount as read-only** - The scanner only reads files, so mounting as `:ro` is safer
3. **Use absolute paths** - More reliable than relative paths
4. **Check exit codes** - Exit code 1 means critical/high issues found (useful for CI/CD)

## Troubleshooting

### Docker daemon not running
```bash
# Start Docker Desktop (Mac/Windows)
# Or start Docker service (Linux)
sudo systemctl start docker
```

### Permission issues
```bash
# On Linux, you might need to add your user to docker group
sudo usermod -aG docker $USER
# Then log out and back in
```

### File not found errors
Make sure the path you're mounting exists and is accessible.

