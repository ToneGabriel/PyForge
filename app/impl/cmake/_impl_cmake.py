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

        # declare target
        cmake_target_var_name = None

        # create target based on product type
        match project_product_type:
            case ProductType.EXE:
                cmake_target_var_name = builder.add_executable(project_name, executable_file)

            case ProductType.LIB:
                cmake_target_var_name = builder.add_library(project_name, CMakeLibraryType.STATIC)

            case ProductType.DLL:
                cmake_target_var_name = builder.add_library(project_name, CMakeLibraryType.SHARED)

            case _:
                raise RuntimeError(f"Project product type not implemented: {project_product_type}")

        # add include, source and compile definitions to target
        builder.add_target_include_directories(cmake_target_var_name, CMakeTargetVisibility.PUBLIC, include_directories)
        builder.add_target_sources(cmake_target_var_name, CMakeTargetVisibility.PRIVATE, source_files)
        builder.add_target_compile_definitions(cmake_target_var_name, CMakeTargetVisibility.PRIVATE, cmake_compile_definitions)

        # link imported libraries
        # TODO

        # write ALL info in CMakelists.txt
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
