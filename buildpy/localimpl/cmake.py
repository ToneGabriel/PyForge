import os


__all__ = ["build_project", "generate_cmakelists"]


class CMakeGenerator:
    '''Description'''

    _CMAKE_MINIMUM_REQUIRED_VERSION = "3.22.1"

    def __init__(self: object, project_dir_path: str, json_data: dict):
        self._project_dir_path = project_dir_path
        self._json_data = json_data

    def generate_cmakelists() -> None:
        pass

    @property
    def build_type(self: object) -> str:
        return self._json_data["build_type"]
    
    @property
    def c_compiler_path(self: object) -> str:
        return self._json_data["c_compiler_path"]

    @property
    def c_standard(self: object) -> int:
        return self._json_data["c_standard"]

    @property
    def c_standard_required(self: object) -> bool:
        return self._json_data["c_standard_required"]
    
    @property
    def c_extensions(self: object) -> bool:
        return self._json_data["c_extensions"]

    @property
    def cpp_compiler_path(self: object) -> str:
        return self._json_data["cpp_compiler_path"]

    @property
    def cpp_standard(self: object) -> int:
        return self._json_data["cpp_standard"]

    @property
    def cpp_standard_required(self: object) -> bool:
        return self._json_data["cpp_standard_required"]

    @property
    def cpp_extensions(self: object) -> bool:
        return self._json_data["cpp_extensions"]

    @property
    def cmake_generator(self: object) -> str:
        return self._json_data["cmake_generator"]

    @property
    def cmake_compile_definitions_def(self: object) -> list[str]:
        return self._json_data["cmake_compile_definitions"]["def"]

    @property
    def cmake_compile_definitions_val(self: object) -> list[tuple[str, str]]:
        return self._json_data["cmake_compile_definitions"]["val"]

    @property
    def project_name(self: object) -> str: 
        return self._json_data["project_name"]

    @property
    def project_version_major(self: object) -> int:
        return self._json_data["project_version"]["major"]

    @property
    def project_version_minor(self: object) -> int:
        return self._json_data["project_version"]["minor"]

    @property
    def project_version_patch(self: object) -> int:
        return self._json_data["project_version"]["patch"]


# def build_project(json_path: str) -> None:
#     """
#     Configure and build a CMake project.

#     :param json_path: Path to the JSON file.
#     """

#     try:
#         # Load json file into dict
#         json_data_dict = load_and_validate_json(json_path, _EXPECTED_BUILD_JSON_STRUCTURE)

#         # Parse data
#         project_path: str       = json_data_dict["project_path"]
#         cmake_generator: str    = json_data_dict["cmake_generator"]
#         c_compiler_path: str    = json_data_dict["c_compiler_path"]
#         cpp_compiler_path: str  = json_data_dict["cpp_compiler_path"]

#         # Check project path
#         if not os.path.exists(project_path):
#             print("Project path does not exist!")
#             return
#         else:
#             # Navigate to the project directory
#             os.chdir(project_path)

#             # Run CMake to configure the project build
#             if not c_compiler_path or not cpp_compiler_path:
#                 _run_command(f"cmake -G \"{cmake_generator}\" -B build")
#             else:
#                 _run_command(f"cmake -G \"{cmake_generator}\"               \
#                              -DCMAKE_C_COMPILER=\"{c_compiler_path}\"       \
#                              -DCMAKE_CXX_COMPILER=\"{cpp_compiler_path}\"   \
#                              -B build")

#             # Build the project
#             _run_command("cmake --build build")
#     except Exception as e:
#         print(e)


# def _list_folder_contents(directory, indent=0):
#     try:
#         with os.scandir(directory) as entries:
#             for entry in entries:
#                 if entry.is_file():
#                     name, ext = os.path.splitext(entry.name)
#                     print("  " * indent + f"File: {name} (Extension: {ext})")
#                 elif entry.is_dir():
#                     print("  " * indent + f"Folder: {entry.name}")
#                     _list_folder_contents(entry.path, indent + 1)
#                 else:
#                     print("  " * indent + f"Unknown: {entry.name}")
#     except PermissionError:
#         print("  " * indent + "[Permission Denied]")


def _adapt_to_cmake_bool(value: bool) -> str:
    return "ON" if value else "OFF"


def _write_cmake_minimum_required_version(file, cmake_minimum_required_version: str):
    file.write( f"cmake_minimum_required(VERSION "
                f"{cmake_minimum_required_version} "
                f"FATAL_ERROR)\n"
                )
    file.write( f"\n")


def _write_project(file, project_name: str, project_version: dict):
    file.write( f"# Project Specifications\n")
    file.write( f"project("
                f"{project_name} "
                f"VERSION "
                f"{project_version['major']}."
                f"{project_version['minor']}."
                f"{project_version['patch']} "
                f"LANGUAGES C CXX)\n"
                )
    file.write( f"\n")


def _write_language_specifications(file,
                                   c_standard: int, c_standard_required: bool, c_extensions: bool,
                                   cpp_standard: int, cpp_standard_required: bool, cpp_extensions: bool):
    file.write( f"# Language Specifications\n")
    file.write( f"set(CMAKE_C_STANDARD {c_standard})\n"
                f"set(CMAKE_C_STANDARD_REQUIRED {_adapt_to_cmake_bool(c_standard_required)})\n"
                f"set(CMAKE_C_EXTENSIONS {_adapt_to_cmake_bool(c_extensions)})\n"

                f"set(CMAKE_cpp_standard {cpp_standard})\n"
                f"set(CMAKE_cpp_standard_REQUIRED {_adapt_to_cmake_bool(cpp_standard_required)})\n"
                f"set(CMAKE_cpp_extensions {_adapt_to_cmake_bool(cpp_extensions)})\n"
                )
    file.write( f"\n")


def _write_work_variables(file):
    file.write( f"# Work Variables\n")
    file.write( f"set(LIBRARY_NAME \"ProjectLibrary\")\n"
                f"set(EXECUTABLE_NAME \"ProjectExecutable\")\n"
                f"set(CURRENT_DIRECTORY \"./\")\n"
               )
    file.write( f"\n")


def _write_subdirectories(file, code_directory: str, app_directory: str):
    file.write( f"# CMakeLists subdirectory config\n")
    file.write( f"add_subdirectory({code_directory})\n"
                f"add_subdirectory({app_directory})\n"
               )
    file.write( f"\n")


# def generate_cmakelists(json_path: str) -> None:

#     try:
#         json_data_dict = load_and_validate_json(json_path, _EXPECTED_GENERATOR_JSON_STRUCTURE)

#         cmake_minimum_required_version: dict    = json_data_dict["cmake_minimum_required_version"]
        
#         project_path: str                       = json_data_dict["project_path"]
#         project_name: str                       = json_data_dict["project_name"]
#         project_version: dict                   = json_data_dict["project_version"]
        
#         c_standard: int                         = json_data_dict["c_standard"]
#         c_standard_required: bool               = json_data_dict["c_standard_required"]
#         c_extensions: bool                      = json_data_dict["c_extensions"]
        
#         cpp_standard: int                       = json_data_dict["cpp_standard"]
#         cpp_standard_required: bool             = json_data_dict["cpp_standard_required"]
#         cpp_extensions: bool                    = json_data_dict["cpp_extensions"]
        
#         app_directory: str                      = json_data_dict["app_directory"]
#         code_directory: str                     = json_data_dict["code_directory"]

#         with open(os.path.join(project_path, "CMakeLists.txt"), "w") as cmake_root_file:
#             _write_cmake_minimum_required_version(cmake_root_file, _CMAKE_MINIMUM_REQUIRED_VERSION)
#             _write_project(cmake_root_file, project_name, project_version)
#             _write_language_specifications(cmake_root_file,
#                                            c_standard, c_standard_required, c_extensions,
#                                            cpp_standard, cpp_standard_required, cpp_extensions)
#             _write_work_variables(cmake_root_file)
#             _write_subdirectories(cmake_root_file, code_directory, app_directory)

#     except Exception as e:
#         print(e)
    

