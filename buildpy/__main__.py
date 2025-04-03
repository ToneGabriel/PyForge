from argparse import ArgumentParser as ap
import localimpl


def _get_parser() -> ap:
    parser = ap(description="Arguments to generate and/or build a C/C++ project with CMake.",
                conflict_handler="resolve"
                )

    parser.add_argument("--action",
                        type=str,
                        required=True,
                        choices=['g', 'b', 'c'],
                        help="Specify the action: 'g' to generate, 'b' to build, 'c' to clear."
                        )

    parser.add_argument("--project",
                        type=str,
                        required=True,
                        help="Path to the project directory"
                        )

    parser.add_argument("--json",
                        type=str,
                        required=True,
                        help="Path to the JSON file"
                        )

    return parser


if __name__ == "__main__":
    options = _get_parser().parse_args()
    localimpl.main(options.action, options.project, options.json)
