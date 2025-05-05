from abc import ABC, abstractmethod
import subprocess
import os


class ICMDPart(ABC):
    @abstractmethod
    def get_cmd_text(self: object) -> str:
        pass


class CMDList:
    def __init__(self: object, *env_paths: str):
        self._parts: list[ICMDPart] = []
        self._env_paths: tuple[str, ...] = env_paths

    def run(self: object) -> None:
        local_env = os.environ.copy()
        local_env['PATH'] = os.pathsep.join(self._env_paths) + os.pathsep + local_env['PATH']

        for part in self._parts:
            subprocess.check_call(part.get_cmd_text(), shell=True, env=local_env)

    def add_part(self: object, part: ICMDPart) -> None:
        self._parts.append(part)
