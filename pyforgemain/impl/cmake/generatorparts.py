from .generator import IGeneratorPart


def _adapt_to_cmake_bool(value: bool) -> str:
    return "ON" if value else "OFF"


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
            gtest_cmake_var_name: str,
            gmock_cmake_var_name: str,
            static_lib_cmake_var_name: str
    ):
        self._gtest_cmake_var_name = gtest_cmake_var_name
        self._gmock_cmake_var_name = gmock_cmake_var_name
        self._static_lib_cmake_var_name = static_lib_cmake_var_name

    def run(self: object, file) -> None:
        self._write_gtest_header(file)
        self._write_gtest_gmock_cmake_variables(file)
        self._write_include_directories_to_static_lib(file)

    def _write_gtest_header(self: object, file) -> None:
        file.write( f"include(FetchContent)\n")
        file.write( f"FetchContent_Declare(\n"
                    f"googletest\n"
                    f"GIT_REPOSITORY https://github.com/google/googletest.git\n"
                    f"GIT_TAG main\n"
                    )
        file.write(f")\n\n")

        file.write( f"set(INSTALL_GTEST OFF CACHE BOOL \"Disable installation of googletest\" FORCE)\n\n"
                    f"FetchContent_MakeAvailable(googletest)\n\n"
                    )

    def _write_gtest_gmock_cmake_variables(self: object, file) -> None:
        file.write( f"set({self._gtest_cmake_var_name} gtest)\n"
                    f"set({self._gmock_cmake_var_name} gmock)\n\n"
                    )

    def _write_include_directories_to_static_lib(self: object, file) -> None:
        file.write(f"target_include_directories(${{{self._static_lib_cmake_var_name}}} PUBLIC\n"
                   f"${{gtest_SOURCE_DIR}}/include\n"
                   f"${{gmock_SOURCE_DIR}}/include\n"
                   )
        file.write(f")\n\n")


# ==========================================================================================================================
# ==========================================================================================================================


class LibraryGeneratorPart(IGeneratorPart):
    def __init__(
            self: object,
            cmake_var_name: str,
            type_flag: str,
            prefix: str,
            project_name: str,
            include_directories: list[str],
            source_files: list[str],
            compile_definitions: list[tuple[str, str]]
    ):
        self._cmake_var_name = cmake_var_name
        self._type_flag = type_flag
        self._prefix = prefix
        self._project_name = project_name
        self._include_directories = include_directories
        self._source_files = source_files
        self._compile_definitions = compile_definitions

    def run(self: object, file) -> None:
        self._write_static_library_header(file)
        self._write_compile_definitions(file)
        self._write_target_include_directories(file)
        self._write_target_sources(file)

    def _write_static_library_header(self: object, file) -> None:
        lib_name = self._prefix + self._project_name
        file.write( f"set({self._cmake_var_name} \"{lib_name}\")\n"
                    f"add_library(${{{self._cmake_var_name}}} {self._type_flag})\n"
                    f"set_target_properties(${{{self._cmake_var_name}}} PROPERTIES PREFIX \"\" IMPORT_PREFIX \"\")\n\n")

    def _write_target_include_directories(self: object, file) -> None:
        file.write(f"target_include_directories(${{{self._cmake_var_name}}} PUBLIC\n")
        for dir in self._include_directories:
            file.write(f"${{CMAKE_SOURCE_DIR}}/{dir}\n")
        file.write(f")\n\n")

    def _write_target_sources(self: object, file) -> None:
        file.write(f"target_sources(${{{self._cmake_var_name}}} PUBLIC\n")
        for source in self._source_files:
            file.write(f"${{CMAKE_SOURCE_DIR}}/{source}\n")
        file.write(f")\n\n")

    def _write_compile_definitions(self: object, file):
        if not self._compile_definitions:
            return

        file.write(f"target_compile_definitions(${{{self._cmake_var_name}}} PRIVATE\n")
        for macro, value in self._compile_definitions:
            if not value:
                file.write(f"{macro}\n")
            else:
                file.write(f"{macro}={value}\n")
        file.write(f")\n\n")


# ==========================================================================================================================
# ==========================================================================================================================


class ExecutableGeneratorPart(IGeneratorPart):
    def __init__(
            self: object,
            cmake_var_name: str,
            prefix: str,
            project_name: str,
            executable_file: str
    ):
        self._cmake_var_name = cmake_var_name
        self._prefix = prefix
        self._project_name = project_name
        self._executable_file = executable_file

    def run(self: object, file) -> None:
        self._write_executable_header(file)

    def _write_executable_header(self: object, file) -> None:
        exe_name = self._prefix + self._project_name
        file.write( f"set({self._cmake_var_name} \"{exe_name}\")\n"
                    f"add_executable(${{{self._cmake_var_name}}} ${{CMAKE_SOURCE_DIR}}/{self._executable_file})\n\n"
                    )


# ==========================================================================================================================
# ==========================================================================================================================


class LinkerGeneratorPart(IGeneratorPart):
    def __init__(
            self: object,
            cmake_exe_var_name: str,
            *cmake_lib_var_names
    ):
        self._cmake_exe_var_name = cmake_exe_var_name
        self._cmake_lib_var_names = cmake_lib_var_names

    def run(self: object, file) -> None:
        self._write_target_link_libraries(file)

    def _write_target_link_libraries(self: object, file) -> None:
        file.write(f"target_link_libraries(${{{self._cmake_exe_var_name}}} PUBLIC\n")
        for lib in self._cmake_lib_var_names:
            file.write(f"${{{lib}}}\n")
        file.write(f")\n\n")
