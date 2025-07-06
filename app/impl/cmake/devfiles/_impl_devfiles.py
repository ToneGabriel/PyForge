import os


__all__ = ["get_cmakelists_file_path",
           "get_build_dir_path",
           "get_project_source_files"
           ]


_SOURCE_EXTENSIONS = (".c", ".cpp", ".cxx", ".cc")
_CMAKELISTS_FILE_NAME = "CMakeLists.txt"
_PROJECT_BUILD_DIR_NAME = "build"


# ==========================================================================================================================
# ==========================================================================================================================


def get_cmakelists_file_path(project_root_path: str) -> str:
    """
    :param project_root_path: full path to the project
    :returns str: full path to the CMakelists.txt file
    """
    return os.path.join(project_root_path, _CMAKELISTS_FILE_NAME).replace("\\", "/")


def get_build_dir_path(project_root_path: str) -> str:
    """
    :param project_root_path: full path to the project
    :returns str: full path to the build directory
    """
    return os.path.join(project_root_path, _PROJECT_BUILD_DIR_NAME).replace("\\", "/")


def get_project_source_files(dir_path: str, ignored_dirs: list[str]) -> list[str]:
    """
    Walks a directory tree, skipping ignored directories.

    :param dir_path: root directory of the tree
    :param ignored_dirs: name of the directories to ignore (recursive)
    :returns list[str]: A list of relative paths to .c/.cpp files (excluding main files).
    """

    src_files = []

    for current_dir_path, current_dir_dirnames, current_dir_filenames in os.walk(dir_path):
        # Modify dirs in-place to skip ignored ones
        current_dir_dirnames[:] = [dir for dir in current_dir_dirnames if dir not in ignored_dirs]

        for filename in current_dir_filenames:
            if filename.endswith(_SOURCE_EXTENSIONS):
                relative_path = os.path.relpath(path=os.path.join(current_dir_path, filename), start=dir_path).replace("\\", "/")
                src_files.append(relative_path)
            # ignore any other files

    return src_files
