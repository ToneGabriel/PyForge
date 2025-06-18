from enum import Enum, auto

from . import devfiles
from .cmd import *
from .generator import *


__all__ = ["ProductType",
           "BuildType",
           "Language",
           "generate",
           "build"
           ]


_CMAKE_MINIMUM_REQUIRED_VERSION = "3.22.1"


class ProductType(Enum):
    EXE = auto()    # Standalone application (executable)
    LIB = auto()    # Static library
    DLL = auto()    # Dynamic linked library
    TST = auto()    # Test executable (with googletest or unity)


def generate(
        project_root_path: str,
        project_ignored_dir_names: list[str],
        project_name: str,
        project_product_type: ProductType,
        project_version: str,
        project_language: Language,
        language_standard: int,
        language_standard_required: bool,
        compiler_extensions_required: bool,
        cmake_compile_definitions: list[tuple[str, str]]
) -> None:
        cmakelists_path = devfiles.get_cmakelists_file_path(project_root_path)
        include_directories, source_files, executable_file = devfiles.get_project_files_and_dirs(project_root_path, project_ignored_dir_names)

        builder = GeneratorBuilder()

        # Header is the same for all cases
        builder.add_header(_CMAKE_MINIMUM_REQUIRED_VERSION,
                           project_name,
                           project_version,
                           project_language,
                           language_standard,
                           language_standard_required,
                           compiler_extensions_required
                           )

        match project_product_type:
            case ProductType.EXE:
                app_executable_cmake_variable_name = builder.add_executable(project_name,
                                                                            executable_file
                                                                            )

                builder.add_target_include_directories(app_executable_cmake_variable_name,
                                                       CMakeTargetVisibility.PRIVATE,
                                                       include_directories
                                                       )

                builder.add_target_sources(app_executable_cmake_variable_name,
                                           CMakeTargetVisibility.PRIVATE,
                                           source_files
                                           )

                builder.add_target_compile_definitions(app_executable_cmake_variable_name,
                                                       CMakeTargetVisibility.PRIVATE,
                                                       cmake_compile_definitions
                                                       )

            case ProductType.LIB:
                static_lib_cmake_variable_name = builder.add_library(project_name,
                                                                     CMakeLibraryType.STATIC
                                                                     )

                builder.add_target_include_directories(static_lib_cmake_variable_name,
                                                       CMakeTargetVisibility.PUBLIC,
                                                       include_directories
                                                       )

                builder.add_target_sources(static_lib_cmake_variable_name,
                                           CMakeTargetVisibility.PRIVATE,
                                           source_files
                                           )

                builder.add_target_compile_definitions(static_lib_cmake_variable_name,
                                                       CMakeTargetVisibility.PRIVATE,
                                                       cmake_compile_definitions
                                                       )

            case ProductType.DLL:
                shared_lib_cmake_variable_name = builder.add_library(project_name,
                                                                     CMakeLibraryType.SHARED
                                                                     )

                builder.add_target_include_directories(shared_lib_cmake_variable_name,
                                                       CMakeTargetVisibility.PUBLIC,
                                                       include_directories
                                                       )

                builder.add_target_sources(shared_lib_cmake_variable_name,
                                           CMakeTargetVisibility.PRIVATE,
                                           source_files
                                           )

                builder.add_target_compile_definitions(shared_lib_cmake_variable_name,
                                                       CMakeTargetVisibility.PRIVATE,
                                                       cmake_compile_definitions
                                                       )

            case ProductType.TST:
                test_executable_cmake_variable_name = builder.add_executable(project_name,
                                                                             executable_file
                                                                             )

                builder.add_target_include_directories(test_executable_cmake_variable_name,
                                                       CMakeTargetVisibility.PRIVATE,
                                                       include_directories
                                                       )

                builder.add_target_sources(test_executable_cmake_variable_name,
                                           CMakeTargetVisibility.PRIVATE,
                                           source_files
                                           )

                builder.add_target_compile_definitions(test_executable_cmake_variable_name,
                                                       CMakeTargetVisibility.PRIVATE,
                                                       cmake_compile_definitions
                                                       )

                if project_language == Language.CPP:
                    gtest_lib_name, gmock_lib_name = builder.add_googletest_library()
                    builder.add_target_linker(test_executable_cmake_variable_name,
                                              CMakeTargetVisibility.PRIVATE,
                                              gtest_lib_name,
                                              gmock_lib_name
                                              )
                else:
                    unity_lib_name = builder.add_unity_library()
                    builder.add_target_linker(test_executable_cmake_variable_name,
                                              CMakeTargetVisibility.PRIVATE,
                                              unity_lib_name
                                              )

            case _:
                raise RuntimeError(f"Project product type not implemented: {project_product_type}")

        with open(cmakelists_path, "w") as cmakelists_root_open_file:
            builder.generator_product.run(cmakelists_root_open_file)


def build(
        project_root_path: str,
        project_build_type: BuildType,
        c_compiler_path: str,
        cpp_compiler_path: str,
        cmake_bin_path: str,
        ninja_bin_path: str,
        clean: bool=True
) -> None:
    build_dir_path = devfiles.get_build_dir_path(project_root_path)

    builder = CMDBuilder(cmake_bin_path, ninja_bin_path)

    if clean:
        builder.add_cmake_build_clear_part(build_dir_path)

    builder.add_cmake_generate_part(project_root_path,
                                    project_build_type,
                                    build_dir_path,
                                    c_compiler_path,
                                    cpp_compiler_path
                                    )

    builder.add_cmake_build_part(build_dir_path)

    builder.cmd_product.run()
