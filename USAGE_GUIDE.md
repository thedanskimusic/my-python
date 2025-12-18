# Security Scanner - Usage Guide

## Quick Start

The scanner can be run from **anywhere** once the Docker image is built!

## Method 1: Direct Docker Command (Works from anywhere)

```bash
# Scan any directory
docker run --rm -it -v /path/to/target:/scan security-scanner /scan

# Scan current directory
docker run --rm -it -v $(pwd):/scan security-scanner /scan

# Dependencies
docker run --rm -it -v $(pwd):/scan security-scanner /scan --dependencies

# With options
docker run --rm -it -v /path/to/target:/scan security-scanner /scan --severity high --output json

# LLM analysis (requires GEMINI_API_KEY)
docker run --rm -it -v /path/to/target:/scan -e GEMINI_API_KEY security-scanner /scan --llm
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
alias security-scan='docker run --rm -it -v'

# Or more complete (handles current directory)
alias security-scan='f(){ docker run --rm -it -v "$(pwd)":/scan security-scanner /scan "$@"; }; f'
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
docker run --rm -it -v ~/code/my-other-project:/scan security-scanner /scan
```

### Scan Current Directory

```bash
# Navigate to any project
cd ~/code/some-project
docker run --rm -it -v $(pwd):/scan security-scanner /scan
```

### Scan with Specific Options

```bash
# Only high/critical issues, JSON output
docker run --rm -it -v ~/code/my-project:/scan security-scanner /scan --severity high --output json

# Only secrets, no vulnerabilities
docker run --rm -it -v ~/code/my-project:/scan security-scanner /scan --no-vulns

# Save results to file
docker run --rm -it -v ~/code/my-project:/scan security-scanner /scan --output json > scan-results.json

# LLM security analysis
export GEMINI_API_KEY="your-api-key-here"
docker run --rm -it -v ~/code/my-project:/scan -e GEMINI_API_KEY security-scanner /scan --llm

# Or provide API key via CLI
docker run --rm -it -v ~/code/my-project:/scan security-scanner /scan --llm --api-key "your-api-key-here"

# Combine LLM with other scans
docker run --rm -it -v ~/code/my-project:/scan -e GEMINI_API_KEY security-scanner /scan --llm --dependencies
```

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Security Scan
  run: |
    docker run --rm -it -v ${{ github.workspace }}:/scan security-scanner /scan --severity high
```

## LLM Security Analysis

The scanner can use Google's Gemini 2.5 Flash to perform deep security analysis of your codebase. This complements pattern-based scanning by identifying issues like:
- Unsecured API endpoints
- Missing authentication/authorization
- Input validation problems
- Sensitive data exposure risks
- General security best practice violations

**Important:** You need your own Gemini API key. The scanner does not include a shared key - each user must provide their own.

**Getting Your API Key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in and create a new API key (free tier available)

**Providing Your API Key:**

**Method 1: Environment Variable** (Best for CI/CD)
```bash
export GEMINI_API_KEY="your-api-key"
docker run --rm -it -v $(pwd):/scan -e GEMINI_API_KEY security-scanner /scan --llm
```

**Method 2: CLI Option** (Convenient for one-off scans)
```bash
docker run --rm -it -v $(pwd):/scan security-scanner /scan --llm --api-key "your-api-key"
```

**Method 3: Config File** (Persistent, good for local use)
```bash
# Option A: Home directory config (applies to all projects)
mkdir -p ~/.security-scanner
echo '{"gemini_api_key": "your-api-key"}' > ~/.security-scanner/config.json

# Option B: Project-specific config
echo '{"gemini_api_key": "your-api-key"}' > .security-scanner.json
```

The scanner checks in this order: CLI option → Environment variable → `~/.security-scanner/config.json` → `.security-scanner.json`

**Examples:**
```bash
# Basic LLM scan with env var
export GEMINI_API_KEY="your-api-key"
docker run --rm -it -v $(pwd):/scan -e GEMINI_API_KEY security-scanner /scan --llm

# LLM with other scans
docker run --rm -it -v $(pwd):/scan -e GEMINI_API_KEY security-scanner /scan --llm --dependencies

# Using config file (no need to set env var)
docker run --rm -it -v $(pwd):/scan -v ~/.security-scanner:/root/.security-scanner security-scanner /scan --llm
```

**Note:** The LLM scanner analyzes the entire repository for better context. Very large repositories may be truncated to stay within token limits. API usage counts against your Google AI Studio quota.

## Tips

1. **The image is stored locally** - Once built, you can use it from anywhere
2. **Use absolute paths** - More reliable than relative paths
3. **Use `-it` flags** - Enables interactive mode for better terminal output and spinner animations (especially in Mac Terminal)
4. **Mount as read-only** - The scanner only reads files (add `:ro` if you want extra safety)
5. **Exit codes** - Exit code 1 means critical/high issues found (useful for CI/CD)
6. **LLM scanning** - Requires API key and sends code to Google's API (be aware of privacy implications)

## Where is the Image?

The Docker image is stored in your local Docker registry. You can see it with:
```bash
docker images | grep security-scanner
```

It's available system-wide, so you can use it from any directory!

