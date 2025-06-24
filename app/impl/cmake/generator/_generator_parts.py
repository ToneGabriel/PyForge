from enum import Enum, auto
from ._generator_base import IGeneratorPart, override


# Implemented ALL generator parts (as IGeneratorPart)


__all__ = ["CMakeLibraryType",
           "CMakeTargetVisibility",
           "Language",
           "HeaderGeneratorPart",
           "LibraryGeneratorPart",
           "ImportedLibraryGeneratorPart",
           "ExecutableGeneratorPart",
           "IncludeGeneratorPart",
           "SourceGeneratorPart",
           "DefinitionGeneratorPart",
           "LinkerGeneratorPart"
           ]


class CMakeLibraryType(Enum):
    STATIC = "STATIC"
    SHARED = "SHARED"
    INTERFACE = "INTERFACE"


class CMakeTargetVisibility(Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    INTERFACE = "INTERFACE"


class Language(Enum):
    C = "C"
    CPP = "CXX"


# ==========================================================================================================================
# ==========================================================================================================================


def _adapt_to_cmake_bool(value: bool) -> str:
    return "ON" if value else "OFF"


def _adapt_to_cmake_path_separator(path: str) -> str:
    return path.replace("\\", "/")


class _COMPILER_SETTINGS_NAMES(Enum):
    LANGUAGE_STANDARD = auto()
    LANGUAGE_STANDARD_REQUIRED = auto()
    COMPILER_EXTENSION_REQUIRED = auto()


_C_CMAKE_COMPILER_SETTINGS_NAMES = {
    _COMPILER_SETTINGS_NAMES.LANGUAGE_STANDARD: "CMAKE_C_STANDARD",
    _COMPILER_SETTINGS_NAMES.LANGUAGE_STANDARD_REQUIRED: "CMAKE_C_STANDARD_REQUIRED",
    _COMPILER_SETTINGS_NAMES.COMPILER_EXTENSION_REQUIRED: "CMAKE_C_EXTENSIONS"
}

_CPP_CMAKE_COMPILER_SETTINGS_NAMES = {
    _COMPILER_SETTINGS_NAMES.LANGUAGE_STANDARD: "CMAKE_CXX_STANDARD",
    _COMPILER_SETTINGS_NAMES.LANGUAGE_STANDARD_REQUIRED: "CMAKE_CXX_STANDARD_REQUIRED",
    _COMPILER_SETTINGS_NAMES.COMPILER_EXTENSION_REQUIRED: "CMAKE_CXX_EXTENSIONS"
}


# ==========================================================================================================================
# ==========================================================================================================================


class HeaderGeneratorPart(IGeneratorPart):
    def __init__(
            self,
            cmake_minimum_required_version: str,
            project_name: str,
            project_version: str,
            project_language: Language,
            language_standard: int,
            language_standard_required: bool,
            compiler_extensions_required: bool
    ):
        """
        Create Header part to append to generator
        :param cmake_minimum_required_version: str with minimum cmake version (format: major.minor.patch)
        :param project_name: str with project name
        :param project_version: str with project version (format: major.minor.patch)
        :param project_language: language C or CPP
        :param language_standard: int for C/C++ language standard
        :param language_standard_required: `False` to use lower standard
        :param compiler_extensions_required: `True` to use optional compiler specific extensions
        """

        self._cmake_minimum_required_version = cmake_minimum_required_version
        self._project_name = project_name
        self._project_version = project_version
        self._project_language = project_language
        self._language_standard = language_standard
        self._language_standard_required = language_standard_required
        self._compiler_extensions_required = compiler_extensions_required

    @override
    def run(self, file) -> None:
        self._write_cmake_minimum_required_version(file)
        self._write_project_specifications(file)
        self._write_language_specifications(file)
        self._write_destination_specifications(file)

    def _write_cmake_minimum_required_version(self, file) -> None:
        file.write( f"cmake_minimum_required(VERSION {self._cmake_minimum_required_version} FATAL_ERROR)\n\n")

    def _write_project_specifications(self, file) -> None:
        file.write( f"project({self._project_name} "
                    f"VERSION {self._project_version} "
                    f"LANGUAGES {self._project_language.value})\n\n"
                    )

    def _write_language_specifications(self, file) -> None:
        cmake_compiler_settings_names_dict: dict[_COMPILER_SETTINGS_NAMES, str] = {}

        if self._project_language == Language.C:
            cmake_compiler_settings_names_dict = _C_CMAKE_COMPILER_SETTINGS_NAMES
        else:
            cmake_compiler_settings_names_dict = _CPP_CMAKE_COMPILER_SETTINGS_NAMES

        file.write( f"set({cmake_compiler_settings_names_dict[_COMPILER_SETTINGS_NAMES.LANGUAGE_STANDARD]} {self._language_standard})\n"
                    f"set({cmake_compiler_settings_names_dict[_COMPILER_SETTINGS_NAMES.LANGUAGE_STANDARD_REQUIRED]} {_adapt_to_cmake_bool(self._language_standard_required)})\n"
                    f"set({cmake_compiler_settings_names_dict[_COMPILER_SETTINGS_NAMES.COMPILER_EXTENSION_REQUIRED]} {_adapt_to_cmake_bool(self._compiler_extensions_required)})\n\n"
                    )

    def _write_destination_specifications(self, file) -> None:
        file.write( f"set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/bin)\n"
                    f"set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/lib)\n"
                    f"set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/lib)\n\n"
                    )


# ==========================================================================================================================
# ==========================================================================================================================


class LibraryGeneratorPart(IGeneratorPart):
    def __init__(
            self,
            name: str,
            type: CMakeLibraryType,
    ):
        """
        Create Library part to append to generator

        :param name: name of the compiled library file
        :param type: library type (STATIC, SHARED, INTERFACE)
        """

        self._name = name
        self._type = type

    @property
    def cmake_variable_name(self) -> str:
        return self._name.upper() + "_LIB_NAME"

    @override
    def run(self, file) -> None:
        self._write_library_header(file)

    def _write_library_header(self, file) -> None:
        file.write( f"set({self.cmake_variable_name} {self._name})\n"
                    f"add_library(${{{self.cmake_variable_name}}} {self._type.value})\n"
                    f"set_target_properties(${{{self.cmake_variable_name}}} PROPERTIES PREFIX \"\" IMPORT_PREFIX \"\")\n\n")


# ==========================================================================================================================
# ==========================================================================================================================


class ImportedLibraryGeneratorPart(IGeneratorPart):
    def __init__(
            self,
            name: str,
            type: CMakeLibraryType,
            imported_location : str,
            imported_impl_location : str,
            imported_include_dir : str
    ):
        """
        Create Imported Library part to append to generator

        :param name: name used to generate the cmake variable name
        :param type: library type (STATIC, SHARED, INTERFACE)
        :param imported_location: relative path where to find the library
        :param imported_impl_location: relative path where to find the library implementation
        (used for SHARED implementation library, can use `imported_location` if STATIC)
        :param imported_include_dir: relative path to imported library headers directory
        """

        self._name = name
        self._type = type
        self._imported_location = imported_location
        self._imported_impl_location = imported_impl_location
        self._imported_include_dir = imported_include_dir

    @property
    def cmake_variable_name(self) -> str:
        return self._name.upper() + "_LIB_NAME"

    @override
    def run(self, file) -> None:
        self._write_library_header(file)

    def _write_library_header(self, file) -> None:
        file.write( f"set({self.cmake_variable_name} {self._name})\n"
                    f"add_library(${{{self.cmake_variable_name}}} {self._type.value} IMPORTED)\n"
                    f"set_target_properties(${{{self.cmake_variable_name}}} PROPERTIES \n"
                    f"IMPORTED_LOCATION ${{CMAKE_SOURCE_DIR}}/{_adapt_to_cmake_path_separator(self._imported_location)}\n"
                    f"IMPORTED_IMPLIB ${{CMAKE_SOURCE_DIR}}/{_adapt_to_cmake_path_separator(self._imported_impl_location)}\n"
                    f"INTERFACE_INCLUDE_DIRECTORIES ${{CMAKE_SOURCE_DIR}}/{_adapt_to_cmake_path_separator(self._imported_include_dir)})\n\n")


# ==========================================================================================================================
# ==========================================================================================================================


class ExecutableGeneratorPart(IGeneratorPart):
    def __init__(
            self,
            name: str,
            executable_file: str=None
    ):
        """
        Create Executable part to append to generator

        :param name: name of the compiled executable file
        :param executable_file: relative path to main.c or main.cpp file
        """

        self._name = name
        self._executable_file = executable_file

    @property
    def cmake_variable_name(self) -> str:
        return self._name.upper() + "_EXE_NAME"

    @override
    def run(self, file) -> None:
        self._write_executable_header(file)

    def _write_executable_header(self, file) -> None:
        exe_file_output = f" ${{CMAKE_SOURCE_DIR}}/{_adapt_to_cmake_path_separator(self._executable_file)}" if self._executable_file else ""

        file.write( f"set({self.cmake_variable_name} {self._name})\n"
                    f"add_executable(${{{self.cmake_variable_name}}}{exe_file_output})\n\n"
                    )


# ==========================================================================================================================
# ==========================================================================================================================


class IncludeGeneratorPart(IGeneratorPart):
    def __init__(self,
                 cmake_target_var_name: str,
                 visibility: CMakeTargetVisibility,
                 include_directories: list[str]
    ):
        """
        Create Include Directory part to append to generator

        :param cmake_target_var_name: name of target to add headers to (returned from `add_library`, `add_imported_library`, `add_executable`)
        :param visibility: cmake forward visibility
        :param include_directories: list of relative paths to header directories
        """

        self._cmake_target_var_name = cmake_target_var_name
        self._visibility = visibility
        self._include_directories = include_directories

    @override
    def run(self, file):
        self._write_target_include_directories(file)

    def _write_target_include_directories(self, file) -> None:
        if not self._include_directories:
            return

        file.write(f"target_include_directories(${{{self._cmake_target_var_name}}} {self._visibility.value}\n")
        for dir in self._include_directories:
            file.write(f"${{CMAKE_SOURCE_DIR}}/{_adapt_to_cmake_path_separator(dir)}\n")
        file.write(f")\n\n")


# ==========================================================================================================================
# ==========================================================================================================================


class SourceGeneratorPart(IGeneratorPart):
    def __init__(self,
                 cmake_target_var_name: str,
                 visibility: CMakeTargetVisibility,
                 source_files: list[str]
    ):
        """
        Create Sources part to append to generator

        :param cmake_target_var_name: name of target to add headers to (returned from `add_library`, `add_imported_library`, `add_executable`)
        :param visibility: cmake forward visibility
        :param source_files: list of relative paths to source files
        """

        self._cmake_target_var_name = cmake_target_var_name
        self._visibility = visibility
        self._source_files = source_files

    @override
    def run(self, file):
        self._write_target_sources(file)

    def _write_target_sources(self, file) -> None:
        if not self._source_files:
            return

        file.write(f"target_sources(${{{self._cmake_target_var_name}}} {self._visibility.value}\n")
        for source in self._source_files:
            file.write(f"${{CMAKE_SOURCE_DIR}}/{_adapt_to_cmake_path_separator(source)}\n")
        file.write(f")\n\n")


# ==========================================================================================================================
# ==========================================================================================================================


class DefinitionGeneratorPart(IGeneratorPart):
    def __init__(self,
                 cmake_target_var_name: str,
                 visibility: CMakeTargetVisibility,
                 compile_definitions: list[tuple[str, str]]
    ):
        """
        Create Compile Definitions part to append to generator

        :param cmake_target_var_name: name of target to add headers to (returned from `add_library`, `add_imported_library`, `add_executable`)
        :param visibility: cmake forward visibility
        :param compile_definitions: list of pairs of str (first: MACRO name, second: MACRO value)
        """

        self._cmake_target_var_name = cmake_target_var_name
        self._visibility = visibility
        self._compile_definitions = compile_definitions

    @override
    def run(self, file):
        self._write_target_compile_definitions(file)

    def _write_target_compile_definitions(self, file):
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
            self,
            cmake_target_var_name: str,
            visibility: CMakeTargetVisibility,
            *cmake_lib_var_names
    ):
        """
        Create Linker part to append to generator. Not created if cmake_lib_var_names is `None`

        :param cmake_target_var_name: the cmake variable name to be linked onto (created by add_library, add_imported_library, add_executable)
        :param visibility: cmake forward visibility
        :param cmake_lib_var_names: the cmake variable names to be linked to the first param (created by add_library, add_imported_library)
        """

        self._cmake_target_var_name = cmake_target_var_name
        self._visibility = visibility
        self._cmake_lib_var_names = cmake_lib_var_names

    @override
    def run(self, file) -> None:
        self._write_target_link_libraries(file)

    def _write_target_link_libraries(self, file) -> None:
        if self._cmake_lib_var_names:
            file.write(f"target_link_libraries(${{{self._cmake_target_var_name}}} {self._visibility.value}\n")
            for lib in self._cmake_lib_var_names:
                file.write(f"${{{lib}}}\n")
            file.write(f")\n\n")
