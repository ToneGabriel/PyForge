from argparse import ArgumentParser
from typing import Callable
from rich.console import Console
from rich.prompt import Prompt

import textwrap

import impl


def _get_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Arguments to generate and/or build a C/C++ project with CMake.",
                            conflict_handler="resolve"
                            )

    parser.add_argument("--json",
                        type=str,
                        required=True,
                        help="Path to the setup JSON file"
                        )
    
    parser.add_argument("--structure",
                        type=str,
                        required=True,
                        help="Path to the project structure .zip file"
                        )

    return parser


class MenuOption:
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


def _setup_project_structure_menu_map_help() -> None:
    impl.setup_project_structure()


def _build_project_menu_map_help() -> None:
    impl.generate_cmakelists()
    impl.build_project()


def _build_project_clean_menu_map_help() -> None:
    impl.generate_cmakelists()
    impl.build_project(clean=True)


_MENU_OPTIONS = {
    "1": MenuOption(
            label="Setup Project Structure",
            action=_setup_project_structure_menu_map_help),

    "2": MenuOption(
            label="Build Project",
            action=_build_project_menu_map_help),

    "3": MenuOption(
            label="Build Project Clean",
            action=_build_project_clean_menu_map_help),

    "4": MenuOption(
            label="Exit",
            action=None),
}


def _build_menu_text_and_keys() -> tuple[str, list[str]]:
    header = textwrap.dedent(
    '''
    ===============================================
                        PyForge
    ===============================================
    Select an option:
    '''
    )

    body = ""
    keys = []
    for key, option in _MENU_OPTIONS.items():
        body += f"{key}. {option.label}\n"
        keys.append(key)

    return (f"{header}\n{body}", keys)


def main(json_path, zip_structure_path) -> None:
    MAIN_CONSOLE = Console()
    (menu_text, option_keys) = _build_menu_text_and_keys()

    while True:
        MAIN_CONSOLE.print(menu_text)

        option = _MENU_OPTIONS[Prompt.ask("Please enter your choice", choices=option_keys)]

        # no function available at option (exit program)
        if not option.action:
            MAIN_CONSOLE.print("Exiting... Goodbye!", style="yellow")
            return

        # try action
        try:
            impl.initialize(json_path, zip_structure_path)

            MAIN_CONSOLE.print(f"Executing: {option.label}...", style="yellow")
            option.action()
        except Exception as e:
            MAIN_CONSOLE.print(f"Operation failed: {e}", style="red")
        else:
            MAIN_CONSOLE.print("Operation successful!", style="green")

        if Prompt.ask("Continue?", choices=["y", "n"]) == "n":
            MAIN_CONSOLE.print("Exiting... Goodbye!", style="yellow")
            return


if __name__ == "__main__":
    args = _get_parser().parse_args()
    main(args.json, args.structure)
