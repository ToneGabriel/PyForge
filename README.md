# BuildPY

## Overview
This project is a C/C++ build automation tool powered by Python, leveraging CMake for project configuration. The project setup is customizable via a JSON configuration file.

## Configuration Details

### project_settings
- **root**: Full path to your C/C++ project root folder
- **build**: Project type. Choose from the following
    - **`app`**: Standalone application (`.exe`)
    - **`lib`**: Static library (`.a`)
    - **`dll`**: Shared library (`.dll`)
    - **`tmp`**: Template library (`.h` only)
- **version**: Defines the current project version. Format `{ "major": X, "minor": Y, "patch": Z }`

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

### cmake_settings
- **generator**: Flag used by CMake to generate build files (`MinGW Makefiles`, `Unix Makefiles`, `Ninja` and others)
- **compile_definitions**: Define macros at compile time
- **Note**: The build system must be available on this machine in order to use the generator flag.

## How to Build
1. TODO
2. TODO

## Requirements
- **CMake** (with minimum version 3.22.1)
- **C/C++ Compiler**
- **Build System**

## Notes
- Modify the JSON configuration file to customize compiler paths and project settings.
- Ensure the selected compiler supports the specified standards.
- Adjust the CMake generator if using a different build system.
