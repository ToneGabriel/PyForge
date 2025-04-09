from . import structure
from . import cmake
from . import jsonvalid


_EXPECTED_BUILD_JSON_STRUCTURE = {
    "project_settings":
    {
        "root": str,
        "build": str,
        "version":
        {
            "major": int,
            "minor": int,
            "patch": int
        }
    },

    "c_settings":
    {
        "compiler_path": str,
        "compiler_extensions_required": bool,
        "language_standard": int,
        "language_standard_required": bool
    },

    "cpp_settings":
    {
        "compiler_path": str,
        "compiler_extensions_required": bool,
        "language_standard": int,
        "language_standard_required": bool
    },

    "cmake_settings":
    {
        "generator": str,
        "compile_definitions": list
    }
}   # END _EXPECTED_BUILD_JSON_STRUCTURE


class _ProjectSetupData:
    '''This class contains the parsed data from setup JSON as properties'''

    _CMAKE_MINIMUM_REQUIRED_VERSION: str = "3.22.1"

    def __init__(self: object, json_path: str):
        self._data = jsonvalid.load(json_path, _EXPECTED_BUILD_JSON_STRUCTURE)

    @property
    def cmake_minimum_required_version(self: object) -> str:
        return _ProjectSetupData._CMAKE_MINIMUM_REQUIRED_VERSION

    @property
    def project_root_path(self: object) -> str:
        return self._data["project_settings"]["root"]

    @property
    def build_type(self: object) -> str:
        return self._data["project_settings"]["build"]

    @property
    def project_version_major(self: object) -> int:
        return self._data["project_settings"]["version"]["major"]
    
    @property
    def project_version_minor(self: object) -> int:
        return self._data["project_settings"]["version"]["minor"]
    
    @property
    def project_version_patch(self: object) -> int:
        return self._data["project_settings"]["version"]["patch"]

    @property
    def c_compiler_path(self: object) -> str:
        return self._data["c_settings"]["compiler_path"]

    @property
    def c_compiler_extensions_required(self: object) -> bool:
        return self._data["c_settings"]["compiler_extensions_required"]

    @property
    def c_language_standard(self: object) -> int:
        return self._data["c_settings"]["language_standard"]

    @property
    def c_language_standard_required(self: object) -> bool:
        return self._data["c_settings"]["language_standard_required"]

    @property
    def cpp_compiler_path(self: object) -> str:
        return self._data["cpp_settings"]["compiler_path"]

    @property
    def cpp_compiler_extensions_required(self: object) -> bool:
        return self._data["cpp_settings"]["compiler_extensions_required"]

    @property
    def cpp_language_standard(self: object) -> int:
        return self._data["cpp_settings"]["language_standard"]

    @property
    def cpp_language_standard_required(self: object) -> bool:
        return self._data["cpp_settings"]["language_standard_required"]

    @property
    def cmake_generator(self: object) -> str:
        return self._data["cmake_settings"]["generator"]

    @property
    def cmake_compile_definitions(self: object) -> list[tuple[str, str]]:
        return self._data["cmake_settings"]["compile_definitions"]


class Forger:
    def __init__(self: object, json_path: str, zip_structure_path: str):
        self._project_setup_data = _ProjectSetupData(json_path)
        self._zip_structure_path = zip_structure_path

    def setup_project_structure(self: object) -> None:
        structure.setup_project(self._zip_structure_path, self._project_setup_data.project_root_path)

    def generate_cmakelists(self: object) -> None:
        cmake.generate(self._project_setup_data.project_root_path,
                       self._project_setup_data.cmake_minimum_required_version,
                       self._project_setup_data.build_type,
                       self._project_setup_data.project_version_major,
                       self._project_setup_data.project_version_minor,
                       self._project_setup_data.project_version_patch,
                       self._project_setup_data.c_language_standard,
                       self._project_setup_data.c_language_standard_required,
                       self._project_setup_data.c_compiler_extensions_required,
                       self._project_setup_data.cpp_language_standard,
                       self._project_setup_data.cpp_language_standard_required,
                       self._project_setup_data.cpp_compiler_extensions_required,
                       self._project_setup_data.cmake_compile_definitions,
                       )

    def build_project(self: object, clean: bool=False) -> None:
        cmake.build(self._project_setup_data.project_root_path,
                    self._project_setup_data.cmake_generator,
                    self._project_setup_data.c_compiler_path,
                    self._project_setup_data.cpp_compiler_path,
                    clean
                    )
