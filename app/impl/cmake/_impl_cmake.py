from enum import Enum, auto

from . import devfiles
from .cmd import    CMDBuilder,\
                    BuildType
from .generator import  GeneratorBuilder,\
                        CMakeLibraryType,\
                        CMakeTargetVisibility


__all__ = ["ProductType",
           "BuildType",
           "generate",
           "build"
           ]


_CMAKE_MINIMUM_REQUIRED_VERSION = "3.22.1"


class ProductType(Enum):
    APP = auto()
    LIB = auto()
    DLL = auto()
    TMP = auto()


def generate(
        project_root_path: str,
        project_name: str,
        project_product_type: ProductType,
        project_version: str,
        c_language_enabled: bool,
        c_language_standard: int,
        c_language_standard_required: bool,
        c_compiler_extensions_required: bool,
        unity_framework_enabled: bool,
        cpp_language_enabled: bool,
        cpp_language_standard: int,
        cpp_language_standard_required: bool,
        cpp_compiler_extensions_required: bool,
        googletest_framework_enabled: bool,
        cmake_compile_definitions: list[tuple[str, str]]
) -> None:
        cmakelists_path = devfiles.get_cmakelists_file_path(project_root_path)

        include_directories = devfiles.get_project_include_dirs(project_root_path)
        source_files = devfiles.get_project_sources(project_root_path)
        executable_file = devfiles.get_project_executable(project_root_path)

        test_source_files = devfiles.get_test_sources(project_root_path)
        test_executable_file = devfiles.get_test_executable(project_root_path)

        builder = GeneratorBuilder()

        # Header is the same for all cases
        builder.add_header(_CMAKE_MINIMUM_REQUIRED_VERSION,
                           project_name,
                           project_version,
                           c_language_enabled,
                           c_language_standard,
                           c_language_standard_required,
                           c_compiler_extensions_required,
                           cpp_language_enabled,
                           cpp_language_standard,
                           cpp_language_standard_required,
                           cpp_compiler_extensions_required
                           )

        match project_product_type:
            case ProductType.APP:
                # Standalone application (executable)
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
                # Static library
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
                # Dynamic linked library
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

            case ProductType.TMP:
                # Template library
                # Only headers matter and they must be included in some other target
                pass
            case _:
                raise RuntimeError(f"Invalid project build type: {project_product_type}.")

        if unity_framework_enabled:
            # Unity
            unity_lib_name = builder.add_unity_library()

            # Test executable
            unity_executable_name = builder.add_executable("utest_" + project_name,
                                                           test_executable_file
                                                           )
            
            builder.add_target_linker(  unity_executable_name,
                                        CMakeTargetVisibility.PRIVATE,
                                        unity_lib_name
                                        )

            builder.add_target_compile_definitions( unity_executable_name,
                                                    CMakeTargetVisibility.PRIVATE,
                                                    cmake_compile_definitions
                                                    )

            builder.add_target_include_directories( unity_executable_name,
                                                    CMakeTargetVisibility.PRIVATE,
                                                    include_directories
                                                    )

            builder.add_target_sources( unity_executable_name,
                                        CMakeTargetVisibility.PRIVATE,
                                        source_files + test_source_files
                                        )

        if googletest_framework_enabled:
            # Googletest (gtest and gmock)
            gtest_lib_name, gmock_lib_name = builder.add_googletest_library()

            # Test executable
            gtest_executable_name = builder.add_executable("gtest_" + project_name,
                                                            test_executable_file
                                                            )

            builder.add_target_linker(  gtest_executable_name,
                                        CMakeTargetVisibility.PRIVATE,
                                        gtest_lib_name,
                                        gmock_lib_name
                                        )

            builder.add_target_compile_definitions( gtest_executable_name,
                                                    CMakeTargetVisibility.PRIVATE,
                                                    cmake_compile_definitions
                                                    )

            builder.add_target_include_directories( gtest_executable_name,
                                                    CMakeTargetVisibility.PRIVATE,
                                                    include_directories
                                                    )

            builder.add_target_sources( gtest_executable_name,
                                        CMakeTargetVisibility.PRIVATE,
                                        source_files + test_source_files
                                        )

        with open(cmakelists_path, "w") as cmakelists_root_open_file:
            builder.generator_product.run(cmakelists_root_open_file)


def build(
        project_root_path: str,
        project_build_type: BuildType,
        c_compiler_path: str,
        cpp_compiler_path: str,
        cmake_bin_path: str,
        buildsystem_bin_path: str,
        clean: bool=True
) -> None:
    build_dir_path = devfiles.get_build_dir_path(project_root_path)

    builder = CMDBuilder(cmake_bin_path, buildsystem_bin_path)

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
