#!/bin/bash
# Security Scanner Wrapper Script
# Usage: scan.sh <target> [options]
# Example: scan.sh ~/code/my-repo --severity high

TARGET="${1:-.}"

if [ ! -d "$TARGET" ] && [ ! -f "$TARGET" ]; then
    echo "Error: Target '$TARGET' does not exist"
    exit 1
fi

# Get absolute path
if [ -f "$TARGET" ]; then
    # For files, mount the parent directory and pass the file path
    TARGET_DIR=$(cd "$(dirname "$TARGET")" && pwd)
    TARGET_FILE=$(basename "$TARGET")
    docker run --rm -v "$TARGET_DIR":/scan security-scanner "/scan/$TARGET_FILE" "${@:2}"
else
    # For directories, mount the directory itself
    TARGET_ABS=$(cd "$TARGET" && pwd)
    docker run --rm -v "$TARGET_ABS":/scan security-scanner /scan "${@:2}"
fi

