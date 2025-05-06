import config
import menu
import impl


def main(json_path: str,
         zip_structure_path: str,
         cmake_bin_path: str,
         ninja_bin_path: str
) -> None:
    # initialize implementation module
    impl_state = impl.ImplementationSharedState()
    impl_state.initialize(json_path,
                          cmake_bin_path,
                          ninja_bin_path,
                          zip_structure_path
    )

    # create menu and map buttons to implementation functions
    main_menu = menu.OptionsMenu()
    main_menu.set_header_text("PyForge")
    main_menu.add_option("Reload", impl_state.reload)
    main_menu.add_option("Setup Project Structure", impl_state.setup_project_structure)
    main_menu.add_option("Generate CMakeLists", impl_state.generate_cmakelists)
    main_menu.add_option("Build Project", impl_state.build_project)
    main_menu.add_option("Build Project Clean", impl_state.build_project, True)
    main_menu.add_option("Exit", None)
    main_menu.run()


if __name__ == "__main__":
    main(config.JSON_PATH,
         config.STRUCTURE_ZIP_PATH,
         config.CMAKE_BIN_PATH,
         config.NINJA_BIN_PATH
    )
