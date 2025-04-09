import os
import shutil
import subprocess


# __all__ = ["build_project", "generate_cmakelists"]


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


def _get_build_path(project_root_path: str) -> str:
    return os.path.join(project_root_path, "build")


def _get_cmakelists_file(project_root_path: str) -> str:
    return os.path.join(project_root_path, "CMakeLists.txt")


def _adapt_to_cmake_bool(value: bool) -> str:
    return "ON" if value else "OFF"


def _write_cmake_minimum_required_version(
        file,
        cmake_minimum_required_version: str
) -> None:
    file.write( f"cmake_minimum_required(VERSION "
                f"{cmake_minimum_required_version} "
                f"FATAL_ERROR)\n"
                )
    file.write( f"\n")


def _write_project_specifications(
        file,
        project_version_major: int,
        project_version_minor: int,
        project_version_patch: int
) -> None:
    file.write( f"project(pyforge_PROJECT "
                f"VERSION {project_version_major}.{project_version_minor}.{project_version_patch} "
                f"LANGUAGES C CXX)\n"
                )
    file.write( f"\n")


def _write_language_specifications(
        file,
        c_standard: int,
        c_standard_required: bool,
        c_extensions: bool,
        cpp_standard: int,
        cpp_standard_required: bool,
        cpp_extensions: bool
) -> None:
    file.write( f"set(CMAKE_C_STANDARD {c_standard})\n"
                f"set(CMAKE_C_STANDARD_REQUIRED {_adapt_to_cmake_bool(c_standard_required)})\n"
                f"set(CMAKE_C_EXTENSIONS {_adapt_to_cmake_bool(c_extensions)})\n\n"

                f"set(CMAKE_cpp_standard {cpp_standard})\n"
                f"set(CMAKE_cpp_standard_REQUIRED {_adapt_to_cmake_bool(cpp_standard_required)})\n"
                f"set(CMAKE_cpp_extensions {_adapt_to_cmake_bool(cpp_extensions)})\n"
                )
    file.write( f"\n")


def _write_destination_specifications(file) -> None:
    file.write(f"set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/bin)\n"
               f"set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/lib)\n"
               f"set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/lib)\n"
               )
    file.write( f"\n")


# def _write_work_variables(file):
#     file.write( f"set(LIBRARY_NAME \"ProjectLibrary\")\n"
#                 f"set(EXECUTABLE_NAME \"ProjectExecutable\")\n"
#                 f"set(CURRENT_DIRECTORY \"./\")\n"
#                )
#     file.write( f"\n")


def generate(
        project_root_path: str,
        cmake_minimum_required_version: str,
        build_type: str,
        project_version_major: int,
        project_version_minor: int,
        project_version_patch: str,
        c_standard: int,
        c_standard_required: bool,
        c_extensions: bool,
        cpp_standard: int,
        cpp_standard_required: bool,
        cpp_extensions: bool,
        cmake_compile_definitions: list
) -> None:
    with open(_get_cmakelists_file(project_root_path), "w") as cmakelists_root_file:
        _write_cmake_minimum_required_version(cmakelists_root_file, cmake_minimum_required_version)
        _write_project_specifications(cmakelists_root_file,
                                      project_version_major, project_version_minor, project_version_patch)
        _write_language_specifications( cmakelists_root_file,
                                        c_standard, c_standard_required, c_extensions,
                                        cpp_standard, cpp_standard_required, cpp_extensions)
        _write_destination_specifications(cmakelists_root_file)


def clear(project_root_path: str) -> None:
    os.remove(_get_cmakelists_file(project_root_path))


def build(
        project_root_path: str,
        cmake_generator: str,
        c_compiler_path: str=None,
        cpp_compiler_path: str=None,
        clear: bool=False
) -> None:
    build_path = _get_build_path(project_root_path)

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
