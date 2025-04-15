from typing import Callable

class Option:
    def __init__(
            self: object,
            label: str,
            action: Callable,
            *args
            ):

        self._label: str = label
        self._action: Callable = action
        self._action_args = args

    @property
    def label(self: object) -> str:
        return self._label

    def is_runnable(self: object) -> bool:
        return self._action is not None

    def run(self: object) -> None:
        if self.is_runnable():
            return self._action(*self._action_args)
