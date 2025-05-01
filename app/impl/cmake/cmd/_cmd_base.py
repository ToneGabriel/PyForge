from abc import ABC, abstractmethod
import subprocess


class ICMDPart(ABC):
    @abstractmethod
    def get_cmd_text(self: object) -> str:
        pass


class CMDList:
    def __init__(self: object):
        self._parts: list[ICMDPart] = []

    def run(self: object) -> None:
        for part in self._parts:
            subprocess.check_call(part.get_cmd_text(), shell=True)

    def add_part(self: object, part: ICMDPart) -> None:
        self._parts.append(part)
