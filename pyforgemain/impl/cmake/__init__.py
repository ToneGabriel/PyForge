import os
import subprocess

from .generatorbuilder import GeneratorBuilder


_MAIN_FILE_NAMES = {"main.c", "main.cpp"}
_SOURCE_EXTENSIONS = (".c", ".cpp")


def _get_include_dirs(include_path: str) -> list[str]:
    ret: list[str] = []

    for dirpath, _, _ in os.walk(include_path):
        relative_path = os.path.relpath(dirpath, start=os.path.dirname(include_path))
        ret.append(relative_path.replace(os.path.sep, '/'))

    return ret


def _get_sources(source_path: str) -> list[str]:
    ret: list[str] = []

    for dirpath, _, filenames in os.walk(source_path):
        for filename in filenames:
            if filename.endswith(_SOURCE_EXTENSIONS) and filename not in _MAIN_FILE_NAMES:
                relative_path = os.path.relpath(os.path.join(dirpath, filename),
                                                start=os.path.dirname(source_path))
                ret.append(relative_path.replace(os.path.sep, '/'))

    return ret


def _get_executable(source_path: str) -> str:
    for dirpath, _, filenames in os.walk(source_path):
        for filename in filenames:
            if filename in _MAIN_FILE_NAMES:
                relative_path = os.path.relpath(os.path.join(dirpath, filename),
                                                start=os.path.dirname(source_path))
                return relative_path.replace(os.path.sep, '/')

    return ""


def generate(
        project_root_path: str,
        project_name: str,
        project_build_type: str,
        project_version: str,
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
        test_path = os.path.join(project_root_path, "test")

        include_directories = _get_include_dirs(include_path)
        source_files = _get_sources(source_path)
        executable_file = _get_executable(source_path)

        test_source_files = _get_sources(test_path)
        test_executable_file = _get_executable(test_path)

        builder = GeneratorBuilder(
                    project_name,
                    project_version,
                    c_language_standard,
                    c_language_standard_required,
                    c_compiler_extensions_required,
                    cpp_language_standard,
                    cpp_language_standard_required,
                    cpp_compiler_extensions_required,
                    cmake_compile_definitions,
                    include_directories,
                    source_files,
                    executable_file,
                    test_source_files,
                    test_executable_file
                )

        # Header is the same for all cases
        builder.add_header()

        # Add test static library and include googletest headers to it
        builder.add_test_static_library()
        builder.add_test_executable()
        builder.add_googletest_configuration_then_include_dirs_to_test_static_library()

        match project_build_type:
            case "app":
                builder.add_project_static_library()
                builder.add_project_executable()
                builder.add_project_target_linker()
                builder.add_test_target_linker()
            case "lib":
                builder.add_project_static_library()
                builder.add_test_target_linker()
            case "dll":
                builder.add_project_shared_library()
                builder.add_project_static_library()
                builder.add_test_target_linker()
            case "tmp":
                builder.add_test_template_target_linker()
            case _:
                raise None

        with open(cmakelists_path, "w") as cmakelists_root_open_file:
            builder.generator_product.run(cmakelists_root_open_file)


def build(
        project_root_path: str,
        cmake_generator: str,
        c_compiler_path: str=None,
        cpp_compiler_path: str=None,
        clean: bool=False
) -> None:
    build_path = os.path.join(project_root_path, "build")

    if clean:
        if os.path.exists(build_path) and os.path.isdir(build_path):
            cmd_delete_build = f"rmdir /s /q \"{build_path}\""
            subprocess.check_call(cmd_delete_build, shell=True)

    cmd_generate_text = f"cmake -S \"{project_root_path}\" -G \"{cmake_generator}\" -B \"{build_path}\""

    if c_compiler_path:
        cmd_generate_text += f" -D CMAKE_C_COMPILER=\"{c_compiler_path}\""

    if cpp_compiler_path:
        cmd_generate_text += f" -D CMAKE_CXX_COMPILER=\"{cpp_compiler_path}\""

    cmd_build_text = f"cmake --build \"{build_path}\""

    subprocess.check_call(cmd_generate_text, shell=True)
    subprocess.check_call(cmd_build_text, shell=True)
