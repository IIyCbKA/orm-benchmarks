#!/bin/sh

cd $(dirname $0)

# Test 1 → Insert
python -m tests_sync.test_1

# Test 2 → Transaction Insert
python -m tests_sync.test_2

# Test 3 → Bulk Insert
python -m tests_sync.test_3

# Test 4 → Filter large
python -m tests_sync.test_4
