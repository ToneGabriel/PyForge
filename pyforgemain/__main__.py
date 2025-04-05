from argparse import ArgumentParser as ap
from impl import main as run_main_impl


def _get_parser() -> ap:
    parser = ap(description="Arguments to generate and/or build a C/C++ project with CMake.",
                conflict_handler="resolve"
                )

    parser.add_argument("--json",
                        type=str,
                        required=True,
                        help="Path to the setup JSON file"
                        )

    return parser


if __name__ == "__main__":
    options = _get_parser().parse_args()
    run_main_impl(options.json)
