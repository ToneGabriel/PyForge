from . import jsonvalid
from . import structure
from . import cmake


__all__ = ["ImplementationSharedState"]


_EXPECTED_JSON_STRUCTURE = {
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
        "include_dir_name": str,
        "source_dir_name": str,

        "language": str,
        "product": str,
        "build": str,
        "compile_definitions": list
    },

    "compiler_settings":
    {
        "compiler_path": str,
        "compiler_extensions_required": bool,
        "language_standard": int,
        "language_standard_required": bool
    }
}   # END _EXPECTED_JSON_STRUCTURE


# ==========================================================================================================================
# ==========================================================================================================================


class _Dataset:
    def __init__(self, json_path: str):
        self._json_data = jsonvalid.load(json_path, _EXPECTED_JSON_STRUCTURE)

    @property
    def project_root_path(self) -> str:
        return self._json_data["project_settings"]["root"]

    @property
    def project_name(self) -> str:
        return self._json_data["project_settings"]["name"]

    @property
    def project_version(self) -> str:
        return (f"{self._json_data["project_settings"]["version"]["major"]}."
                f"{self._json_data["project_settings"]["version"]["minor"]}."
                f"{self._json_data["project_settings"]["version"]["patch"]}"
                )

    @property
    def include_dir_name(self) -> str:
        return self._json_data["project_settings"]["include_dir_name"]

    @property
    def source_dir_name(self) -> str:
        return self._json_data["project_settings"]["source_dir_name"]

    @property
    def project_language(self) -> cmake.Language:
        # [] for match by enum name
        return cmake.Language[self._json_data["project_settings"]["language"]]

    @property
    def project_product_type(self) -> cmake.ProductType:
        # [] for match by enum name
        return cmake.ProductType[self._json_data["project_settings"]["product"]]

    @property
    def project_build_type(self) -> cmake.BuildType:
        # [] for match by enum name
        return cmake.BuildType[self._json_data["project_settings"]["build"]]

    @property
    def cmake_compile_definitions(self) -> list[tuple[str, str]]:
        return self._json_data["project_settings"]["compile_definitions"]

    @property
    def compiler_path(self) -> str:
        return self._json_data["compiler_settings"]["compiler_path"]

    @property
    def compiler_extensions_required(self) -> bool:
        return self._json_data["compiler_settings"]["compiler_extensions_required"]

    @property
    def language_standard(self) -> int:
        return self._json_data["compiler_settings"]["language_standard"]

    @property
    def language_standard_required(self) -> bool:
        return self._json_data["compiler_settings"]["language_standard_required"]


# ==========================================================================================================================
# ==========================================================================================================================


class ImplementationSharedState:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._json_path = None
        self._cmake_bin_path = None
        self._ninja_bin_path = None
        self._zip_structure_path = None
        self._dataset = None

    def initialize(self,
                   json_path: str,
                   cmake_bin_path: str,
                   ninja_bin_path: str,
                   zip_structure_path: str
    ) -> None:
        self._json_path = json_path
        self._cmake_bin_path = cmake_bin_path
        self._ninja_bin_path = ninja_bin_path
        self._zip_structure_path = zip_structure_path
        self.reload()

    def is_initialized(self) -> bool:
        return self._json_path is not None

    def reload(self) -> None:
        self._check_initialization()
        self._dataset = _Dataset(self._json_path)

    def setup_project_structure(self) -> None:
        self._check_initialization()
        structure.setup_project(zip_structure_path=self._zip_structure_path,
                                project_root_path=self._dataset.project_root_path
        )

    def generate_cmakelists(self) -> None:
        self._check_initialization()
        cmake.generate( project_root_path=self._dataset.project_root_path,
                        project_name=self._dataset.project_name,
                        project_product_type=self._dataset.project_product_type,
                        project_version=self._dataset.project_version,
                        project_language=self._dataset.project_language,
                        language_standard=self._dataset.language_standard,
                        language_standard_required=self._dataset.language_standard_required,
                        compiler_extensions_required=self._dataset.compiler_extensions_required,
                        cmake_compile_definitions=self._dataset.cmake_compile_definitions
        )

    def build_project(self, clean: bool=False) -> None:
        self._check_initialization()
        cmake.build(project_root_path=self._dataset.project_root_path,
                    project_build_type=self._dataset.project_build_type,
                    c_compiler_path=self._dataset.compiler_path,
                    cpp_compiler_path=self._dataset.compiler_path,
                    cmake_bin_path=self._cmake_bin_path,
                    ninja_bin_path=self._ninja_bin_path,
                    clean=clean
        )

    def _check_initialization(self) -> None:
        if not self.is_initialized():
            raise RuntimeError("Shared state has not been initialized. Call initialize() first.")
