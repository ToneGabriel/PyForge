import os
import sys
import subprocess

from .jsonhelp import *


__all__ = ["build_project", "generate_cmakelists"]


_EXPECTED_BUILD_JSON_STRUCTURE = {
    "project_path": str,
    "cmake_generator": str,
    "c_compiler_path": str,
    "cpp_compiler_path": str
}   # END _EXPECTED_BUILD_JSON_STRUCTURE

_EXPECTED_GENERATOR_JSON_STRUCTURE = {
    "cmake_minimum_required_version":
                                    {
                                        "major": int,
                                        "minor": int,
                                        "patch": int
                                    },

    "project_path": str,
    "project_name": str,
    "project_version":
                    {
                        "major": int,
                        "minor": int,
                        "patch": int
                    },

    "c_standard": int,
    "c_standard_required": bool,
    "c_extensions": bool,

    "cpp_standard": int,
    "cpp_standard_required": bool,
    "cpp_extensions": bool,
    
    "app_directory": str,
    "code_directory": str
}   # END _EXPECTED_GENERATOR_JSON_STRUCTURE


def _run_command(command: str) -> None:
    """
    Helper function to run a command in the shell.
    
    :param command: executes command in the shell.
    :raises subprocess.CalledProcessError: if command fails
    """

    print(f"Running command: {command}")
    subprocess.check_call(command, shell=True)


def build_project(json_path: str) -> None:
    """
    Configure and build a CMake project.

    :param json_path: Path to the JSON file.
    """

    try:
        # Load json file into dict
        json_data_dict = load_and_validate_json(json_path, _EXPECTED_BUILD_JSON_STRUCTURE)

        # Parse data
        project_path: str       = json_data_dict["project_path"]
        cmake_generator: str    = json_data_dict["cmake_generator"]
        c_compiler_path: str    = json_data_dict["c_compiler_path"]
        cpp_compiler_path: str  = json_data_dict["cpp_compiler_path"]

        # Check project path
        if not os.path.exists(project_path):
            print("Project path does not exist!")
            return
        else:
            # Navigate to the project directory
            os.chdir(project_path)

            # Run CMake to configure the project build
            if not c_compiler_path or not cpp_compiler_path:
                _run_command(f"cmake -G \"{cmake_generator}\" -B build")
            else:
                _run_command(f"cmake -G \"{cmake_generator}\"               \
                             -DCMAKE_C_COMPILER=\"{c_compiler_path}\"       \
                             -DCMAKE_CXX_COMPILER=\"{cpp_compiler_path}\"   \
                             -B build")

            # Build the project
            _run_command("cmake --build build")
    except Exception as e:
        print(e)


# def _list_folder_contents(directory, indent=0):
#     try:
#         with os.scandir(directory) as entries:
#             for entry in entries:
#                 if entry.is_file():
#                     name, ext = os.path.splitext(entry.name)
#                     print("  " * indent + f"File: {name} (Extension: {ext})")
#                 elif entry.is_dir():
#                     print("  " * indent + f"Folder: {entry.name}")
#                     _list_folder_contents(entry.path, indent + 1)
#                 else:
#                     print("  " * indent + f"Unknown: {entry.name}")
#     except PermissionError:
#         print("  " * indent + "[Permission Denied]")


def _adapt_to_cmake_bool(value: bool) -> str:
    return "ON" if value else "OFF"


def _write_cmake_minimum_required_version(file, cmake_minimum_required_version: dict):
    file.write( f"# CMake Specifications\n")
    file.write( f"cmake_minimum_required(VERSION "
                f"{cmake_minimum_required_version['major']}."
                f"{cmake_minimum_required_version['minor']}."
                f"{cmake_minimum_required_version['patch']} "
                f"FATAL_ERROR)\n"
                )
    file.write( f"\n")


def _write_project(file, project_name: str, project_version: dict):
    file.write( f"# Project Specifications\n")
    file.write( f"project("
                f"{project_name} "
                f"VERSION "
                f"{project_version['major']}."
                f"{project_version['minor']}."
                f"{project_version['patch']} "
                f"LANGUAGES C CXX)\n"
                )
    file.write( f"\n")


def _write_language_specifications(file,
                                   c_standard: int, c_standard_required: bool, c_extensions: bool,
                                   cpp_standard: int, cpp_standard_required: bool, cpp_extensions: bool):
    file.write( f"# Language Specifications\n")
    file.write( f"set(CMAKE_C_STANDARD {c_standard})\n"
                f"set(CMAKE_C_STANDARD_REQUIRED {_adapt_to_cmake_bool(c_standard_required)})\n"
                f"set(CMAKE_C_EXTENSIONS {_adapt_to_cmake_bool(c_extensions)})\n"

                f"set(CMAKE_cpp_standard {cpp_standard})\n"
                f"set(CMAKE_cpp_standard_REQUIRED {_adapt_to_cmake_bool(cpp_standard_required)})\n"
                f"set(CMAKE_cpp_extensions {_adapt_to_cmake_bool(cpp_extensions)})\n"
                )
    file.write( f"\n")


def _write_work_variables(file):
    file.write( f"# Work Variables\n")
    file.write( f"set(LIBRARY_NAME \"ProjectLibrary\")\n"
                f"set(EXECUTABLE_NAME \"ProjectExecutable\")\n"
                f"set(CURRENT_DIRECTORY \"./\")\n"
               )
    file.write( f"\n")


def _write_subdirectories(file, code_directory: str, app_directory: str):
    file.write( f"# CMakeLists subdirectory config\n")
    file.write( f"add_subdirectory({code_directory})\n"
                f"add_subdirectory({app_directory})\n"
               )
    file.write( f"\n")


def generate_cmakelists(json_path: str) -> None:

    try:
        json_data_dict = load_and_validate_json(json_path, _EXPECTED_GENERATOR_JSON_STRUCTURE)

        cmake_minimum_required_version: dict    = json_data_dict["cmake_minimum_required_version"]
        
        project_path: str                       = json_data_dict["project_path"]
        project_name: str                       = json_data_dict["project_name"]
        project_version: dict                   = json_data_dict["project_version"]
        
        c_standard: int                         = json_data_dict["c_standard"]
        c_standard_required: bool               = json_data_dict["c_standard_required"]
        c_extensions: bool                      = json_data_dict["c_extensions"]
        
        cpp_standard: int                       = json_data_dict["cpp_standard"]
        cpp_standard_required: bool             = json_data_dict["cpp_standard_required"]
        cpp_extensions: bool                    = json_data_dict["cpp_extensions"]
        
        app_directory: str                      = json_data_dict["app_directory"]
        code_directory: str                     = json_data_dict["code_directory"]

        with open(os.path.join(project_path, "CMakeLists.txt"), "w") as cmake_root_file:
            _write_cmake_minimum_required_version(cmake_root_file, cmake_minimum_required_version)
            _write_project(cmake_root_file, project_name, project_version)
            _write_language_specifications(cmake_root_file,
                                           c_standard, c_standard_required, c_extensions,
                                           cpp_standard, cpp_standard_required, cpp_extensions)
            _write_work_variables(cmake_root_file)
            _write_subdirectories(cmake_root_file, code_directory, app_directory)

    except Exception as e:
        print(e)
    

