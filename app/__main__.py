import config
import menu
import impl


def main(json_path: str,
         cmake_bin_path: str,
         ninja_bin_path: str
) -> None:
    # initialize implementation module
    impl_state = impl.ImplementationSharedState()
    impl_state.initialize(json_path,
                          cmake_bin_path,
                          ninja_bin_path
    )

    # create menu and map buttons to implementation functions
    main_menu = menu.OptionsMenu()
    main_menu.set_header_text("PyForge")
    main_menu.add_option("Reload Manifest", impl_state.reload)
    main_menu.add_option("Configure Project", impl_state.configure_project)
    main_menu.add_option("Build Project", impl_state.build_project)
    main_menu.add_option("Exit", None)
    main_menu.run()


if __name__ == "__main__":
    main(config.JSON_MANIFEST_PATH,
         config.CMAKE_BIN_PATH,
         config.NINJA_BIN_PATH
    )
