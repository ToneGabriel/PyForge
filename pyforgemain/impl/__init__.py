import subprocess
import textwrap

from rich.console import Console
from rich.prompt import Prompt

from . import structure
from . import cmake
from . import jsonvalid


_MAIN_CONSOLE = Console()


_EXPECTED_BUILD_JSON_STRUCTURE = {
    "project_settings":
    {
        "root": str,
        "build": str,
        "version":
        {
            "major": int,
            "minor": int,
            "patch": int
        }
    },

    "c_settings":
    {
        "compiler_path": str,
        "compiler_extensions_required": bool,
        "language_standard": int,
        "language_standard_required": bool
    },

    "cpp_settings":
    {
        "compiler_path": str,
        "compiler_extensions_required": bool,
        "language_standard": int,
        "language_standard_required": bool
    },

    "cmake_settings":
    {
        "generator": str,
        "compile_definitions": list
    }
}   # END _EXPECTED_BUILD_JSON_STRUCTURE


class ProjectSetupData:
    '''Description'''

    _CMAKE_MINIMUM_REQUIRED_VERSION: str = "3.22.1"

    def __init__(self: object, json_path: str):
        self._data = jsonvalid.load(json_path, _EXPECTED_BUILD_JSON_STRUCTURE)

    @property
    def cmake_minimum_required_version(self: object) -> str:
        return ProjectSetupData._CMAKE_MINIMUM_REQUIRED_VERSION

    @property
    def project_root_path(self: object) -> str:
        return self._data["project_settings"]["root"]

    @property
    def build_type(self: object) -> str:
        return self._data["project_settings"]["build"]

    @property
    def project_version_major(self: object) -> int:
        return self._data["project_settings"]["version"]["major"]
    
    @property
    def project_version_minor(self: object) -> int:
        return self._data["project_settings"]["version"]["minor"]
    
    @property
    def project_version_patch(self: object) -> int:
        return self._data["project_settings"]["version"]["patch"]

    @property
    def c_compiler_path(self: object) -> str:
        return self._data["c_settings"]["compiler_path"]

    @property
    def c_compiler_extensions_required(self: object) -> bool:
        return self._data["c_settings"]["compiler_extensions_required"]

    @property
    def c_language_standard(self: object) -> int:
        return self._data["c_settings"]["language_standard"]

    @property
    def c_language_standard_required(self: object) -> bool:
        return self._data["c_settings"]["language_standard_required"]

    @property
    def cpp_compiler_path(self: object) -> str:
        return self._data["cpp_settings"]["compiler_path"]

    @property
    def cpp_compiler_extensions_required(self: object) -> bool:
        return self._data["cpp_settings"]["compiler_extensions_required"]

    @property
    def cpp_language_standard(self: object) -> int:
        return self._data["cpp_settings"]["language_standard"]

    @property
    def cpp_language_standard_required(self: object) -> bool:
        return self._data["cpp_settings"]["language_standard_required"]

    @property
    def cmake_generator(self: object) -> str:
        return self._data["cmake_settings"]["generator"]

    @property
    def cmake_compile_definitions(self: object) -> list[tuple[str, str]]:
        return self._data["cmake_settings"]["compile_definitions"]


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


def main(json_path, zip_structure_path) -> None:
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
                    structure.setup_project(zip_structure_path, data.project_root_path)
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
