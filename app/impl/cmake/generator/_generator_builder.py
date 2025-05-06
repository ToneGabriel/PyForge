from ._generator_base import Generator
from ._generator_parts import   CMakeTargetVisibility,\
                                CMakeLibraryType,\
                                HeaderGeneratorPart,\
                                LibraryGeneratorPart,\
                                ExecutableGeneratorPart,\
                                IncludeGeneratorPart,\
                                SourceGeneratorPart,\
                                DefinitionGeneratorPart,\
                                GoogleTestLibraryGeneratorPart,\
                                LinkerGeneratorPart


__all__ = ["GeneratorBuilder",
           "CMakeLibraryType",
           "CMakeTargetVisibility"
           ]


class GeneratorBuilder:
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
                   c_language_standard: int,
                   c_language_standard_required: bool,
                   c_compiler_extensions_required: bool,
                   cpp_language_standard: int,
                   cpp_language_standard_required: bool,
                   cpp_compiler_extensions_required: bool
    ) -> None:
        part = HeaderGeneratorPart(cmake_minimum_required_version,
                                    project_name,
                                    project_version,
                                    c_language_standard,
                                    c_language_standard_required,
                                    c_compiler_extensions_required,
                                    cpp_language_standard,
                                    cpp_language_standard_required,
                                    cpp_compiler_extensions_required
                                    )
        self._generator.add_part(part)

    def add_library(self,
                    name: str,
                    type: CMakeLibraryType,
    ) -> str:
        part = LibraryGeneratorPart(name, type)
        self._generator.add_part(part)
        return part.cmake_variable_name

    def add_executable(self,
                       name: str,
                       executable_file: str,
    ) -> str:
        part = ExecutableGeneratorPart(name, executable_file)
        self._generator.add_part(part)
        return part.cmake_variable_name

    def add_target_include_directories(self,
                                       cmake_target_var_name: str,
                                       visibility: CMakeTargetVisibility,
                                       include_directories: list[str]
    ) -> None:
        part = IncludeGeneratorPart(cmake_target_var_name, visibility, include_directories)
        self._generator.add_part(part)

    def add_target_sources(self,
                           cmake_target_var_name: str,
                           visibility: CMakeTargetVisibility,
                           source_files: list[str],
    ) -> None:
        part = SourceGeneratorPart(cmake_target_var_name, visibility, source_files)
        self._generator.add_part(part)

    def add_target_compile_definitions(self,
                                       cmake_target_var_name: str,
                                       visibility: CMakeTargetVisibility,
                                       compile_definitions: list[tuple[str, str]]
    ) -> None:
        part = DefinitionGeneratorPart(cmake_target_var_name, visibility, compile_definitions)
        self._generator.add_part(part)

    def add_target_linker(self,
                          cmake_target_var_name: str,
                          visibility: CMakeTargetVisibility,
                          *cmake_other_var_names
    ) -> None:
        part = LinkerGeneratorPart(cmake_target_var_name, visibility, *cmake_other_var_names)
        self._generator.add_part(part)

    def add_googletest_library(self,
                               git_tag: str="main"
    ) -> tuple[str, str]:
        part = GoogleTestLibraryGeneratorPart(git_tag)
        self._generator.add_part(part)
        return [part.gtest_cmake_variable_name, part.gmock_cmake_variable_name]
