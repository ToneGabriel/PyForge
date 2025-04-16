import os
import shutil
import subprocess

from .generatorbuilder import GeneratorBuilder


def _get_include_dirs(include_path: str) -> list[str]:
    ret: list[str] = []

    for dirpath, _, _ in os.walk(include_path):
        relative_path = os.path.relpath(dirpath, start=os.path.dirname(include_path))
        ret.append(relative_path.replace(os.path.sep, '/'))

    return ret


def _get_sources(source_path: str, ignore: set[str]={}) -> list[str]:
    ret: list[str] = []

    for dirpath, _, filenames in os.walk(source_path):
        for filename in filenames:
            if filename.endswith(('.c', '.cpp')) and filename not in ignore:
                relative_path = os.path.relpath(os.path.join(dirpath, filename),
                                                start=os.path.dirname(source_path))
                ret.append(relative_path.replace(os.path.sep, '/'))

    return ret


def _get_executable(source_path: str) -> str:
    main_files = {"main.c", "main.cpp"}

    for dirpath, _, filenames in os.walk(source_path):
        for filename in filenames:
            if filename in main_files:
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

        test_source_files = _get_sources(test_path, ignore={"main.cpp"})
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

        # Test - googletest library from GIT, test library and executable
        builder.add_googletest_library()
        builder.add_static_library_test()
        builder.add_executable_test()

        match project_build_type:
            case "app":
                builder.add_static_library_project()
                builder.add_executable_project()
                builder.add_target_linker_project()
                builder.add_target_linker_test()
            case "lib":
                builder.add_static_library_project()
                builder.add_target_linker_test()
            case "dll":
                builder.add_shared_library_project()
                builder.add_static_library_project()
                builder.add_target_linker_test()
            case "tmp":
                builder.add_target_linker_template_test()
            case _:
                raise None

        with open(cmakelists_path, "w") as cmakelists_root_open_file:
            builder.generator.run(cmakelists_root_open_file)


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
            shutil.rmtree(build_path)

    cmd_generate_text = f"cmake -S \"{project_root_path}\" -G \"{cmake_generator}\" -B \"{build_path}\""

    if c_compiler_path:
        cmd_generate_text += f" -D CMAKE_C_COMPILER=\"{c_compiler_path}\""

    if cpp_compiler_path:
        cmd_generate_text += f" -D CMAKE_CXX_COMPILER=\"{cpp_compiler_path}\""

    cmd_build_text = f"cmake --build \"{build_path}\""

    subprocess.check_call(cmd_generate_text, shell=True)
    subprocess.check_call(cmd_build_text, shell=True)
