from . import structure
from . import cmake
from . import jsonvalid


__all__ = ["initialize",
           "setup_project_structure",
           "generate_cmakelists",
           "build_project"
           ]


_EXPECTED_BUILD_JSON_STRUCTURE = {
    "project_settings":
    {
        "root": str,
        "name": str,
        "version":
        {
            "major": int,
            "minor": int,
            "patch": int
        },
        "product": str,
        "build": str,
        "compile_definitions": list
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
    }
}   # END _EXPECTED_BUILD_JSON_STRUCTURE


class _SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)

        return cls._instances[cls]


class _Dataset(metaclass=_SingletonMeta):
    def __init__(self: object):
        self._data = None

    def is_initialized(self: object) -> bool:
        return self._data is not None

    def initialize(self: object,
                   json_path: str,
                   cmake_bin_path: str,
                   ninja_bin_path: str,
                   zip_structure_path: str
    ) -> None:
        # override prev config if any
        self._data = jsonvalid.load(json_path, _EXPECTED_BUILD_JSON_STRUCTURE)
        self._data["cmake_bin_path"] = cmake_bin_path
        self._data["ninja_bin_path"] = ninja_bin_path
        self._data["zip_structure_path"] = zip_structure_path

    @property
    def cmake_bin_path(self: object) -> str:
        return self._data["cmake_bin_path"]
    
    @property
    def ninja_bin_path(self: object) -> str:
        return self._data["ninja_bin_path"]

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
    def project_version(self: object) -> str:
        return (f"{self._data["project_settings"]["version"]["major"]}."
                f"{self._data["project_settings"]["version"]["minor"]}."
                f"{self._data["project_settings"]["version"]["patch"]}"
                )

    @property
    def project_product_type(self: object) -> cmake.ProductType:
        return cmake.ProductType(self._data["project_settings"]["product"])

    @property
    def project_build_type(self: object) -> None:
        pass
        # return self._data["project_settings"]["build"]

    @property
    def cmake_compile_definitions(self: object) -> list[tuple[str, str]]:
        return self._data["project_settings"]["compile_definitions"]

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


def _get_dataset() -> _Dataset:
    data = _Dataset()

    if not data.is_initialized():
        raise RuntimeError("Dataset has not been initialized. Call initialize() first.")

    return data


def initialize(json_path: str,
               cmake_bin_path: str,
               ninja_bin_path: str,
               zip_structure_path: str
    ) -> None:
    data = _Dataset()
    data.initialize(json_path, cmake_bin_path, ninja_bin_path, zip_structure_path)


def setup_project_structure() -> None:
    data = _get_dataset()
    structure.setup_project(zip_structure_path=data.zip_structure_path,
                            project_root_path=data.project_root_path)


def generate_cmakelists() -> None:
    data = _get_dataset()
    cmake.generate( project_root_path=data.project_root_path,
                    project_name=data.project_name,
                    project_product_type=data.project_product_type,
                    project_version=data.project_version,
                    c_language_standard=data.c_language_standard,
                    c_language_standard_required=data.c_language_standard_required,
                    c_compiler_extensions_required=data.c_compiler_extensions_required,
                    cpp_language_standard=data.cpp_language_standard,
                    cpp_language_standard_required=data.cpp_language_standard_required,
                    cpp_compiler_extensions_required=data.cpp_compiler_extensions_required,
                    cmake_compile_definitions=data.cmake_compile_definitions)


def build_project(clean: bool=False) -> None:
    data = _get_dataset()
    cmake.build(project_root_path=data.project_root_path,
                c_compiler_path=data.c_compiler_path,
                cpp_compiler_path=data.cpp_compiler_path,
                cmake_bin_path=data.cmake_bin_path,
                ninja_bin_path=data.ninja_bin_path,
                clean=clean)
