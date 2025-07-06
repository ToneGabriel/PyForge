from ._cmd_base import CMDList
from ._cmd_parts import *


__all__ = ["CMDBuilder",
           "BuildType"
           ]


class CMDBuilder:
    """
    Builder class for CMD that appends parts to it and returns the complete product
    """

    def __init__(self, *env_paths: str):
        self.reset_cmd_product(*env_paths)

    @property
    def cmd_product(self) -> CMDList:
        return self._cmd_list

    def reset_cmd_product(self, *env_paths: str) -> None:
        self._cmd_list = CMDList(*env_paths)

    def add_cmake_generate_part(self,
                                cmakelists_root_dir_path: str,
                                build_type: BuildType,
                                build_dir_path: str,
                                c_compiler_path: str,
                                cpp_compiler_path: str
    ) -> None:
        """
        Append cmake generate command to cmd list

        :param cmakelists_root_dir_path: full path to CMakelists.txx
        :param build_type: type of the build DEBUGG, RELEASE, DBGRELEASE, MINRELEASE
        :param build_dir_path: full path to build directory
        :param c_compiler_path: full path to C compiler exe
        :param cpp_compiler_path: full path to C++ compiler exe
        """

        part = CMakeGeneratePart(cmakelists_root_dir_path,
                                 build_type,
                                 build_dir_path,
                                 c_compiler_path,
                                 cpp_compiler_path
                                 )
        self._cmd_list.add_part(part)

    def add_cmake_build_part(self,
                             build_dir_path: str
    ) -> None:
        """
        Append cmake build command to cmd list
        :param build_dir_path: full path to build directory
        """

        part = CMakeBuildPart(build_dir_path)
        self._cmd_list.add_part(part)

    def add_remove_directory_part(self,
                                  dir_path: str
    ) -> None:
        """
        Append rmdir command to cmd list
        :param dir_path: full path to directory to remove
        """

        part = RemoveDirectoryPart(dir_path)
        self._cmd_list.add_part(part)
