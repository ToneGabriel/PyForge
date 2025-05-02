import os


__all__ = ["get_cmakelists_file_path",
           "get_build_dir_path",
           "get_project_include_dirs",
           "get_project_sources",
           "get_project_executable",
           "get_test_sources",
           "get_test_executable"
           ]


_MAIN_FILE_NAMES = {"main.c", "main.cpp"}
_SOURCE_EXTENSIONS = (".c", ".cpp")
_CMAKELISTS_FILE_NAME = "CMakeLists.txt"
_PROJECT_BUILD_DIR_NAME = "build"
_PROJECT_INCLUDE_DIR_NAME = "include"
_PROJECT_SOURCE_DIR_NAME = "source"
_PROJECT_TEST_DIR_NAME = "test"
_PROJECT_EXTERN_DIR_NAME = "extern"


def _get_include_dirs(dir_path: str) -> list[str]:
    ret: list[str] = []

    for current_dir_path, _, _ in os.walk(dir_path):
        relative_path = os.path.relpath(path=current_dir_path,
                                        start=os.path.dirname(dir_path)
                                        )
        ret.append(relative_path)

    return ret


def _get_sources(dir_path: str) -> str:
    ret: list[str] = []

    for current_dir_path, _, current_dir_filenames in os.walk(dir_path):
        for filename in current_dir_filenames:
            if filename.endswith(_SOURCE_EXTENSIONS) and filename not in _MAIN_FILE_NAMES:
                relative_path = os.path.relpath(path=os.path.join(current_dir_path, filename),
                                                start=os.path.dirname(dir_path)
                                                )
                ret.append(relative_path)

    return ret


def _get_executable(dir_path: str) -> str:
    for current_dir_path, _, current_dir_filenames in os.walk(dir_path):
        for filename in current_dir_filenames:
            if filename in _MAIN_FILE_NAMES:
                relative_path = os.path.relpath(path=os.path.join(current_dir_path, filename),
                                                start=os.path.dirname(dir_path)
                                                )
                return relative_path

    return ""


# ==========================================================================================================================
# ==========================================================================================================================


def get_cmakelists_file_path(project_root_path: str) -> str:
    return os.path.join(project_root_path, _CMAKELISTS_FILE_NAME)


def get_build_dir_path(project_root_path: str) -> str:
    return os.path.join(project_root_path, _PROJECT_BUILD_DIR_NAME)


def get_project_include_dirs(project_root_path: str) -> str:
    project_include_path = os.path.join(project_root_path, _PROJECT_INCLUDE_DIR_NAME)
    return _get_include_dirs(project_include_path)


def get_project_sources(project_root_path: str) -> list[str]:
    project_source_path = os.path.join(project_root_path, _PROJECT_SOURCE_DIR_NAME)
    return _get_sources(project_source_path)


def get_project_executable(project_root_path: str) -> str:
    project_source_path = os.path.join(project_root_path, _PROJECT_SOURCE_DIR_NAME)
    return _get_executable(project_source_path)


def get_test_sources(project_root_path: str) -> str:
    test_source_path = os.path.join(project_root_path, _PROJECT_TEST_DIR_NAME)
    return _get_sources(test_source_path)


def get_test_executable(project_root_path: str) -> str:
    test_source_path = os.path.join(project_root_path, _PROJECT_TEST_DIR_NAME)
    return _get_executable(test_source_path)
