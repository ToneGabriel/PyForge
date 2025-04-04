import os


__all__ = ["build_project", "generate_cmakelists"]


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
        project_name: str,
        project_version_major: int,
        project_version_minor: int,
        project_version_patch: int
) -> None:
    file.write( f"project("
                f"{project_name} "
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


def _write_subdirs_to_add(
        file,
        *subdirs: str
) -> None:
    for dir in subdirs:
        file.write(f"add_subdirectory({dir})\n")
    file.write( f"\n")


def _write_work_variables(file):
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


def generate_root_cmakelists(
        project_root_dir: str,
        cmake_minimum_required_version: str,
        project_name: str,
        project_version_major: int,
        project_version_minor: int,
        project_version_patch: str,
        c_standard: int,
        c_standard_required: bool,
        c_extensions: bool,
        cpp_standard: int,
        cpp_standard_required: bool,
        cpp_extensions: bool
) -> None:
    with open(os.path.join(project_root_dir, "CMakeLists.txt"), "w") as cmake_root_file:
        _write_cmake_minimum_required_version(cmake_root_file, cmake_minimum_required_version)
        _write_project_specifications(cmake_root_file,
                                      project_name,
                                      project_version_major, project_version_minor, project_version_patch)
        _write_language_specifications( cmake_root_file,
                                        c_standard, c_standard_required, c_extensions,
                                        cpp_standard, cpp_standard_required, cpp_extensions)
        _write_destination_specifications(cmake_root_file)
        _write_subdirs_to_add(cmake_root_file, "include", "source", "app", "extern", "test")


def generate_include_recursive_cmakelists(project_root_dir: str) -> None:
    pass


def generate_source_recursive_cmakelists(project_root_dir: str) -> None:
    pass


def generate_app_cmakelists(project_root_dir: str) -> None:
    pass
