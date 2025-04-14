from typing import Callable
from rich.console import Console
from rich.prompt import Prompt
import textwrap


class _Option:
    def __init__(
            self: object,
            label: str,
            action: Callable=None
            ):

        self._label: str = label
        self._action: Callable = action

    @property
    def label(self: object) -> str:
        return self._label

    @property
    def action(self: object) -> Callable:
        return self._action


class OptionsMenu:
    def __init__(self: object):
        self._header_text = ""
        self._count: int = 1
        self._options: dict[int, _Option] = {}

    def set_header_text(
            self: object,
            text: str
    ) -> None:
        self._header_text = text

    def add_option(
            self: object,
            label: str,
            action: Callable
    ) -> None:
        self._options[self._count] = _Option(label, action)
        self._count += 1

    def run(self: object) -> None:
        self.add_option("Exit", None)
        MAIN_CONSOLE = Console()
        menu_text = self._build_menu_text()

        while True:
            MAIN_CONSOLE.print(menu_text)

            index = int(Prompt.ask("Please enter your choice", choices=[str(i) for i in range(1, self._count)]))
            selected_option = self._options[index]

            # no function available at option (exit program)
            if not selected_option.action:
                MAIN_CONSOLE.print("Exiting... Goodbye!", style="yellow")
                return

            try:
                MAIN_CONSOLE.print(f"Executing: {selected_option.label}...", style="yellow")
                selected_option.action()
            except Exception as e:
                MAIN_CONSOLE.print(f"Operation failed: {e}", style="red")
            else:
                MAIN_CONSOLE.print("Operation successful!", style="green")

    def _build_menu_text(self: object) -> str:
        header = textwrap.dedent(
        f'''
        ===============================================
        {self._header_text}
        ===============================================
        Select an option:
        '''
        )

        body = ""
        for key, option in self._options.items():
            body += f"{key}. {option.label}\n"

        return f"{header}\n{body}"