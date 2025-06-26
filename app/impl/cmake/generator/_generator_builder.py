from ._generator_base import Generator
from ._generator_parts import *


__all__ = ["GeneratorBuilder",
           "CMakeLibraryType",
           "CMakeTargetVisibility",
           "Language"
           ]


class GeneratorBuilder:
    """
    Builder class for Generator that appends parts to it and returns the complete product
    """

    def __init__(self):
        self.reset_generator_product()

    @property
    def generator_product(self) -> Generator:
        return self._generator

    def reset_generator_product(self) -> None:
        self._generator = Generator()

    def add_header(self,
                   cmake_minimum_required_version: str,
                   project_name: str,
                   project_version: str,
                   project_language: Language,
                   language_standard: int,
                   language_standard_required: bool,
                   compiler_extensions_required: bool,
    ) -> None:
        """
        Append Header part to generator

        :param cmake_minimum_required_version: str with minimum cmake version (format: major.minor.patch)
        :param project_name: str with project name
        :param project_version: str with project version (format: major.minor.patch)
        :param project_language: language C or CPP
        :param language_standard: int for C/C++ language standard
        :param language_standard_required: `False` to use lower standard
        :param compiler_extensions_required: `True` to use optional compiler specific extensions
        """

        part = HeaderGeneratorPart(cmake_minimum_required_version,
                                   project_name,
                                   project_version,
                                   project_language,
                                   language_standard,
                                   language_standard_required,
                                   compiler_extensions_required
                                   )
        self._generator.add_part(part)

    def add_library(self,
                    name: str,
                    type: CMakeLibraryType,
    ) -> str:
        """
        Append Library part to generator

        :param name: name of the compiled library file
        :param type: library type (STATIC, SHARED, INTERFACE)
        :returns str: cmake variable name for the newly created library
        (used in `add_target_include_directories`, `add_target_sources`, `add_target_compile_definitions`, `add_target_linker`)
        """

        part = LibraryGeneratorPart(name, type)
        self._generator.add_part(part)
        return part.cmake_variable_name

    def add_imported_library(self,
                             name: str,
                             type: CMakeLibraryType,
                             imported_location : str,
                             imported_impl_location : str,
                             imported_include_dir : str
    ) -> str:
        """
        Append Imported Library part to generator

        :param name: name used to generate the cmake variable name
        :param type: library type (STATIC, SHARED, INTERFACE)
        :param imported_location: relative path where to find the library
        :param imported_impl_location: relative path where to find the library implementation
        (used for SHARED implementation library, can use `imported_location` if STATIC)
        :param imported_include_dir: relative path to imported library headers directory
        :returns str: cmake variable name for the newly created library
        (used in `add_target_include_directories`, `add_target_sources`, `add_target_compile_definitions`, `add_target_linker`)
        """

        part = ImportedLibraryGeneratorPart(name, type, imported_location, imported_impl_location, imported_include_dir)
        self._generator.add_part(part)
        return part.cmake_variable_name

    def add_executable(self,
                       name: str,
                       executable_file: str=None,
    ) -> str:
        """
        Append Executable part to generator

        :param name: name of the compiled executable file
        :param executable_file: relative path to main.c or main.cpp file
        :returns str: cmake variable name for the newly created executable
        """

        part = ExecutableGeneratorPart(name, executable_file)
        self._generator.add_part(part)
        return part.cmake_variable_name

    def add_target_include_directories(self,
                                       cmake_target_var_name: str,
                                       visibility: CMakeTargetVisibility,
                                       include_directories: list[str]
    ) -> None:
        """
        Append Include Directory part to generator

        :param cmake_target_var_name: name of target to add headers to (returned from `add_library`, `add_imported_library`, `add_executable`)
        :param visibility: cmake forward visibility
        :param include_directories: list of relative paths to header directories
        """

        part = IncludeGeneratorPart(cmake_target_var_name, visibility, include_directories)
        self._generator.add_part(part)

    def add_target_sources(self,
                           cmake_target_var_name: str,
                           visibility: CMakeTargetVisibility,
                           source_files: list[str],
    ) -> None:
        """
        Append Sources part to generator

        :param cmake_target_var_name: name of target to add headers to (returned from `add_library`, `add_imported_library`, `add_executable`)
        :param visibility: cmake forward visibility
        :param source_files: list of relative paths to source files
        """

        part = SourceGeneratorPart(cmake_target_var_name, visibility, source_files)
        self._generator.add_part(part)

    def add_target_compile_definitions(self,
                                       cmake_target_var_name: str,
                                       visibility: CMakeTargetVisibility,
                                       compile_definitions: list[tuple[str, str]]
    ) -> None:
        """
        Append Compile Definitions part to generator

        :param cmake_target_var_name: name of target to add headers to (returned from `add_library`, `add_imported_library`, `add_executable`)
        :param visibility: cmake forward visibility
        :param compile_definitions: list of pairs of str (first: MACRO name, second: MACRO value)
        """

        part = DefinitionGeneratorPart(cmake_target_var_name, visibility, compile_definitions)
        self._generator.add_part(part)

    def add_target_linker(self,
                          cmake_target_var_name: str,
                          visibility: CMakeTargetVisibility,
                          *cmake_lib_var_names
    ) -> None:
        """
        Append Linker part to generator

        :param cmake_target_var_name: the cmake variable name to be linked onto (created by `add_library`, `add_imported_library`, `add_executable`)
        :param visibility: cmake forward visibility
        :param cmake_lib_var_names: the cmake variable names to be linked to the first param (created by `add_library`, `add_imported_library`)
        """

        part = LinkerGeneratorPart(cmake_target_var_name, visibility, *cmake_lib_var_names)
        self._generator.add_part(part)
