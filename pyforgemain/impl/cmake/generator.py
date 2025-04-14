from abc import ABC, abstractmethod


class IGeneratorPart(ABC):
    @abstractmethod
    def run(self: object, file) -> None:
        pass


class Generator:
    def __init__(self: object):
        self._parts: list[IGeneratorPart] = []

    def run(self: object, file) -> None:
        for part in self._parts:
            part.run(file)

    def add_part(self: object, part: IGeneratorPart) -> None:
        self._parts.append(part)
