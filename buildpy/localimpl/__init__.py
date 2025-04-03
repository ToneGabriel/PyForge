import subprocess
import textwrap
import os

from rich.console import Console
from rich.prompt import Prompt

from . import cmake
from . import jsonvalid


MAIN_CONSOLE = Console()


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


class BuildDataParser:
    '''Description'''

    _CMAKE_MINIMUM_REQUIRED_VERSION = "3.22.1"

    def __init__(self: object, json_path: str):
        self._data = jsonvalid.load(json_path, _EXPECTED_BUILD_JSON_STRUCTURE)

    @property
    def cmake_minimum_required_version(self: object) -> str:
        return BuildDataParser._CMAKE_MINIMUM_REQUIRED_VERSION
    
    @property
    def project_directory_path(self: object) -> str:
        return self._project_dir_path

    @property
    def build_type(self: object) -> str:
        return self._data["build_type"]
    
    @property
    def c_compiler_path(self: object) -> str:
        return self._data["c_compiler_path"]

    @property
    def c_standard(self: object) -> int:
        return self._data["c_standard"]

    @property
    def c_standard_required(self: object) -> bool:
        return self._data["c_standard_required"]
    
    @property
    def c_extensions(self: object) -> bool:
        return self._data["c_extensions"]

    @property
    def cpp_compiler_path(self: object) -> str:
        return self._data["cpp_compiler_path"]

    @property
    def cpp_standard(self: object) -> int:
        return self._data["cpp_standard"]

    @property
    def cpp_standard_required(self: object) -> bool:
        return self._data["cpp_standard_required"]

    @property
    def cpp_extensions(self: object) -> bool:
        return self._data["cpp_extensions"]

    @property
    def cmake_generator(self: object) -> str:
        return self._data["cmake_generator"]

    @property
    def cmake_compile_definitions_def(self: object) -> list[str]:
        return self._data["cmake_compile_definitions"]["def"]

    @property
    def cmake_compile_definitions_val(self: object) -> list[tuple[str, str]]:
        return self._data["cmake_compile_definitions"]["val"]

    @property
    def project_name(self: object) -> str: 
        return self._data["project_name"]

    @property
    def project_version_major(self: object) -> int:
        return self._data["project_version"]["major"]

    @property
    def project_version_minor(self: object) -> int:
        return self._data["project_version"]["minor"]

    @property
    def project_version_patch(self: object) -> int:
        return self._data["project_version"]["patch"]


def _print_menu_and_get_choice() -> str:
    MAIN_CONSOLE.print(textwrap.dedent(
    '''
    ===============================================
                        PyForge
    ===============================================
    Select an option:
    1. Generate CMakeLists
    2. Clear CMakeLists
    3. Build Project
    4. Exit"
    '''
    ))

    return Prompt.ask("Please enter your choice", choices=["1", "2", "3", "4"])


def _run_command(command: str) -> None:
    """
    Helper function to run a command in the shell.
    
    :param command: executes command in the shell.
    :raises subprocess.CalledProcessError: if command fails
    """

    MAIN_CONSOLE.print(f"Running command: {command}")
    subprocess.check_call(command, shell=True)


def main(project_path, json_path) -> None:
    while True:
        try:
            choice = _print_menu_and_get_choice()

            if choice == "4":
                MAIN_CONSOLE.print("Exiting... Goodbye!", style="yellow")
                return
            else:
                data = BuildDataParser(json_path)

                if choice == "1":
                    MAIN_CONSOLE.print("Generating CMakeLists...", style="yellow")
                elif choice == "2":
                    MAIN_CONSOLE.print("Clearing CMakeLists...", style="yellow")
                elif choice == "3":
                    MAIN_CONSOLE.print("Building Project...", style="yellow")
                else:
                    MAIN_CONSOLE.print("Invalid choice...", style="red")
        except Exception as e:
            MAIN_CONSOLE.print(f"Operation failed: {e}", style="red")
        else:
            MAIN_CONSOLE.print("Operation successful!", style="green")
