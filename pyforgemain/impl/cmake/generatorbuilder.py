from .generator import Generator
from .generatorparts import HeaderGeneratorPart,\
                            StaticLibraryGeneratorPart, \
                            SharedLibraryGeneratorPart


class GeneratorBuilder:
    def __init__(self: object):
        self.reset()

    @property
    def generator(self: object) -> Generator:
        return self._generator

    def reset(self: object) -> None:
        self._generator = Generator()

    def add_header(
            self: object,
            project_name: str,
            project_version: str,
            c_language_standard: int,
            c_language_standard_required: bool,
            c_compiler_extensions_required: bool,
            cpp_language_standard: int,
            cpp_language_standard_required: bool,
            cpp_compiler_extensions_required: bool
    ) -> None:
        part = HeaderGeneratorPart(
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
