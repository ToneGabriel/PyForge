import subprocess
import textwrap
import os

from rich.console import Console
from rich.prompt import Prompt

from . import structure
from . import cmake
from . import jsonvalid


_MAIN_CONSOLE = Console()


_EXPECTED_BUILD_JSON_STRUCTURE = {
    "project_root_directory": str,
    "project_type": str,
    "project_version":
    {
        "major": int,
        "minor": int,
        "patch": int
    },

    "c_compiler_path": str,
    "c_standard": int,
    "c_standard_required": bool,
    "c_extensions": bool,

    "cpp_compiler_path": str,
    "cpp_standard": int,
    "cpp_standard_required": bool,
    "cpp_extensions": bool,

    "cmake_generator": str,
    "cmake_compile_definitions": list
}   # END _EXPECTED_BUILD_JSON_STRUCTURE


class ProjectSetupData:
    '''Description'''

    _CMAKE_MINIMUM_REQUIRED_VERSION = "3.22.1"

    def __init__(self: object, json_path: str):
        self._data = jsonvalid.load(json_path, _EXPECTED_BUILD_JSON_STRUCTURE)

    # @property
    # def cmake_minimum_required_version(self: object) -> str:
    #     return ProjectSetupData._CMAKE_MINIMUM_REQUIRED_VERSION
    
    # @property
    # def project_directory_path(self: object) -> str:
    #     return self._project_dir_path

    # @property
    # def build_type(self: object) -> str:
    #     return self._data["build_type"]
    
    # @property
    # def c_compiler_path(self: object) -> str:
    #     return self._data["c_compiler_path"]

    # @property
    # def c_standard(self: object) -> int:
    #     return self._data["c_standard"]

    # @property
    # def c_standard_required(self: object) -> bool:
    #     return self._data["c_standard_required"]
    
    # @property
    # def c_extensions(self: object) -> bool:
    #     return self._data["c_extensions"]

    # @property
    # def cpp_compiler_path(self: object) -> str:
    #     return self._data["cpp_compiler_path"]

    # @property
    # def cpp_standard(self: object) -> int:
    #     return self._data["cpp_standard"]

    # @property
    # def cpp_standard_required(self: object) -> bool:
    #     return self._data["cpp_standard_required"]

    # @property
    # def cpp_extensions(self: object) -> bool:
    #     return self._data["cpp_extensions"]

    # @property
    # def cmake_generator(self: object) -> str:
    #     return self._data["cmake_generator"]

    # @property
    # def cmake_compile_definitions_def(self: object) -> list[str]:
    #     return self._data["cmake_compile_definitions"]["def"]

    # @property
    # def cmake_compile_definitions_val(self: object) -> list[tuple[str, str]]:
    #     return self._data["cmake_compile_definitions"]["val"]

    # @property
    # def project_name(self: object) -> str: 
    #     return self._data["project_name"]

    # @property
    # def project_version_major(self: object) -> int:
    #     return self._data["project_version"]["major"]

    # @property
    # def project_version_minor(self: object) -> int:
    #     return self._data["project_version"]["minor"]

    # @property
    # def project_version_patch(self: object) -> int:
    #     return self._data["project_version"]["patch"]


def _run_command(command: str) -> None:
    """
    Helper function to run a command in the shell.
    
    :param command: executes command in the shell.
    :raises subprocess.CalledProcessError: if command fails
    """

    _MAIN_CONSOLE.print(f"Running command: {command}")
    subprocess.check_call(command, shell=True)


# def _generate_project_cmakelists(project_path: str, data: ProjectSetupData) -> None:
#     cmake.generate_root_cmakelists(
#         project_path,
#         data.cmake_minimum_required_version,
#         data.project_name,
#         data.project_version_major,
#         data.project_version_minor,
#         data.project_version_patch,
#         data.c_standard,
#         data.c_standard_required,
#         data.c_extensions,
#         data.cpp_standard,
#         data.cpp_standard_required,
#         data.cpp_extensions
#     )

#     cmake.generate_include_recursive_cmakelists(project_path)
#     cmake.generate_source_recursive_cmakelists(project_path)
#     cmake.generate_app_cmakelists(project_path)


# def _clear_project_cmakelists(project_path: str) -> None:
#     pass


# def _build_project(project_path: str, data: ProjectSetupData) -> None:
#     pass


def main(json_path) -> None:
    while True:
        try:
            _MAIN_CONSOLE.print(textwrap.dedent(
            '''
            ===============================================
                                PyForge
            ===============================================
            Select an option:
            0. Setup Project Structure
            1. Generate CMakeLists
            2. Clear CMakeLists
            3. Build Project
            4. Exit"
            '''
            ))

            choice = Prompt.ask("Please enter your choice", choices=["0", "1", "2", "3", "4"])

            if choice == "4":
                _MAIN_CONSOLE.print("Exiting... Goodbye!", style="yellow")
                return
            else:
                data = ProjectSetupData(json_path)

                if choice == "0":
                    _MAIN_CONSOLE.print("Setting Project Structure...", style="yellow")
                    # structure.setup_project_structure("./structure.zip", "./test")
                elif choice == "1":
                    _MAIN_CONSOLE.print("Generating CMakeLists...", style="yellow")
                    # _generate_project_cmakelists(project_path, data)
                elif choice == "2":
                    _MAIN_CONSOLE.print("Clearing CMakeLists...", style="yellow")
                    # _clear_project_cmakelists(project_path)
                elif choice == "3":
                    _MAIN_CONSOLE.print("Building Project...", style="yellow")
                    # _build_project(project_path, data)
                else:
                    _MAIN_CONSOLE.print("Invalid choice...", style="red")
        except Exception as e:
            _MAIN_CONSOLE.print(f"Operation failed: {e}", style="red")
        else:
            _MAIN_CONSOLE.print("Operation successful!", style="green")

        if Prompt.ask("Continue?", choices=["y", "n"]) == "n":
            _MAIN_CONSOLE.print("Exiting... Goodbye!", style="yellow")
            return
