#!/bin/bash

echo "Running tests in sequential order..."
echo "-----------------------------------"
python3 -m behave
echo "-----------------------------------"

sleep 2

echo
echo "==================================="
echo "=========== SWITCHING ============"
echo "==================================="
echo

echo "Running tests in random order..."
echo "-----------------------------------"

feature_files=$(find . -name "*.feature" | python3 -c "import sys, random; files = sys.stdin.read().splitlines(); random.shuffle(files); print(' '.join(files))")
python3 -m behave $feature_files

echo "-----------------------------------"
