import os
import sys


__all__ = ["CMAKE_BIN_PATH",
           "NINJA_BIN_PATH",
           "STRUCTURE_ZIP_PATH",
           "JSON_PATH"
           ]


def _get_executable_path() -> str:
    if getattr(sys, 'frozen', False):
        # if project is build into and .exe file return absolute path to it
        return sys.executable

    # if project is in dev mode return absolute path to the directory holding the __main__.py file
    # this returns path to 'app' directory
    return os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))


_ENVIRONMENT_ROOT_PATH: str = os.path.dirname(_get_executable_path())

CMAKE_BIN_PATH: str = os.path.join(_ENVIRONMENT_ROOT_PATH, "deps", "cmake", "bin")
NINJA_BIN_PATH: str = os.path.join(_ENVIRONMENT_ROOT_PATH, "deps", "ninja", "bin")
STRUCTURE_ZIP_PATH: str = os.path.join(_ENVIRONMENT_ROOT_PATH, "deps", "structure.zip")
JSON_PATH: str = os.path.join(_ENVIRONMENT_ROOT_PATH, "input.json")
