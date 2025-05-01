from enum import Enum
from ._generator_base import IGeneratorPart


class CMakeLibraryType(Enum):
    STATIC = "STATIC"
    SHARED = "SHARED"
    INTERFACE = "INTERFACE"


class CMakeTargetVisibility(Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    INTERFACE = "INTERFACE"


def _adapt_to_cmake_bool(value: bool) -> str:
    return "ON" if value else "OFF"


# ==========================================================================================================================
# ==========================================================================================================================


class HeaderGeneratorPart(IGeneratorPart):
    def __init__(
            self: object,
            cmake_minimum_required_version: str,
            project_name: str,
            project_version: str,
            c_language_standard: int,
            c_language_standard_required: bool,
            c_compiler_extensions_required: bool,
            cpp_language_standard: int,
            cpp_language_standard_required: bool,
            cpp_compiler_extensions_required: bool
    ):
        self._cmake_minimum_required_version = cmake_minimum_required_version
        self._project_name = project_name
        self._project_version = project_version
        self._c_language_standard = c_language_standard
        self._c_language_standard_required = c_language_standard_required
        self._c_compiler_extensions_required = c_compiler_extensions_required
        self._cpp_language_standard = cpp_language_standard
        self._cpp_language_standard_required = cpp_language_standard_required
        self._cpp_compiler_extensions_required = cpp_compiler_extensions_required

    def run(self: object, file) -> None:
        self._write_cmake_minimum_required_version(file)
        self._write_project_specifications(file)
        self._write_language_specifications(file)
        self._write_destination_specifications(file)

    def _write_cmake_minimum_required_version(self: object, file) -> None:
        file.write( f"cmake_minimum_required(VERSION {self._cmake_minimum_required_version} FATAL_ERROR)\n\n")

    def _write_project_specifications(self: object, file) -> None:
        file.write( f"project({self._project_name} "
                    f"VERSION {self._project_version} "
                    f"LANGUAGES C CXX)\n\n"
                    )

    def _write_language_specifications(self: object, file) -> None:
        file.write( f"set(CMAKE_C_STANDARD {self._c_language_standard})\n"
                    f"set(CMAKE_C_STANDARD_REQUIRED {_adapt_to_cmake_bool(self._c_language_standard_required)})\n"
                    f"set(CMAKE_C_EXTENSIONS {_adapt_to_cmake_bool(self._c_compiler_extensions_required)})\n\n"

                    f"set(CMAKE_CXX_STANDARD {self._cpp_language_standard})\n"
                    f"set(CMAKE_CXX_STANDARD_REQUIRED {_adapt_to_cmake_bool(self._cpp_language_standard_required)})\n"
                    f"set(CMAKE_CXX_EXTENSIONS {_adapt_to_cmake_bool(self._cpp_compiler_extensions_required)})\n\n"
                    )

    def _write_destination_specifications(self: object, file) -> None:
        file.write( f"set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/bin)\n"
                    f"set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/lib)\n"
                    f"set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/lib)\n\n"
                    )


# ==========================================================================================================================
# ==========================================================================================================================


class GoogleTestLibraryGeneratorPart(IGeneratorPart):
    def __init__(
            self: object,
            git_tag: str
    ):
        self._git_tag = git_tag

    @property
    def gtest_cmake_variable_name(self: object) -> str:
        return "GTEST_CMAKE_LIB_NAME"

    @property
    def gmock_cmake_variable_name(self: object) -> str:
        return "GMOCK_CMAKE_LIB_NAME"

    def run(self: object, file) -> None:
        self._write_gtest_header(file)
        self._write_gtest_gmock_cmake_variables(file)

    def _write_gtest_header(self: object, file) -> None:
        file.write( f"include(FetchContent)\n")
        file.write( f"FetchContent_Declare(\n"
                    f"googletest\n"
                    f"GIT_REPOSITORY https://github.com/google/googletest.git\n"
                    f"GIT_TAG {self._git_tag}\n"
                    )
        file.write( f")\n\n")

        file.write( f"set(INSTALL_GTEST OFF CACHE BOOL \"Disable installation of googletest\" FORCE)\n\n"
                    f"FetchContent_MakeAvailable(googletest)\n\n"
                    )

    def _write_gtest_gmock_cmake_variables(self: object, file) -> None:
        file.write( f"set({self.gtest_cmake_variable_name} gtest)\n"
                    f"set({self.gmock_cmake_variable_name} gmock)\n\n"
                    )


# ==========================================================================================================================
# ==========================================================================================================================


class LibraryGeneratorPart(IGeneratorPart):
    def __init__(
            self: object,
            name: str,
            type: CMakeLibraryType,
    ):
        self._name = name
        self._type = type

    @property
    def cmake_variable_name(self: object) -> str:
        return self._name.upper() + "_LIB_NAME"

    def run(self: object, file) -> None:
        self._write_library_header(file)

    def _write_library_header(self: object, file) -> None:
        file.write( f"set({self.cmake_variable_name} {self._name})\n"
                    f"add_library(${{{self.cmake_variable_name}}} {self._type.value})\n"
                    f"set_target_properties(${{{self.cmake_variable_name}}} PROPERTIES PREFIX \"\" IMPORT_PREFIX \"\")\n\n")


# ==========================================================================================================================
# ==========================================================================================================================


class ExecutableGeneratorPart(IGeneratorPart):
    def __init__(
            self: object,
            name: str,
            executable_file: str
    ):
        self._name = name
        self._executable_file = executable_file

    @property
    def cmake_variable_name(self: object) -> str:
        return self._name.upper() + "_EXE_NAME"

    def run(self: object, file) -> None:
        self._write_executable_header(file)

    def _write_executable_header(self: object, file) -> None:
        file.write( f"set({self.cmake_variable_name} {self._name})\n"
                    f"add_executable(${{{self.cmake_variable_name}}} ${{CMAKE_SOURCE_DIR}}/{self._executable_file})\n\n"
                    )


# ==========================================================================================================================
# ==========================================================================================================================


class IncludeGeneratorPart(IGeneratorPart):
    def __init__(self: object,
                 cmake_target_var_name: str,
                 visibility: CMakeTargetVisibility,
                 include_directories: list[str]
    ):
        self._cmake_target_var_name = cmake_target_var_name
        self._visibility = visibility
        self._include_directories = include_directories

    def run(self: object, file):
        self._write_target_include_directories(file)

    def _write_target_include_directories(self: object, file) -> None:
        if not self._include_directories:
            return

        file.write(f"target_include_directories(${{{self._cmake_target_var_name}}} {self._visibility.value}\n")
        for dir in self._include_directories:
            file.write(f"${{CMAKE_SOURCE_DIR}}/{dir}\n")
        file.write(f")\n\n")


# ==========================================================================================================================
# ==========================================================================================================================


class SourceGeneratorPart(IGeneratorPart):
    def __init__(self: object,
                 cmake_target_var_name: str,
                 visibility: CMakeTargetVisibility,
                 source_files: list[str]
    ):
        self._cmake_target_var_name = cmake_target_var_name
        self._visibility = visibility
        self._source_files = source_files

    def run(self: object, file):
        self._write_target_sources(file)

    def _write_target_sources(self: object, file) -> None:
        if not self._source_files:
            return

        file.write(f"target_sources(${{{self._cmake_target_var_name}}} {self._visibility.value}\n")
        for source in self._source_files:
            file.write(f"${{CMAKE_SOURCE_DIR}}/{source}\n")
        file.write(f")\n\n")


# ==========================================================================================================================
# ==========================================================================================================================


class DefinitionGeneratorPart(IGeneratorPart):
    def __init__(self: object,
                 cmake_target_var_name: str,
                 visibility: CMakeTargetVisibility,
                 compile_definitions: list[tuple[str, str]]
    ):
        self._cmake_target_var_name = cmake_target_var_name
        self._visibility = visibility
        self._compile_definitions = compile_definitions

    def run(self: object, file):
        self._write_target_compile_definitions(file)

    def _write_target_compile_definitions(self: object, file):
        if not self._compile_definitions:
            return

        file.write(f"target_compile_definitions(${{{self._cmake_target_var_name}}} {self._visibility.value}\n")
        for macro, value in self._compile_definitions:
            if not value:
                file.write(f"{macro}\n")
            else:
                file.write(f"{macro}={value}\n")
        file.write(f")\n\n")


# ==========================================================================================================================
# ==========================================================================================================================


class LinkerGeneratorPart(IGeneratorPart):
    def __init__(
            self: object,
            cmake_target_var_name: str,
            visibility: CMakeTargetVisibility,
            *cmake_lib_var_names
    ):
        self._cmake_target_var_name = cmake_target_var_name
        self._visibility = visibility
        self._cmake_lib_var_names = cmake_lib_var_names

    def run(self: object, file) -> None:
        self._write_target_link_libraries(file)

    def _write_target_link_libraries(self: object, file) -> None:
        file.write(f"target_link_libraries(${{{self._cmake_target_var_name}}} {self._visibility.value}\n")
        for lib in self._cmake_lib_var_names:
            file.write(f"${{{lib}}}\n")
        file.write(f")\n\n")
