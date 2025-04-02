from argparse import ArgumentParser as ap


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


def main(options):
    # Call function based on choice and pass the corresponding json file path
    if options.action == 'g':
        # localimpl.generate_cmakelists(options.json)
        pass
    elif options.action == 'b':
        # localimpl.build_project(options.json)
        pass
    else:    # options.action == 'c'
        # clear
        pass


if __name__ == "__main__":
    main(_get_parser().parse_args())
