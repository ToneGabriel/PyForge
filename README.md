# PyForge

## Overview
This project is a C/C++ build automation tool powered by Python, leveraging CMake for project configuration. The project setup is customizable via a JSON configuration file.

## Requirements
- **Admin rights to install/uninstall**
- **C/C++ Compiler for your project**

## How to Use
0. Install using `pyforge-setup.exe`
1. Modify the `manifest.JSON` configuration file to customize compiler paths and project settings. Ensure the selected compiler supports the specified settings.
2. Start PyForge with `pyforge.exe`
3. Select `Reload` to load manifest data if you changed it during run.
4. Create you project files (ex: `.h`, `.c`) using the existing folders.
    - 4.1. Can create any subfolder structure.
    - 4.2. Can modify `manifest.json` to ignore folders.
5. Select `Generate CMakeLists` to setup the build process.
6. Select `Build Project` or `Build Project Clean` to build the project (output files are available in project `build` folder).
7. Select `Exit` to stop PyForge.

## Configuration Details

### project_settings
- **root**: Full path to your C/C++ project root folder
- **ignored**: List of folder names to be ignored
- **name**: Name of executable and library will be based on this
- **version**: Defines the current project version. Format `{ "major": X, "minor": Y, "patch": Z }`
- **language**: Language used: `C` or `CPP`
- **product**: Project product type. Choose from the following:
    - **`APP`**: Standalone application (`.exe`)
    - **`LIB`**: Static library (`.a`)
    - **`DLL`**: Shared library (`.dll`)
    - **`TST`**: Test executable (`.exe`). Integrates `googletest` or `unity` based on language
- **build**: Project build type. Choose from the following:
    - **`DEBUGG`**: Includes full debug information with no optimization. Used for development and debugging
    - **`RELEASE`**: Enables maximum optimization and excludes debug information. Intended for production builds
    - **`DBGRELEASE`**: Applies optimization while retaining debug information. Suitable for profiling
    - **`MINRELEASE`**: Optimizes for minimal binary size without debug information. Ideal for size-sensitive deployments
- **compile_definitions**: Define macros at compile time. First parameter is the macro name. The second parameter is:
    - **None**: #define MACRO
    - **Int_Value**: #define MACRO `int_value`
    - **String**: #define MACRO `"string"`

### compiler_settings
- **compiler_path**: Full path to your C/C++ compiler. Leave empty for auto search
- **compiler_extensions_required**: Allows compiler-specific extensions (`true`/`false`)
- **language_standard**: Number for C language standard (`11`, `17`, `23`) OR C++ language standard (`11`, `14`, `17`, `20`, `23`)
- **language_standard_required**: Enforces standard compliance (`true`/`false`)
