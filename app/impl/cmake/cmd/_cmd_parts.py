import platform
from enum import Enum
from ._cmd_base import ICMDPart


# Implemented ALL generator parts (as ICMDPart)


__all__ = ["BuildType",
           "CMakeGeneratePart",
           "CMakeBuildPart",
           "RemoveDirectoryPart"
           ]


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
        """
        Create cmake generate command to append to cmd list

        :param cmakelists_root_dir_path: full path to CMakelists.txx
        :param build_type: type of the build `DEBUGG`, `RELEASE`, `DBGRELEASE`, `MINRELEASE`
        :param build_dir_path: full path to build directory
        :param c_compiler_path: full path to C compiler exe
        :param cpp_compiler_path: full path to C++ compiler exe
        """

        self._cmakelists_root_dir_path = cmakelists_root_dir_path
        self._build_type = build_type
        self._build_dir_path = build_dir_path
        self._c_compiler_path = c_compiler_path
        self._cpp_compiler_path = cpp_compiler_path

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
        """
        Create cmake build command to append to cmd list
        :param build_dir_path: full path to build directory
        """

        self._build_dir_path = build_dir_path

    def get_cmd_text(self) -> str:
        ret = f"cmake --build \"{self._build_dir_path}\""
        return ret


# ==========================================================================================================================
# ==========================================================================================================================


class RemoveDirectoryPart(ICMDPart):
    def __init__(self,
                 dir_path: str
    ):
        """
        Create rmdir command to append to cmd list
        :param dir_path: full path to directory to remove
        """

        self._dir_path = dir_path

    def get_cmd_text(self) -> str:
        if platform.system() == "Windows":
            ret = f"if exist \"{self._dir_path}\" rmdir /s /q \"{self._dir_path}\""
        elif platform.system() == "Linux":
            ret = f"if [ -d \"{self._dir_path}\" ]; then rm -rf \"{self._dir_path}\"; fi"
        return ret
