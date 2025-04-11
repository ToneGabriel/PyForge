from .generator import IGeneratorPart


_PROJECT_EXECUTABLE_CMAKE_VAR_NAME = "PROJECT_EXECUTABLE_NAME"
_PROJECT_STATIC_LIBRARY_CMAKE_VAR_NAME = "PROJECT_STATIC_LIBRARY_NAME"
_PROJECT_SHARED_LIBRARY_CMAKE_VAR_NAME = "PROJECT_SHARED_LIBRARY_NAME"


def _adapt_to_cmake_bool(value: bool) -> str:
    return "ON" if value else "OFF"


class HeaderGeneratorPart(IGeneratorPart):
    def __init__(
            self: object,
            cmake_minimum_required_version: str,
            project_name: str,
            project_version_major: int,
            project_version_minor: int,
            project_version_patch: str,
            c_language_standard: int,
            c_language_standard_required: bool,
            c_compiler_extensions_required: bool,
            cpp_language_standard: int,
            cpp_language_standard_required: bool,
            cpp_compiler_extensions_required: bool
    ):
        self._cmake_minimum_required_version = cmake_minimum_required_version
        self._project_name = project_name
        self._project_version_major = project_version_major
        self._project_version_minor = project_version_minor
        self._project_version_patch = project_version_patch
        self._c_language_standard = c_language_standard
        self._c_language_standard_required = c_language_standard_required
        self._c_compiler_extensions_required = c_compiler_extensions_required
        self._cpp_language_standard = cpp_language_standard
        self._cpp_language_standard_required = cpp_language_standard_required
        self._cpp_compiler_extensions_required = cpp_compiler_extensions_required

    def generate(self: object, file):
        self._write_cmake_minimum_required_version(file)
        self._write_project_specifications(file)
        self._write_language_specifications(file)
        self._write_destination_specifications(file)

    def _write_cmake_minimum_required_version(self: object, file) -> None:
        file.write( f"cmake_minimum_required(VERSION "
                    f"{self._cmake_minimum_required_version} "
                    f"FATAL_ERROR)\n"
                    )
        file.write( f"\n")

    def _write_project_specifications(self: object, file) -> None:
        file.write( f"project({self._project_name} "
                    f"VERSION {self._project_version_major}.{self._project_version_minor}.{self._project_version_patch} "
                    f"LANGUAGES C CXX)\n"
                    )
        file.write( f"\n")

    def _write_language_specifications(self: object, file) -> None:
        file.write( f"set(CMAKE_C_STANDARD {self._c_language_standard})\n"
                    f"set(CMAKE_C_STANDARD_REQUIRED {_adapt_to_cmake_bool(self._c_language_standard_required)})\n"
                    f"set(CMAKE_C_EXTENSIONS {_adapt_to_cmake_bool(self._c_compiler_extensions_required)})\n\n"

                    f"set(CMAKE_cpp_standard {self._cpp_language_standard})\n"
                    f"set(CMAKE_cpp_standard_REQUIRED {_adapt_to_cmake_bool(self._cpp_language_standard_required)})\n"
                    f"set(CMAKE_cpp_extensions {_adapt_to_cmake_bool(self._cpp_compiler_extensions_required)})\n"
                    )
        file.write( f"\n")

    def _write_destination_specifications(self: object, file) -> None:
        file.write( f"set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/bin)\n"
                    f"set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/lib)\n"
                    f"set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/lib)\n"
                    )
        file.write( f"\n")


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

    def generate(self: object, file):
        self._write_static_library_header(file)
        self._write_target_include_directories(file)
        self._write_target_sources(file)

    def _write_static_library_header(self: object, file) -> None:
        lib_name: str = self._project_name + "_static_lib"
        file.write(f"set({_PROJECT_STATIC_LIBRARY_CMAKE_VAR_NAME} \"{lib_name}\")\n"
                   f"add_library(${{{_PROJECT_STATIC_LIBRARY_CMAKE_VAR_NAME}}} STATIC)\n"
                   )
        file.write(f"\n")

    def _write_target_include_directories(self: object, file) -> None:
        pass

    def _write_target_sources(self: object, file) -> None:
        file.write(f"target_sources(${{{_PROJECT_STATIC_LIBRARY_CMAKE_VAR_NAME}}} PUBLIC\n")
        for source in self._source_files:
            file.write(f"{source}\n")
        file.write(f")\n")
        file.write(f"\n")


class SharedLibraryGeneratorPart(IGeneratorPart):
    def __init__(self: object):
        pass

    def generate(self: object, file):
        pass
