from .generator import Generator
from .generatorparts import HeaderGeneratorPart,\
                            LibraryGeneratorPart,\
                            ExecutableGeneratorPart,\
                            GoogleTestLibraryGeneratorPart,\
                            LinkerGeneratorPart


_CMAKE_MINIMUM_REQUIRED_VERSION = "3.22.1"

_STATIC = "STATIC"
_SHARED = "SHARED"

_PROJECT_STATIC_LIBRARY_PREFIX = "slib_"
_PROJECT_SHARED_LIBRARY_PREFIX = "dlib_"
_TEST_LIBRARY_PREFIX = "tlib_"

_PROJECT_EXECUTABLE_PREFIX = ""
_TEST_EXECUTABLE_PREFIX = "test_"

_PROJECT_STATIC_LIBRARY_CMAKE_VAR_NAME = "PROJECT_STATIC_LIBRARY_NAME"
_PROJECT_SHARED_LIBRARY_CMAKE_VAR_NAME = "PROJECT_SHARED_LIBRARY_NAME"
_PROJECT_EXECUTABLE_CMAKE_VAR_NAME = "PROJECT_EXECUTABLE_NAME"
_TEST_STATIC_LIBRARY_CMAKE_VAR_NAME = "TEST_STATIC_LIBRARY_NAME"
_TEST_EXECUTABLE_CMAKE_VAR_NAME = "TEST_EXECUTABLE_NAME"

_GTEST_STATIC_LIBRARY_CMAKE_VAR_NAME = "GTEST_STATIC_LIBRARY_NAME"
_GMOCK_STATIC_LIBRARY_CMAKE_VAR_NAME = "GMOCK_STATIC_LIBRARY_NAME"


class GeneratorBuilder:
    def __init__(
            self: object,
            project_name: str,
            project_version: str,
            c_language_standard: int,
            c_language_standard_required: bool,
            c_compiler_extensions_required: bool,
            cpp_language_standard: int,
            cpp_language_standard_required: bool,
            cpp_compiler_extensions_required: bool,
            cmake_compile_definitions: list,
            include_directories: list,
            source_files: list,
            executable_file: str,
            test_source_files: str,
            test_executable_file: str
    ):
        self._project_name = project_name
        self._project_version = project_version
        self._c_language_standard = c_language_standard
        self._c_language_standard_required = c_language_standard_required
        self._c_compiler_extensions_required = c_compiler_extensions_required
        self._cpp_language_standard = cpp_language_standard
        self._cpp_language_standard_required = cpp_language_standard_required
        self._cpp_compiler_extensions_required = cpp_compiler_extensions_required
        self._cmake_compile_definitions = cmake_compile_definitions
        self._include_directories = include_directories
        self._source_files = source_files
        self._executable_file = executable_file
        self._test_source_files = test_source_files
        self._test_executable_file = test_executable_file
        self.reset_generator()

    @property
    def generator(self: object) -> Generator:
        return self._generator

    def reset_generator(self: object) -> None:
        self._generator = Generator()

    def add_header(self: object) -> None:
        self._generator.add_part(HeaderGeneratorPart(
                                    _CMAKE_MINIMUM_REQUIRED_VERSION,
                                    self._project_name,
                                    self._project_version,
                                    self._c_language_standard,
                                    self._c_language_standard_required,
                                    self._c_compiler_extensions_required,
                                    self._cpp_language_standard,
                                    self._cpp_language_standard_required,
                                    self._cpp_compiler_extensions_required
                                    )
                                )

    def add_static_library_project(self: object) -> None:
        self._generator.add_part(LibraryGeneratorPart(
                                    _PROJECT_STATIC_LIBRARY_CMAKE_VAR_NAME,
                                    _STATIC,
                                    _PROJECT_STATIC_LIBRARY_PREFIX,
                                    self._project_name,
                                    self._include_directories,
                                    self._source_files
                                    )
                                )

    def add_static_library_test(self: object) -> None:
        self._generator.add_part(LibraryGeneratorPart(
                                    _TEST_STATIC_LIBRARY_CMAKE_VAR_NAME,
                                    _STATIC,
                                    _TEST_LIBRARY_PREFIX,
                                    self._project_name,
                                    self._include_directories,
                                    self._test_source_files
                                    )
                                )

    def add_shared_library_project(self: object) -> None:
        self._generator.add_part(LibraryGeneratorPart(
                                    _PROJECT_SHARED_LIBRARY_CMAKE_VAR_NAME,
                                    _SHARED,
                                    _PROJECT_SHARED_LIBRARY_PREFIX,
                                    self._project_name,
                                    self._include_directories,
                                    self._source_files
                                    )
                                )

    def add_googletest_library(self: object) -> None:
        self._generator.add_part(GoogleTestLibraryGeneratorPart(
                                    _GTEST_STATIC_LIBRARY_CMAKE_VAR_NAME,
                                    _GMOCK_STATIC_LIBRARY_CMAKE_VAR_NAME
                                    )
                                )

    def add_executable_project(self: object) -> None:
        self._generator.add_part(ExecutableGeneratorPart(
                                    _PROJECT_EXECUTABLE_CMAKE_VAR_NAME,
                                    _PROJECT_EXECUTABLE_PREFIX,
                                    self._project_name,
                                    self._executable_file
                                    )
                                )

    def add_executable_test(self: object) -> None:
        self._generator.add_part(ExecutableGeneratorPart(
                                    _TEST_EXECUTABLE_CMAKE_VAR_NAME,
                                    _TEST_EXECUTABLE_PREFIX,
                                    self._project_name,
                                    self._test_executable_file
                                    )
                                )

    def add_target_linker_project(self: object) -> None:
        self._generator.add_part(LinkerGeneratorPart(
                                    _PROJECT_EXECUTABLE_CMAKE_VAR_NAME,
                                    _PROJECT_STATIC_LIBRARY_CMAKE_VAR_NAME
                                    )
                                )
    
    def add_target_linker_test(self: object) -> None:
        self._generator.add_part(LinkerGeneratorPart(
                                    _TEST_EXECUTABLE_CMAKE_VAR_NAME,
                                    _PROJECT_STATIC_LIBRARY_CMAKE_VAR_NAME,
                                    _TEST_STATIC_LIBRARY_CMAKE_VAR_NAME,
                                    _GTEST_STATIC_LIBRARY_CMAKE_VAR_NAME,
                                    _GMOCK_STATIC_LIBRARY_CMAKE_VAR_NAME
                                    )
                                )

    def add_target_linker_template_test(self: object) -> None:
        self._generator.add_part(LinkerGeneratorPart(
                                    _TEST_EXECUTABLE_CMAKE_VAR_NAME,
                                    _TEST_STATIC_LIBRARY_CMAKE_VAR_NAME,
                                    _GTEST_STATIC_LIBRARY_CMAKE_VAR_NAME,
                                    _GMOCK_STATIC_LIBRARY_CMAKE_VAR_NAME
                                    )
                                )