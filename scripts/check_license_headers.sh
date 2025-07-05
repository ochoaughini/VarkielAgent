#!/bin/bash

# Check for SPDX license headers in all Python files
find src -type f -name "*.py" | while read file; do
    if ! grep -q "SPDX-License-Identifier" "$file"; then
        echo "Missing license header in $file"
        exit 1
    fi
done

echo "All files have license headers"
exit 0
