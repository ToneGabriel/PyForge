from enum import Enum
from ._cmd_base import ICMDPart, override


class BuildType(Enum):
    DEBUGG = "Debugg"
    RELEASE = "Release"
    DBGRELEASE = "RelWithDebInfo"
    MINRELEASE = "MinSizeRel"


# ==========================================================================================================================
# ==========================================================================================================================


class CMakeGeneratePart(ICMDPart):
    def __init__(self,
                 cmakelists_root_dir_path: str,
                 build_type: BuildType,
                 build_dir_path: str,
                 c_compiler_path: str=None,
                 cpp_compiler_path: str=None
    ):
        self._cmakelists_root_dir_path = cmakelists_root_dir_path
        self._build_type = build_type
        self._build_dir_path = build_dir_path
        self._c_compiler_path = c_compiler_path
        self._cpp_compiler_path = cpp_compiler_path

    @override
    def get_cmd_text(self) -> str:
        ret = "cmake"
        ret += f" -S \"{self._cmakelists_root_dir_path}\""
        ret += f" -G \"Ninja\""
        ret += f" -B \"{self._build_dir_path}\""
        ret += f" -D CMAKE_BUILD_TYPE={self._build_type.value}"

        if self._c_compiler_path:
            ret += f" -D CMAKE_C_COMPILER=\"{self._c_compiler_path}\""

        if self._cpp_compiler_path:
            ret += f" -D CMAKE_CXX_COMPILER=\"{self._cpp_compiler_path}\""

        return ret


# ==========================================================================================================================
# ==========================================================================================================================


class CMakeBuildPart(ICMDPart):
    def __init__(self,
                 build_dir_path: str,
    ):
        self._build_dir_path = build_dir_path

    @override
    def get_cmd_text(self) -> str:
        ret = f"cmake --build \"{self._build_dir_path}\""
        return ret


# ==========================================================================================================================
# ==========================================================================================================================


class CMakeBuildClearPart(ICMDPart):
    def __init__(self,
                 build_dir_path: str
    ):
        self._build_dir_path = build_dir_path

    @override
    def get_cmd_text(self) -> str:
        ret = f"if exist \"{self._build_dir_path}\" rmdir /s /q \"{self._build_dir_path}\""
        return ret
