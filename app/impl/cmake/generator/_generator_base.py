from abc import ABC, abstractmethod
from typing import override


# Implemented the CMakelists.txt text generator using the builder pattern


class IGeneratorPart(ABC):
    """
    Interface for text generator part
    """
    @abstractmethod
    def run(self, file) -> None:
        pass


class Generator:
    """
    Uses a list of IGeneratorPart to write sequentially text data in a file
    """

    def __init__(self):
        self._parts: list[IGeneratorPart] = []

    def run(self, file) -> None:
        for part in self._parts:
            part.run(file)

    def add_part(self, part: IGeneratorPart) -> None:
        self._parts.append(part)
