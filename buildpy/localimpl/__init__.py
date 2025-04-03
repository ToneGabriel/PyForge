import subprocess
import os

from . import cmake
from . import jsonvalid


_CMAKE_MINIMUM_REQUIRED_VERSION = "3.22.1"

_EXPECTED_BUILD_JSON_STRUCTURE = {
    "build_type": str,

    "c_compiler_path": str,
    "c_standard": int,
    "c_standard_required": bool,
    "c_extensions": bool,

    "cpp_compiler_path": str,
    "cpp_standard": int,
    "cpp_standard_required": bool,
    "cpp_extensions": bool,

    "cmake_generator": str,
    "cmake_compile_definitions":
    {
        "def": list,
        "val": list
    },

    "project_name": str,
    "project_version":
    {
        "major": int,
        "minor": int,
        "patch": int
    }
}   # END _EXPECTED_BUILD_JSON_STRUCTURE


def _run_command(command: str) -> None:
    """
    Helper function to run a command in the shell.
    
    :param command: executes command in the shell.
    :raises subprocess.CalledProcessError: if command fails
    """

    print(f"Running command: {command}")
    subprocess.check_call(command, shell=True)


def main(action: str, project_path: str, json_path: str):
    try:
        json_data: dict = jsonvalid.load(json_path, _EXPECTED_BUILD_JSON_STRUCTURE)

        if action == 'g':
            pass
        elif action == 'b':
            pass
        else:   # 'c'
            pass
    except Exception as e:
        print(e)
