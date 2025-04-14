from .generator import IGeneratorPart


_CMAKE_MINIMUM_REQUIRED_VERSION = "3.22.1"
_TEST_EXECUTABLE_CMAKE_VAR_NAME = "TEST_EXECUTABLE_NAME"
_PROJECT_EXECUTABLE_CMAKE_VAR_NAME = "PROJECT_EXECUTABLE_NAME"
_PROJECT_STATIC_LIBRARY_CMAKE_VAR_NAME = "PROJECT_STATIC_LIBRARY_NAME"
_PROJECT_SHARED_LIBRARY_CMAKE_VAR_NAME = "PROJECT_SHARED_LIBRARY_NAME"


def _adapt_to_cmake_bool(value: bool) -> str:
    return "ON" if value else "OFF"


# ==========================================================================================================================
# ==========================================================================================================================


class HeaderGeneratorPart(IGeneratorPart):
    def __init__(
            self: object,
            project_name: str,
            project_version: str,
            c_language_standard: int,
            c_language_standard_required: bool,
            c_compiler_extensions_required: bool,
            cpp_language_standard: int,
            cpp_language_standard_required: bool,
            cpp_compiler_extensions_required: bool
    ):
        self._project_name = project_name
        self._project_version = project_version
        self._c_language_standard = c_language_standard
        self._c_language_standard_required = c_language_standard_required
        self._c_compiler_extensions_required = c_compiler_extensions_required
        self._cpp_language_standard = cpp_language_standard
        self._cpp_language_standard_required = cpp_language_standard_required
        self._cpp_compiler_extensions_required = cpp_compiler_extensions_required

    def run(self: object, file):
        self._write_cmake_minimum_required_version(file)
        self._write_project_specifications(file)
        self._write_language_specifications(file)
        self._write_destination_specifications(file)

    def _write_cmake_minimum_required_version(self: object, file) -> None:
        file.write( f"cmake_minimum_required(VERSION {_CMAKE_MINIMUM_REQUIRED_VERSION} FATAL_ERROR)\n\n")

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


class StaticLibraryGeneratorPart(IGeneratorPart):
    def __init__(
            self: object,
            project_name: str,
            include_directories: list[str],
            source_files: list[str]
    ):
        self._project_name = project_name
        self._include_directories = include_directories
        self._source_files = source_files

    def run(self: object, file):
        self._write_static_library_header(file)
        self._write_target_include_directories(file)
        self._write_target_sources(file)

    def _write_static_library_header(self: object, file) -> None:
        lib_name: str = self._project_name + "_static_lib"
        file.write( f"set({_PROJECT_STATIC_LIBRARY_CMAKE_VAR_NAME} \"{lib_name}\")\n"
                    f"add_library(${{{_PROJECT_STATIC_LIBRARY_CMAKE_VAR_NAME}}} STATIC)\n\n"
                    )

    def _write_target_include_directories(self: object, file) -> None:
        pass

    def _write_target_sources(self: object, file) -> None:
        file.write(f"target_sources(${{{_PROJECT_STATIC_LIBRARY_CMAKE_VAR_NAME}}} PUBLIC\n")
        for source in self._source_files:
            file.write(f"{source}\n")
        file.write(f")\n\n")


# ==========================================================================================================================
# ==========================================================================================================================


class SharedLibraryGeneratorPart(IGeneratorPart):
    def __init__(self: object):
        pass

    def run(self: object, file):
        pass
