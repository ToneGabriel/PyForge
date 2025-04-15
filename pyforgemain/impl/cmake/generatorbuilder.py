from .generator import Generator
from .generatorparts import HeaderGeneratorPart,\
                            StaticLibraryGeneratorPart,\
                            SharedLibraryGeneratorPart,\
                            ExecutableGeneratorPart


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
            executable_file: str
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
        self.reset_generator()

    @property
    def generator(self: object) -> Generator:
        return self._generator

    def reset_generator(self: object) -> None:
        self._generator = Generator()

    def add_header(self: object) -> None:
        self._generator.add_part(HeaderGeneratorPart(
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

    def add_static_library(self: object) -> None:
        self._generator.add_part(StaticLibraryGeneratorPart(
                                    self._project_name,
                                    self._include_directories,
                                    self._source_files
                                    )
                                )

    def add_shared_library(self: object) -> None:
        self._generator.add_part(SharedLibraryGeneratorPart(
                                    self._project_name,
                                    self._include_directories,
                                    self._source_files
                                    )
                                )

    def add_executable(self: object) -> None:
        self._generator.add_part(ExecutableGeneratorPart(
                                    self._project_name,
                                    self._executable_file
                                    )
                                )

    def add_compile_definitions(self: object) -> None:
        pass
        part = None
        self._generator.add_part(part)
