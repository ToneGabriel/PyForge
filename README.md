# PyForge

## Overview
This project is a C/C++ build automation tool powered by Python, leveraging CMake for project configuration. The project setup is customizable via a JSON configuration file.

## Requirements
- **Admin rights to install/uninstall**
- **C/C++ Compiler for your project**

## How to Use
0. Install using `pyforge-setup.exe`
1. Create an EMPTY folder where you want the project.
2. Modify the `input.JSON` configuration file to customize compiler paths and project settings. Ensure the selected compiler supports the specified settings.
3. Start PyForge with `pyforge.exe`
4. Select `Reload` to load input data if you changed it during run.
5. Select `Setup project structure` to create the base folders and files.
6. Create you project files (ex: `.h`, `.c`) using the existing folders.
    - 6.1. Write headers in `include` folder
    - 6.2. Write sources in `source` folder
    - 6.3. Write test sources in `test` folder
    - 6.4. Can create any subfolder structure.
7. Select `Generate CMakeLists` to setup the build process.
8. Select `Build Project` or `Build Project Clean` to build the project (output files are available in project `build` folder).
9. Select `Exit` to stop PyForge.

## Configuration Details

### project_settings
- **root**: Full path to your C/C++ project root folder
- **name**: Name of executable and library will be based on this
- **version**: Defines the current project version. Format `{ "major": X, "minor": Y, "patch": Z }`
- **product**: Project product type. Choose from the following:
    - **`APP`**: Standalone application (`.exe`)
    - **`LIB`**: Static library (`.a`)
    - **`DLL`**: Shared library (`.dll`)
    - **`TMP`**: Template library (`.h` only)
- **build**: Project build type. Choose from the following:
    - **`DEBUGG`**: Includes full debug information with no optimization. Used for development and debugging.
    - **`RELEASE`**: Enables maximum optimization and excludes debug information. Intended for production builds.
    - **`DBGRELEASE`**: Applies optimization while retaining debug information. Suitable for profiling.
    - **`MINRELEASE`**: Optimizes for minimal binary size without debug information. Ideal for size-sensitive deployments.
- **compile_definitions**: Define macros at compile time

### c_settings
- **compiler_path**: Full path to your C compiler. Leave empty for auto search.
- **compiler_extensions_required**: Allows compiler-specific extensions (`true`/`false`)
- **language_standard**: Number for C language standard (`11`, `17`, `23`)
- **language_standard_required**: Enforces standard compliance (`true`/`false`)

### cpp_settings
- **compiler_path**: Full path to your C++ compiler. Leave empty for auto search.
- **compiler_extensions_required**: Allows compiler-specific extensions (`true`/`false`)
- **language_standard**: Number for C language standard (`11`, `14`, `17`, `20`, `23`)
- **language_standard_required**: Enforces standard compliance (`true`/`false`)
