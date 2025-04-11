import os
import shutil
import subprocess

from abc import ABC, abstractmethod

# __all__ = ["build_project", "generate_cmakelists"]


# _PROJECT_EXECUTABLE_CMAKE_VAR_NAME = "PROJECT_EXECUTABLE_NAME"
# _PROJECT_STATIC_LIBRARY_CMAKE_VAR_NAME = "PROJECT_STATIC_LIBRARY_NAME"
# _PROJECT_SHARED_LIBRARY_CMAKE_VAR_NAME = "PROJECT_SHARED_LIBRARY_NAME"


# # def _list_folder_contents(directory, indent=0):
# #     try:
# #         with os.scandir(directory) as entries:
# #             for entry in entries:
# #                 if entry.is_file():
# #                     name, ext = os.path.splitext(entry.name)
# #                     print("  " * indent + f"File: {name} (Extension: {ext})")
# #                 elif entry.is_dir():
# #                     print("  " * indent + f"Folder: {entry.name}")
# #                     _list_folder_contents(entry.path, indent + 1)
# #                 else:
# #                     print("  " * indent + f"Unknown: {entry.name}")
# #     except PermissionError:
# #         print("  " * indent + "[Permission Denied]")


def _adapt_to_cmake_bool(value: bool) -> str:
    return "ON" if value else "OFF"


# def _write_work_variables(file):
#     file.write( f"set(LIBRARY_NAME \"ProjectLibrary\")\n"
#                 f"set(EXECUTABLE_NAME \"ProjectExecutable\")\n"
#                 f"set(CURRENT_DIRECTORY \"./\")\n"
#                )
#     file.write( f"\n")


class _IGeneratorPart(ABC):
    @abstractmethod
    def generate(self: object, file) -> None:
        pass


class _HeaderGeneratorPart(_IGeneratorPart):
    def __init__(
            self: object,
            cmake_minimum_required_version: str,
            project_name: str,
            project_version_major: int,
            project_version_minor: int,
            project_version_patch: str,
            c_language_standard: int,
            c_language_standard_required: bool,
            c_compiler_extensions_required: bool,
            cpp_language_standard: int,
            cpp_language_standard_required: bool,
            cpp_compiler_extensions_required: bool
    ):
        self._cmake_minimum_required_version = cmake_minimum_required_version
        self._project_name = project_name
        self._project_version_major = project_version_major
        self._project_version_minor = project_version_minor
        self._project_version_patch = project_version_patch
        self._c_language_standard = c_language_standard
        self._c_language_standard_required = c_language_standard_required
        self._c_compiler_extensions_required = c_compiler_extensions_required
        self._cpp_language_standard = cpp_language_standard
        self._cpp_language_standard_required = cpp_language_standard_required
        self._cpp_compiler_extensions_required = cpp_compiler_extensions_required

    def generate(self: object, file):
        self._write_cmake_minimum_required_version(file)
        self._write_project_specifications(file)
        self._write_language_specifications(file)
        self._write_destination_specifications(file)

    def _write_cmake_minimum_required_version(self: object, file) -> None:
        file.write( f"cmake_minimum_required(VERSION "
                    f"{self._cmake_minimum_required_version} "
                    f"FATAL_ERROR)\n"
                    )
        file.write( f"\n")

    def _write_project_specifications(self: object, file) -> None:
        file.write( f"project({self._project_name} "
                    f"VERSION {self._project_version_major}.{self._project_version_minor}.{self._project_version_patch} "
                    f"LANGUAGES C CXX)\n"
                    )
        file.write( f"\n")

    def _write_language_specifications(self: object, file) -> None:
        file.write( f"set(CMAKE_C_STANDARD {self._c_language_standard})\n"
                    f"set(CMAKE_C_STANDARD_REQUIRED {_adapt_to_cmake_bool(self._c_language_standard_required)})\n"
                    f"set(CMAKE_C_EXTENSIONS {_adapt_to_cmake_bool(self._c_compiler_extensions_required)})\n\n"

                    f"set(CMAKE_cpp_standard {self._cpp_language_standard})\n"
                    f"set(CMAKE_cpp_standard_REQUIRED {_adapt_to_cmake_bool(self._cpp_language_standard_required)})\n"
                    f"set(CMAKE_cpp_extensions {_adapt_to_cmake_bool(self._cpp_compiler_extensions_required)})\n"
                    )
        file.write( f"\n")

    def _write_destination_specifications(self: object, file) -> None:
        file.write( f"set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/bin)\n"
                    f"set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/lib)\n"
                    f"set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/lib)\n"
                    )
        file.write( f"\n")


class _Generator:
    def __init__(self: object):
        self._parts: list[_IGeneratorPart] = []

    def generate(self: object, file) -> None:
        for part in self._parts:
            part.generate(file)

    def ready(self: object) -> bool:
        return self._parts.count() > 0

    def reset(self: object) -> None:
        self._parts.clear()

    def add_part(self: object, part: _IGeneratorPart) -> None:
        self._parts.append(part)


class _GeneratorBuilder:
    def __init__(self: object):
        self._generator = _Generator()

    @property
    def generator(self: object) -> _Generator:
        return self._generator

    def add_header(
            self: object,
            cmake_minimum_required_version: str,
            project_name: str,
            project_version_major: int,
            project_version_minor: int,
            project_version_patch: str,
            c_language_standard: int,
            c_language_standard_required: bool,
            c_compiler_extensions_required: bool,
            cpp_language_standard: int,
            cpp_language_standard_required: bool,
            cpp_compiler_extensions_required: bool
    ) -> None:
        part = _HeaderGeneratorPart(
                    cmake_minimum_required_version,
                    project_name,
                    project_version_major,
                    project_version_minor,
                    project_version_patch,
                    c_language_standard,
                    c_language_standard_required,
                    c_compiler_extensions_required,
                    cpp_language_standard,
                    cpp_language_standard_required,
                    cpp_compiler_extensions_required
                )
        self._generator.add_part(part)


def generate(
        cmake_minimum_required_version: str,
        project_root_path: str,
        project_name: str,
        project_build_type: str,
        project_version_major: int,
        project_version_minor: int,
        project_version_patch: str,
        c_language_standard: int,
        c_language_standard_required: bool,
        c_compiler_extensions_required: bool,
        cpp_language_standard: int,
        cpp_language_standard_required: bool,
        cpp_compiler_extensions_required: bool,
        cmake_compile_definitions: list
) -> None:
        builder = _GeneratorBuilder()

        # Header is the same for all cases
        builder.add_header(
                    cmake_minimum_required_version,
                    project_name,
                    project_version_major,
                    project_version_minor,
                    project_version_patch,
                    c_language_standard,
                    c_language_standard_required,
                    c_compiler_extensions_required,
                    cpp_language_standard,
                    cpp_language_standard_required,
                    cpp_compiler_extensions_required
                )

        match project_build_type:
            case "app":
                pass
            case "lib":
                pass
            case "dll":
                pass
            case "tmp":
                pass
            case _:
                raise None

        with open(os.path.join(project_root_path, "CMakeLists.txt"), "w") as cmakelists_root_file:
            builder.generator.generate(cmakelists_root_file)


def build(
        project_root_path: str,
        cmake_generator: str,
        c_compiler_path: str=None,
        cpp_compiler_path: str=None,
        clear: bool=False
) -> None:
    build_path = os.path.join(project_root_path, "build")

    if clear:
        if os.path.exists(build_path) and os.path.isdir(build_path):
            shutil.rmtree(build_path)

    cmd_generate_text = f"cmake -S \"{project_root_path}\" -G \"{cmake_generator}\" -B \"{build_path}\""

    if c_compiler_path:
        cmd_generate_text += f" -D CMAKE_C_COMPILER=\"{c_compiler_path}\""

    if cpp_compiler_path:
        cmd_generate_text += f" -D CMAKE_CXX_COMPILER=\"{cpp_compiler_path}\""

    cmd_build_text = f"cmake --build \"{build_path}\""

    subprocess.check_call(cmd_generate_text, shell=True)
    subprocess.check_call(cmd_build_text, shell=True)
