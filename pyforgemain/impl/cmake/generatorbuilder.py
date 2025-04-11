from .generator import Generator
from .parts import  HeaderGeneratorPart,\
                    StaticLibraryGeneratorPart, \
                    SharedLibraryGeneratorPart

class GeneratorBuilder:
    def __init__(self: object):
        self._generator = Generator()

    @property
    def generator(self: object) -> Generator:
        return self._generator

    def add_header(
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
    ) -> None:
        part = HeaderGeneratorPart(
                    cmake_minimum_required_version,
                    project_name,
                    project_version_major,
                    project_version_minor,
                    project_version_patch,
                    c_language_standard,
                    c_language_standard_required,
                    c_compiler_extensions_required,
                    cpp_language_standard,
                    cpp_language_standard_required,
                    cpp_compiler_extensions_required
                )
        self._generator.add_part(part)

    def add_static_library(
            self: object,
            project_name: str,
            include_directories: list[str],
            source_files: list[str]
    ) -> None:
        part = StaticLibraryGeneratorPart(
                    project_name,
                    include_directories,
                    source_files
                )
        self._generator.add_part(part)

    def add_shared_library(self: object) -> None:
        part = SharedLibraryGeneratorPart()
        self._generator.add_part(part)

    def add_executable(self: object) -> None:
        part = None
        self._generator.add_part(part)

    def add_compile_definitions(self: object) -> None:
        part = None
        self._generator.add_part(part)
