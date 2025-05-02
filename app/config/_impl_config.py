import os
import sys


__all__ = ["PROJECT_ROOT_PATH",
           "CMAKE_BIN_PATH",
           "NINJA_BIN_PATH",
           "STRUCTURE_ZIP_PATH",
           "JSON_PATH"
           ]


def _get_app_root() -> str:
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)

    return os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))


PROJECT_ROOT_PATH: str = os.path.dirname(_get_app_root())
CMAKE_BIN_PATH: str = os.path.join(PROJECT_ROOT_PATH, "deps", "cmake", "bin")
NINJA_BIN_PATH: str = os.path.join(PROJECT_ROOT_PATH, "deps", "ninja", "bin")
STRUCTURE_ZIP_PATH: str = os.path.join(PROJECT_ROOT_PATH, "deps", "structure.zip")
JSON_PATH: str = os.path.join(PROJECT_ROOT_PATH, "input.json")
