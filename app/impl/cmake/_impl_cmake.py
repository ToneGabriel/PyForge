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


def _get_next_library_name() -> str:
    """
    Generate sequential `import_lib` names
    """

    if not hasattr(_get_next_library_name, "index"):
        _get_next_library_name.index = 0

    _get_next_library_name.index += 1
    return f"import_lib{_get_next_library_name.index}"


class ProductType(Enum):
    EXE = auto()    # Standalone application (executable)
    LIB = auto()    # Static library
    DLL = auto()    # Dynamic linked library


def generate(
        project_root_path: str,
        project_ignored_dir_names: list[str],
        project_imported_static_libs: list[tuple[str, str]],
        project_imported_shared_libs: list[tuple[str, str, str]],
        project_name: str,
        project_product_type: ProductType,
        project_version: str,
        project_language: Language,
        language_standard: int,
        language_standard_required: bool,
        compiler_extensions_required: bool,
        cmake_compile_definitions: list[tuple[str, str]]
) -> None:
        """
        Generate the CMakelists.txt file
        """

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

        # declare target and import libs
        cmake_target_var_name: str = ""
        cmake_import_lib_names: list[str] = []

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

        # create static imported libraries
        for imported_location, imported_include_dir in project_imported_static_libs:
            temp_cmake_target_lib_name = builder.add_imported_library(_get_next_library_name(), CMakeLibraryType.STATIC, imported_location, imported_location, imported_include_dir)
            cmake_import_lib_names.append(temp_cmake_target_lib_name)

        # create shared imported libraries
        for imported_location, imported_impl_location, imported_include_dir in project_imported_shared_libs:
            temp_cmake_target_lib_name = builder.add_imported_library(_get_next_library_name(), CMakeLibraryType.SHARED, imported_location, imported_impl_location, imported_include_dir)
            cmake_import_lib_names.append(temp_cmake_target_lib_name)

        # link imported libraries
        builder.add_target_linker(cmake_target_var_name, CMakeTargetVisibility.PRIVATE, *cmake_import_lib_names)

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
        clean: bool=False,
        install: bool=False
) -> None:
    """
    Run commands in console for cmake build and install
    """

    build_dir_path = devfiles.get_build_dir_path(project_root_path)
    install_dir_path = devfiles.get_install_dir_path(project_root_path)

    builder = CMDBuilder(cmake_bin_path, ninja_bin_path)

    if clean:
        builder.add_rmdir_part(build_dir_path)

    builder.add_cmake_generate_part(project_root_path,
                                    project_build_type,
                                    build_dir_path,
                                    install_dir_path,
                                    c_compiler_path,
                                    cpp_compiler_path
                                    )

    builder.add_cmake_build_part(build_dir_path)

    if install:
        builder.add_rmdir_part(install_dir_path)    # always clean
        builder.add_cmake_install_part(build_dir_path)

    builder.cmd_product.run()
