import os
import shutil
import subprocess

from .generatorbuilder import GeneratorBuilder


def _get_include_dirs(include_path) -> list[str]:
    pass


def _get_sources(source_path) -> list[str]:
    ret: list[str] = []

    for dirpath, _, filenames in os.walk(source_path):
        for filename in filenames:
            if filename.endswith(('.c', '.cpp')):
                relative_path = os.path.relpath(os.path.join(dirpath, filename),
                                                start=os.path.dirname(source_path))
                ret.append(relative_path.replace(os.path.sep, '/'))

    return ret


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
        cmakelists_path = os.path.join(project_root_path, "CMakeLists.txt")
        include_path = os.path.join(project_root_path, "include")
        source_path = os.path.join(project_root_path, "source")
        app_path = os.path.join(project_root_path, "app")

        include_directories = _get_include_dirs(include_path)
        source_files = _get_sources(source_path)

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
                builder.add_static_library(
                            project_name,
                            include_directories,
                            source_files
                        )
                # builder.add_executable()
            case "lib":
                pass
                # builder.add_static_library()
            case "dll":
                pass
                # builder.add_static_library()
                # builder.add_shared_library()
            case "tmp":
                pass
            case _:
                raise None

        with open(cmakelists_path, "w") as cmakelists_root_open_file:
            builder.generator.generate(cmakelists_root_open_file)


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
