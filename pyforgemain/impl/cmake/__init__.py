import os
import shutil
import subprocess

from .generatorbuilder import GeneratorBuilder

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


# def _write_work_variables(file):
#     file.write( f"set(LIBRARY_NAME \"ProjectLibrary\")\n"
#                 f"set(EXECUTABLE_NAME \"ProjectExecutable\")\n"
#                 f"set(CURRENT_DIRECTORY \"./\")\n"
#                )
#     file.write( f"\n")


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
        builder = GeneratorBuilder()

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
