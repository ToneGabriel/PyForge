from argparse import ArgumentParser as ap
import textwrap
import localimpl


def _print_menu() -> None:
    print(textwrap.dedent(
    '''
    ===============================================
                        PyForge
    ===============================================
    Select an option:
    1. Generate CMakeLists
    2. Clear CMakeLists
    3. Build Project
    4. Exit"
    '''
    ))


def _get_parser() -> ap:
    parser = ap(description="Arguments to generate and/or build a C/C++ project with CMake.",
                conflict_handler="resolve"
                )

    parser.add_argument("--project",
                        type=str,
                        required=True,
                        help="Path to the project directory"
                        )

    parser.add_argument("--json",
                        type=str,
                        required=True,
                        help="Path to the setup JSON file"
                        )

    return parser


def main(options):

    # TODO
    options.project
    options.json

    while True:
        _print_menu()

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            print("Generating CMakeLists...")
        elif choice == "2":
            print("Clearing CMakeLists...")
        elif choice == "3":
            print("Building Project...")
        elif choice == "4":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main(_get_parser().parse_args())
