# Path: src/utils/helpers.py

import json

def load_json(file_path):
    """Loads JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(data, file_path):
    """Saves JSON data to a file."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)