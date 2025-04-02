import json


__all__ = ["JSONStructureError", "load_and_validate_json"]


class JSONStructureError(Exception):
    """Exception raised for invalid json file structure"""

    def __init__(self: object, message: str):
        super().__init__(message)


def load_and_validate_json(json_path: str, expected_json_structure:dict) -> dict:
    """
    Loads a JSON file and validates it against an expected schema.

    :param json_path: Path to the JSON file.
    :param expected_json_structure: Dictionary defining the expected structure.
    :return: Parsed JSON dictionary if valid, otherwise None.
    :raises FileNotFoundError: If the file does not exist.
    :raises json.JSONDecodeError: If the file contains invalid JSON.
    :raises InvalidJsonStructure: If the structure does not match expectations.
    """

    with open(json_path, "r") as file:
        json_data = json.load(file)
        _check_json_structure(json_data, expected_json_structure)
        return json_data


def _check_json_structure(json_data:dict, expected_json_structure:dict, path="") -> None:
    """
    Recursively validate a JSON object against the expected structure.

    :param json_data: The parsed JSON dictionary.
    :param expected_json_structure: The expected structure with types.
    :param path: Keeps track of the nested path for better error reporting.
    :raises InvalidJsonStructure: if the json structure does not match the expected structure
    """

    if not isinstance(json_data, dict):
        raise JSONStructureError(f"Error: Expected a dictionary at '{path}', but got {type(json_data).__name__}")

    for expected_key, expected_type in expected_json_structure.items():
        current_path = f"{path}.{expected_key}" if path else expected_key  # Track the nested key

        if expected_key not in json_data:
            raise JSONStructureError(f"Missing key: '{current_path}'")

        if not isinstance(expected_type, dict): # Validate primitive types
            if not isinstance(json_data[expected_key], expected_type):
                raise JSONStructureError(f"Incorrect type for '{current_path}': Expected {expected_type.__name__}, got {type(json_data[expected_key]).__name__}")
        else:   # Recurse for nested structures
            _check_json_structure(json_data[expected_key], expected_type, current_path)
