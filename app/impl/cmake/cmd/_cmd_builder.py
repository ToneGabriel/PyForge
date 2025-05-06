from ._cmd_base import CMDList
from ._cmd_parts import CMakeGeneratePart,\
                        CMakeBuildPart,\
                        CMakeBuildClearPart,\
                        BuildType


__all__ = ["CMDBuilder",
           "BuildType"
           ]


class CMDBuilder:
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
        part = CMakeBuildPart(build_dir_path)
        self._cmd_list.add_part(part)

    def add_cmake_build_clear_part(self,
                                   build_dir_path: str
    ) -> None:
        part = CMakeBuildClearPart(build_dir_path)
        self._cmd_list.add_part(part)
