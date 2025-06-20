from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from typing import Callable
from functools import partial


__all__ = ["OptionsMenu"]


class _Option:
    def __init__(
            self,
            label: str,
            action: Callable | None,
            *args
    ):
        """
        :param label: Option text
        :param action: Option function
        :param args: Option function bound arguments
        :raises TypeError: if action not callable. (Can be None)
        """
        self._label: str = label
        self._action: partial = partial(action, *args) if action else None

    @property
    def label(self) -> str:
        return self._label

    def empty(self) -> bool:
        return self._action is None

    def run(self) -> None:
        if self.empty():
            return

        self._action()


# ==========================================================================================================================
# ==========================================================================================================================


class OptionsMenu:
    """
    CMD menu with options from 1 to N where each option has a function bound to it
    """

    def __init__(self):
        self._header_text = "Main Menu"     # default header text
        self._count: int = 1
        self._options: dict[int, _Option] = {}

    def set_header_text(self, text: str) -> None:
        """
        :param text: Text to be shown as table title
        """
        self._header_text = text

    def add_option(self, label: str, action: Callable, *args) -> None:
        """
        Add a new option to the table.

        :param label: Option text
        :param action: Option function
        :param args: Option function bound arguments
        """
        self._options[self._count] = _Option(label, action, *args)
        self._count += 1

    def run(self) -> None:
        """
        Start menu display and run functions safely
        """

        MAIN_CONSOLE = Console()
        MENU_TABLE = self._build_menu_table()

        while True:
            MAIN_CONSOLE.clear()
            MAIN_CONSOLE.print(MENU_TABLE)

            choice_index = int(Prompt.ask("Please enter your choice", choices=[str(i) for i in range(1, self._count)]))
            selected_option = self._options[choice_index]

            # no function available at option (exit loop)
            if selected_option.empty():
                MAIN_CONSOLE.print("Exiting... Goodbye!", style="yellow")
                return

            MAIN_CONSOLE.print(f"Executing: {selected_option.label}...", style="yellow")

            try:
                selected_option.run()
            except Exception as e:
                MAIN_CONSOLE.print(f"Operation failed: {e}", style="red")
            else:
                MAIN_CONSOLE.print("Operation successful!", style="green")

            # make a pause to see the result before showing the table again
            Prompt.ask("\nPress Enter to continue", default="", show_default=False)

    def _build_menu_table(self) -> Table:
        """
        Create table border and options text
        """

        table = Table(
            title=self._header_text,
            title_style="bold magenta",
            title_justify="center",
            show_edge=True,
            pad_edge=True
        )

        table.add_column("Option", justify="center", style="cyan", header_style="bold white")
        table.add_column("Description", justify="left", style="white", header_style="bold green")

        for key, option in self._options.items():
            table.add_row(str(key), option.label)

        return table
