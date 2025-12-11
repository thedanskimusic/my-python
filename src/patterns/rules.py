"""
Security pattern definitions for scanning
"""

import re
from typing import Dict, List, Tuple

# Secret detection patterns
SECRET_PATTERNS: List[Dict[str, any]] = [
    {
        "name": "API Key",
        "pattern": re.compile(r'(?i)(api[_-]?key|apikey)\s*[=:]\s*["\']?([a-zA-Z0-9_\-]{20,})["\']?', re.IGNORECASE),
        "severity": "high",
        "description": "Potential API key found"
    },
    {
        "name": "AWS Access Key",
        "pattern": re.compile(r'AKIA[0-9A-Z]{16}'),
        "severity": "critical",
        "description": "AWS Access Key ID detected"
    },
    {
        "name": "AWS Secret Key",
        "pattern": re.compile(r'(?i)(aws[_-]?secret[_-]?access[_-]?key|aws[_-]?secret)\s*[=:]\s*["\']?([A-Za-z0-9/+=]{40})["\']?'),
        "severity": "critical",
        "description": "AWS Secret Access Key detected"
    },
    {
        "name": "Password",
        "pattern": re.compile(r'(?i)(password|passwd|pwd)\s*[=:]\s*["\']?([^\s"\']{8,})["\']?', re.IGNORECASE),
        "severity": "high",
        "description": "Potential password found"
    },
    {
        "name": "Private Key",
        "pattern": re.compile(r'-----BEGIN\s+(RSA|DSA|EC|OPENSSH)\s+PRIVATE KEY-----'),
        "severity": "critical",
        "description": "Private key file detected"
    },
    {
        "name": "GitHub Token",
        "pattern": re.compile(r'ghp_[a-zA-Z0-9]{36}'),
        "severity": "high",
        "description": "GitHub Personal Access Token detected"
    },
    {
        "name": "Generic Token",
        "pattern": re.compile(r'(?i)(token|secret|key)\s*[=:]\s*["\']?([a-zA-Z0-9_\-]{32,})["\']?', re.IGNORECASE),
        "severity": "medium",
        "description": "Potential token or secret found"
    },
    {
        "name": "Database Connection String",
        "pattern": re.compile(r'(?i)(mysql|postgres|mongodb)://[^\s"\']+:[^\s"\']+@', re.IGNORECASE),
        "severity": "high",
        "description": "Database connection string with credentials"
    },
]

# Vulnerability patterns
VULNERABILITY_PATTERNS: List[Dict[str, any]] = [
    {
        "name": "SQL Injection Risk",
        "pattern": re.compile(r'(?i)(execute|query|exec)\s*\([^)]*\+.*["\']', re.IGNORECASE),
        "severity": "high",
        "description": "Potential SQL injection vulnerability - string concatenation in query"
    },
    {
        "name": "Eval Usage",
        "pattern": re.compile(r'\beval\s*\('),
        "severity": "high",
        "description": "Use of eval() can be dangerous - allows code execution"
    },
    {
        "name": "Exec Usage",
        "pattern": re.compile(r'\bexec\s*\('),
        "severity": "high",
        "description": "Use of exec() can be dangerous - allows code execution"
    },
    {
        "name": "Hardcoded IP Address",
        "pattern": re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'),
        "severity": "low",
        "description": "Hardcoded IP address found"
    },
    {
        "name": "Insecure Random",
        "pattern": re.compile(r'random\.(random|randint|choice)\s*\('),
        "severity": "medium",
        "description": "Use of insecure random - consider secrets module for crypto"
    },
    {
        "name": "Shell Command Injection",
        "pattern": re.compile(r'(?i)(os\.system|subprocess\.call|subprocess\.Popen)\s*\([^)]*\+', re.IGNORECASE),
        "severity": "high",
        "description": "Potential shell command injection - string concatenation in system call"
    },
]

# File extensions to scan
CODE_FILE_EXTENSIONS = {
    '.py', '.js', '.ts', '.java', '.go', '.rb', '.php', '.cpp', '.c', '.h',
    '.cs', '.swift', '.kt', '.scala', '.rs', '.sh', '.bash', '.zsh'
}

CONFIG_FILE_EXTENSIONS = {
    '.json', '.yaml', '.yml', '.toml', '.ini', '.conf', '.config', '.env',
    '.properties', '.xml'
}

# Files/directories to ignore
IGNORE_PATTERNS = {
    'venv', 'env', '.venv', '__pycache__', 'node_modules', '.git',
    '.pytest_cache', 'dist', 'build', '.idea', '.vscode'
}

