from . import structure
from . import cmake
from . import jsonvalid


_EXPECTED_BUILD_JSON_STRUCTURE = {
    "project_settings":
    {
        "root": str,
        "name": str,
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


class _SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)

        return cls._instances[cls]


class _Database(metaclass=_SingletonMeta):
    def __init__(self: object):
        self._data = None

    def is_initialized(self: object) -> bool:
        return self._data is not None

    def initialize(self: object, json_path: str, zip_structure_path: str) -> None:
        if self.is_initialized():
            return

        self._data = jsonvalid.load(json_path, _EXPECTED_BUILD_JSON_STRUCTURE)
        self._data["zip_structure_path"] = zip_structure_path

    @property
    def zip_structure_path(self: object) -> str:
        return self._data["zip_structure_path"]

    @property
    def project_root_path(self: object) -> str:
        return self._data["project_settings"]["root"]

    @property
    def project_name(self: object) -> str:
        return self._data["project_settings"]["name"]

    @property
    def project_build_type(self: object) -> str:
        return self._data["project_settings"]["build"]

    @property
    def project_version(self: object) -> str:
        return (f"{self._data["project_settings"]["version"]["major"]}."
                f"{self._data["project_settings"]["version"]["minor"]}."
                f"{self._data["project_settings"]["version"]["patch"]}"
                )

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


def _get_database() -> _Database:
    db = _Database()

    if not db.is_initialized():
        raise RuntimeError("Database has not been initialized. Call initialize() first.")

    return db


def initialize(json_path: str, zip_structure_path: str) -> None:
    db = _Database()
    db.initialize(json_path, zip_structure_path)


def setup_project_structure() -> None:
    db = _get_database()
    structure.setup_project(zip_structure_path=db.zip_structure_path,
                            project_root_path=db.project_root_path)


def generate_cmakelists() -> None:
    db = _get_database()
    cmake.generate( project_root_path=db.project_root_path,
                    project_name=db.project_name,
                    project_build_type=db.project_build_type,
                    project_version=db.project_version,
                    c_language_standard=db.c_language_standard,
                    c_language_standard_required=db.c_language_standard_required,
                    c_compiler_extensions_required=db.c_compiler_extensions_required,
                    cpp_language_standard=db.cpp_language_standard,
                    cpp_language_standard_required=db.cpp_language_standard_required,
                    cpp_compiler_extensions_required=db.cpp_compiler_extensions_required,
                    cmake_compile_definitions=db.cmake_compile_definitions)


def build_project(clean: bool=False) -> None:
    db = _get_database()
    cmake.build(project_root_path=db.project_root_path,
                cmake_generator=db.cmake_generator,
                c_compiler_path=db.c_compiler_path,
                cpp_compiler_path=db.cpp_compiler_path,
                clean=clean)
