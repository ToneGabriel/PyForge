from argparse import ArgumentParser

import menu
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


def main(json_path, zip_structure_path) -> None:
    main_menu = menu.OptionsMenu()

    main_menu.set_header_text("PyForge")
    main_menu.add_option("Initialize", impl.initialize, json_path, zip_structure_path)
    main_menu.add_option("Setup Project Structure", impl.setup_project_structure)
    main_menu.add_option("Generate CMakeLists", impl.generate_cmakelists)
    main_menu.add_option("Build Project", impl.build_project)
    main_menu.add_option("Build Project Clean", impl.build_project, True)
    main_menu.add_option("Exit", None)
    main_menu.run()


if __name__ == "__main__":
    args = _get_parser().parse_args()
    main(args.json, args.structure)
