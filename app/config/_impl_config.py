import os
import sys


__all__ = ["CMAKE_BIN_PATH",
           "NINJA_BIN_PATH",
           "JSON_PATH"
           ]


def _get_executable_path() -> str:
    """
    :returns str: full path to project executable
    """

    if getattr(sys, 'frozen', False):
        # if project is build into and .exe file return absolute path to it
        return sys.executable

    # if project is in dev mode return absolute path to the directory holding the __main__.py file
    # this returns path to 'app' directory
    return os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))


# Parent directory of the executable (the root of the project distribution: all paths are relative to this)
_ENVIRONMENT_ROOT_PATH: str = os.path.dirname(_get_executable_path())

# Relative path to cmake binary dependency
CMAKE_BIN_PATH: str = os.path.join(_ENVIRONMENT_ROOT_PATH, "deps", "cmake", "bin")

# Relative path to ninja binary dependency
NINJA_BIN_PATH: str = os.path.join(_ENVIRONMENT_ROOT_PATH, "deps", "ninja", "bin")

# Relative path to json manifest for user settings
JSON_PATH: str = os.path.join(_ENVIRONMENT_ROOT_PATH, "manifest.json")
