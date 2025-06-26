from . import jsonvalid
from . import cmake


__all__ = ["ImplementationSharedState"]


_EXPECTED_JSON_STRUCTURE = {
    "path_settings":
    {
        "root_dir": str,
        "include_dirs": list,
        "source_dirs_ignore": list,
        "imports":
        {
            "static": list,
            "shared": list
        }
    },

    "project_settings":
    {
        "name": str,
        "version":
        {
            "major": int,
            "minor": int,
            "patch": int
        },

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
    """
    Structure representing the parsed json file
    """
    def __init__(self, json_path: str):
        self._json_data = jsonvalid.load(json_path, _EXPECTED_JSON_STRUCTURE)

# path_settings
    @property
    def project_root_path(self) -> str:
        return self._json_data["path_settings"]["root_dir"]

    @property
    def project_include_dir_names(self) -> str:
        return self._json_data["path_settings"]["include_dirs"]

    @property
    def project_source_ignored_dir_names(self) -> list[str]:
        return self._json_data["path_settings"]["source_dirs_ignore"]

    @property
    def project_imported_static_libs(self) -> list[tuple[str, str]]:
        return self._json_data["path_settings"]["imports"]["static"]

    @property
    def project_imported_shared_libs(self) -> list[tuple[str, str, str]]:
        return self._json_data["path_settings"]["imports"]["shared"]

# project_settings
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

# compiler_settings
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
    """
    Singleton class used to centralize ALL cmake and cmd functions
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # declare first
        self._json_path = None
        self._cmake_bin_path = None
        self._ninja_bin_path = None
        self._dataset = None

    def initialize(self,
                   json_path: str,
                   cmake_bin_path: str,
                   ninja_bin_path: str,
    ) -> None:
        self._json_path = json_path
        self._cmake_bin_path = cmake_bin_path
        self._ninja_bin_path = ninja_bin_path
        self.reload()

    def is_initialized(self) -> bool:
        return all(param is not None for param in (self._json_path,
                                                   self._cmake_bin_path,
                                                   self._ninja_bin_path))

    def reload(self) -> None:
        """
        Reload data from json if changed while running
        """
        self._check_initialization()
        self._dataset = _Dataset(self._json_path)

    def configure_project(self) -> None:
        """
        Check if json data was parsed, generate CMakelists.txt file and run cmake configuration
        """
        self._check_initialization()
        cmake.generate( project_root_path=self._dataset.project_root_path,
                        project_include_dir_names=self._dataset.project_include_dir_names,
                        project_source_ignored_dir_names=self._dataset.project_source_ignored_dir_names,
                        project_imported_static_libs=self._dataset.project_imported_static_libs,
                        project_imported_shared_libs=self._dataset.project_imported_shared_libs,
                        project_name=self._dataset.project_name,
                        project_product_type=self._dataset.project_product_type,
                        project_version=self._dataset.project_version,
                        project_language=self._dataset.project_language,
                        language_standard=self._dataset.language_standard,
                        language_standard_required=self._dataset.language_standard_required,
                        compiler_extensions_required=self._dataset.compiler_extensions_required,
                        cmake_compile_definitions=self._dataset.cmake_compile_definitions
        )
        cmake.configure(project_root_path=self._dataset.project_root_path,
                        project_build_type=self._dataset.project_build_type,
                        c_compiler_path=self._dataset.compiler_path,
                        cpp_compiler_path=self._dataset.compiler_path,
                        cmake_bin_path=self._cmake_bin_path,
                        ninja_bin_path=self._ninja_bin_path,
        )

    def build_project(self) -> None:
        """
        Check if json data was parsed and apply cmd commands for cmake build
        """
        self._check_initialization()
        cmake.build(project_root_path=self._dataset.project_root_path,
                    cmake_bin_path=self._cmake_bin_path,
                    ninja_bin_path=self._ninja_bin_path,
        )

    def _check_initialization(self) -> None:
        if not self.is_initialized():
            raise RuntimeError("Shared state has not been initialized. Call initialize() first.")
