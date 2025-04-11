from abc import ABC, abstractmethod


class IGeneratorPart(ABC):
    @abstractmethod
    def generate(self: object, file) -> None:
        pass


class Generator:
    def __init__(self: object):
        self._parts: list[IGeneratorPart] = []

    def generate(self: object, file) -> None:
        for part in self._parts:
            part.generate(file)

    def ready(self: object) -> bool:
        return len(self._parts) > 0

    def reset(self: object) -> None:
        self._parts.clear()

    def add_part(self: object, part: IGeneratorPart) -> None:
        self._parts.append(part)
