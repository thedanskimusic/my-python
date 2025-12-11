#!/bin/bash
# Quick rebuild script for the security scanner
# Usage: ./scripts/rebuild.sh

set -e

echo "🔨 Rebuilding security-scanner Docker image..."
docker build -t security-scanner .

echo "✅ Build complete!"
echo ""
echo "Test it with:"
echo "  docker run --rm -v \$(pwd):/scan security-scanner /scan/test_security.py"

