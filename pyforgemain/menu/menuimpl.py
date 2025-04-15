from rich.console import Console
from rich.prompt import Prompt
import textwrap

from .option import *


class OptionsMenu:
    def __init__(self: object):
        self._header_text = "Options Menu"
        self._count: int = 1
        self._options: dict[int, Option] = {}

    def set_header_text(
            self: object,
            text: str
    ) -> None:
        self._header_text = text

    def add_option(
            self: object,
            label: str,
            action: Callable,
            *args
    ) -> None:
        self._options[self._count] = Option(label, action, *args)
        self._count += 1

    def run(self: object) -> None:
        MAIN_CONSOLE = Console()
        menu_text = self._build_menu_text()

        while True:
            MAIN_CONSOLE.print(menu_text)

            choice_index = int(Prompt.ask("Please enter your choice", choices=[str(i) for i in range(1, self._count)]))
            selected_option = self._options[choice_index]

            # no function available at option (exit program)
            if not selected_option.is_runnable():
                MAIN_CONSOLE.print("Exiting... Goodbye!", style="yellow")
                return

            MAIN_CONSOLE.print(f"Executing: {selected_option.label}...", style="yellow")

            try:
                selected_option.run()
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
