#!/bin/bash

echo "Running tests in fixed order..."
python3 -m unittest test_todos_api.py
python3 -m unittest test_projects_api.py
python3 -m unittest test_categories_api.py

echo "Tests in order completed."

echo "Running tests in random order..."
python3 -m pytest --random-order .

echo "Tests in random order completed."