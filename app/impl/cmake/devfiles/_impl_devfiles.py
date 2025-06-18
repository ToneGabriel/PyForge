import os


__all__ = ["get_cmakelists_file_path",
           "get_build_dir_path",
           "get_project_files_and_dirs"
           ]


_MAIN_FILE_NAMES = ("main.c", "main.cpp")
_SOURCE_EXTENSIONS = (".c", ".cpp")
_HEADER_EXTENSIONS = (".h", ".hpp")
_CMAKELISTS_FILE_NAME = "CMakeLists.txt"
_PROJECT_BUILD_DIR_NAME = "build"


# ==========================================================================================================================
# ==========================================================================================================================


def get_cmakelists_file_path(project_root_path: str) -> str:
    return os.path.join(project_root_path, _CMAKELISTS_FILE_NAME)


def get_build_dir_path(project_root_path: str) -> str:
    return os.path.join(project_root_path, _PROJECT_BUILD_DIR_NAME)


def get_project_files_and_dirs(dir_path: str, ignored_dirs: list[str]) -> tuple[list[str], list[str], str | None]:
    """
    Walks a directory tree, skipping ignored directories.

    Returns:
        - A list of relative directories containing .h/.hpp files.
        - A list of relative paths to .c/.cpp files (excluding main files).
        - A relative path to the first main.c/main.cpp file found, or None.
    """

    inc_dirs = set()
    src_files = list()
    main_file = None

    for current_dir_path, current_dir_dirnames, current_dir_filenames in os.walk(dir_path):
        # Modify dirs in-place to skip ignored ones
        current_dir_dirnames[:] = [dir for dir in current_dir_dirnames if dir not in ignored_dirs]

        for filename in current_dir_filenames:
            if filename.endswith(_SOURCE_EXTENSIONS):
                relative_path = os.path.relpath(path=os.path.join(current_dir_path, filename),
                                                start=dir_path)
                if filename not in _MAIN_FILE_NAMES:
                    # manage sources
                    src_files.append(relative_path)
                else:
                    # manage main files
                    if main_file is None:
                        main_file = relative_path
                    else:
                        raise RuntimeError(f"More than one main file found: {main_file} AND {relative_path}")
            elif filename.endswith(_HEADER_EXTENSIONS):
                # manage headers
                relative_path = os.path.relpath(path=current_dir_path,
                                                start=dir_path)
                inc_dirs.add(relative_path)
            else:
                # ignore any other files
                pass

    return list(inc_dirs), src_files, main_file
