from argparse import ArgumentParser
from menu import OptionsMenu
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


menu = OptionsMenu()
menu.set_header_text("PyForge")
menu.add_option("Setup Project Structure", impl.setup_project_structure)
menu.add_option("Build Project", impl.build_project)


def _setup_project_structure_menu_map_help() -> None:
    impl.setup_project_structure()


def _build_project_menu_map_help() -> None:
    impl.generate_cmakelists()
    impl.build_project()


def _build_project_clean_menu_map_help() -> None:
    impl.generate_cmakelists()
    impl.build_project(clean=True)


def main(json_path, zip_structure_path) -> None:
    menu.run()


if __name__ == "__main__":
    args = _get_parser().parse_args()
    main(args.json, args.structure)
