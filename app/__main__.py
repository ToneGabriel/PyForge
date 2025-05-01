import config
import menu
import impl


def main(json_path: str,
         zip_structure_path: str,
         cmake_bin_path: str,
         ninja_bin_path: str
) -> None:
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
    main(config.JSON_PATH,
         config.STRUCTURE_ZIP_PATH,
         config.CMAKE_BIN_PATH,
         config.NINJA_BIN_PATH
         )
