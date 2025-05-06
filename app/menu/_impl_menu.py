from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from typing import Callable


__all__ = ["OptionsMenu"]


class _Option:
    def __init__(
            self,
            label: str,
            action: Callable,
            *args
    ):
        self._label: str = label
        self._action: Callable = action
        self._action_args = args

    @property
    def label(self) -> str:
        return self._label

    def empty(self) -> bool:
        return self._action is None

    def run(self) -> None:
        if not self.empty():
            return self._action(*self._action_args)


# ==========================================================================================================================
# ==========================================================================================================================


class OptionsMenu:
    def __init__(self):
        self._header_text = "Main Menu"     # default header text
        self._count: int = 1
        self._options: dict[int, _Option] = {}

    def set_header_text(
            self,
            text: str
    ) -> None:
        self._header_text = text

    def add_option(
            self,
            label: str,
            action: Callable,
            *args
    ) -> None:
        self._options[self._count] = _Option(label, action, *args)
        self._count += 1

    def run(self) -> None:
        MAIN_CONSOLE = Console()
        MENU_TABLE = self._build_menu_table()

        while True:
            MAIN_CONSOLE.clear()
            MAIN_CONSOLE.print(MENU_TABLE)

            choice_index = int(Prompt.ask("Please enter your choice", choices=[str(i) for i in range(1, self._count)]))
            selected_option = self._options[choice_index]

            # no function available at option (exit program)
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

            Prompt.ask("\nPress Enter to continue", default="", show_default=False)

    def _build_menu_table(self) -> Table:
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
