# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 01:55:22 2026

@author: ssj34
"""

import ast
import json

# Path to your functions.py file
functions_file = "taxcalc/functions_pit_kenya.py"

# Save to JSON
output_file = "taxcalc/function_names_pit_kenya.json"

# Read the Python file
with open(functions_file, "r", encoding="utf-8") as f:
    source = f.read()

# Parse the Python code
tree = ast.parse(source)

# Extract function names
function_names = [
    node.name
    for node in ast.walk(tree)
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
]

# Convert to the same structure as your JSON file
function_dict = {
    str(i): name
    for i, name in enumerate(function_names)
}

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(function_dict, f, indent=4)

# Display results
print(f"Found {len(function_names)} functions:")
for i, name in enumerate(function_names):
    print(i, name)

print(f"\nSaved to: {output_file}")