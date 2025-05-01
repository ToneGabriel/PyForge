from ._cmd_base import CMDList
from ._cmd_parts import CMakeGeneratePart,\
                        CMakeBuildPart,\
                        CMakeBuildType,\
                        CMakeGeneratorFlag


__all__ = ["CMDBuilder",
           "CMakeBuildType",
           "CMakeGeneratorFlag"
           ]


class CMDBuilder:
    def __init__(self: object):
        self.reset_cmd_product()

    @property
    def cmd_product(self: object) -> CMDList:
        return self._cmd_list

    def reset_cmd_product(self: object) -> None:
        self._cmd_list = CMDList()

    def add_cmake_generate_part(self: object,
                                cmakelists_root_dir_path: str,
                                cmake_generator_flag: CMakeGeneratorFlag,
                                build_type: CMakeBuildType,
                                build_dir_path: str,
                                c_compiler_path: str,
                                cpp_compiler_path: str
    ) -> None:
        part = CMakeGeneratePart(cmakelists_root_dir_path,
                                 cmake_generator_flag,
                                 build_type,
                                 build_dir_path,
                                 c_compiler_path,
                                 cpp_compiler_path
                                 )
        self._cmd_list.add_part(part)

    def add_cmake_build_part(self: object,
                             build_dir_path: str,
                             clean: bool
    ) -> None:
        part = CMakeBuildPart(build_dir_path,
                              clean
                              )
        self._cmd_list.add_part(part)
