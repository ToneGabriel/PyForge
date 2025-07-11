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
3. Select `Reload Manifest` to load manifest data if you changed it during run.
4. Create you project files. Can create any subfolder structure.
5. Select `Configure Project` to setup the build process (if project files have changed).
6. Select `Build Project` to build the project (output files are available in project `build` folder).
7. Select `Exit` to stop PyForge.

## Configuration Details

### path_settings
- **root_dir**: Full path to your C/C++ project root folder
- **include_dirs**: List of relative paths to include folders
- **source_dirs_ignore**: List of folder names to be ignored when searching local source files
- **imports**: External dependencies (static and shared libraries):
    - **`static`**: Declare a list of paths (leave empty if none):
        - **`string param 1`**: Relative path to the actual library (.lib, .a)
        - **`string param 2`**: Relative path to the public API for the library (include)
    - **`shared`**: Declare a list of paths (leave empty if none):
        - **`string param 1`**: Relative path to the actual library (.dll)
        - **`string param 2`**: Relative path to the implementation library if any (.lib, .a), else leave empty
        - **`string param 3`**: Relative path to the public API for the library (include)

### project_settings
- **name**: Name of executable and library will be based on this
- **version**: Defines the current project version. Format `{ "major": X, "minor": Y, "patch": Z }`
- **language**: Language used: `C` or `CPP`
- **product**: Project product type. Choose from the following:
    - **`EXE`**: Standalone application (`.exe`)
    - **`LIB`**: Static library (`.a`)
    - **`DLL`**: Shared library (`.dll`)
- **build**: Project build type. Choose from the following:
    - **`DEBUGG`**: Includes full debug information with no optimization. Used for development and debugging
    - **`RELEASE`**: Enables maximum optimization and excludes debug information. Intended for production builds
    - **`DBGRELEASE`**: Applies optimization while retaining debug information. Suitable for profiling
    - **`MINRELEASE`**: Optimizes for minimal binary size without debug information. Ideal for size-sensitive deployments
- **compile_definitions**: Define a list of macros at compile time:
    - **`string param 1`**: Macro name.
    - **`string param 2`**: Macro value:
        - *`Empty`*: #define MACRO
        - *`Int_Value`*: #define MACRO `int_value`
        - *`String`*: #define MACRO `"string"`

### compiler_settings
- **compiler_path**: Full path to your C/C++ compiler. Leave empty for auto search
- **compiler_extensions_required**: Allows compiler-specific extensions (`true`/`false`)
- **language_standard**: Number for C language standard (`11`, `17`, `23`) OR C++ language standard (`11`, `14`, `17`, `20`, `23`)
- **language_standard_required**: Enforces standard compliance (`true`/`false`)
