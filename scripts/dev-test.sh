#!/bin/bash
# Development testing script
# Rebuilds and tests the scanner
# Usage: ./scripts/dev-test.sh [target]

TARGET="${1:-test_security.py}"

echo "🔨 Rebuilding..."
docker build -t security-scanner . > /dev/null 2>&1

echo "🧪 Testing on: $TARGET"
echo ""

if [ -f "$TARGET" ]; then
    docker run --rm -v "$(pwd)":/scan security-scanner "/scan/$TARGET"
else
    docker run --rm -v "$(pwd)":/scan security-scanner "/scan/$TARGET"
fi

