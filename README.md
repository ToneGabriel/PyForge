# BuildPY

## Overview
This project is a C/C++ build automation tool powered by Python, leveraging CMake for project configuration. The project setup is customizable via a JSON configuration file.

## Configuration Details

### build_type
- **Application**: `app`
- **Static Lib**:  `lib`
- **Shared Lib**:  `dll`
- **Template Lib**: `tmp`

### c_compiler_path
- **No C compiler**: `none`
- **Automatically detected**: `auto`
- **User defined**: `full/path/to/compiler`

### c_standard
- **Number for C language standard**: `11`, `17`, `23`

### c_standard_required
- **Enforces standard compliance**: `true`/`false`

### c_extensions
- **Allows compiler-specific extensions**: `true`/`false`

### cxx_compiler_path
- **No C++ compiler**: `none`
- **Automatically detected**: `auto`
- **User defined**: `full/path/to/compiler`

### cxx_standard
- **Number for C++ language standard**: `11`, `14`, `17`, `20`, `23`

### cxx_standard_required
- **Enforces standard compliance**: `true`/`false`

### cxx_extensions
- **Allows compiler-specific extensions**: `true`/`false`

### cmake_generator
- **Examples**: `MinGW Makefiles`, `Unix Makefiles`, `Ninja`
- **Note**: The build system must be available on this machine in order to use the generator flag.

### cmake_minimum_required_version
- **Format**: `{ "major": X, "minor": Y, "patch": Z }`
- **Note**: The build will fail if the installed CMake version is lower than the specified requirement.

### project_name
- **Defines the project name**: `your_project_name`

### project_version
- **Format**: `{ "major": X, "minor": Y, "patch": Z }`
- **Defines the current project version**

## How to Build
1. TODO
2. TODO

## Requirements
- **CMake** (with minimum version as defined in the JSON configuration)
- **C/C++ Compiler** (as defined in the JSON configuration)
- **Build System** (ex: `Ninja`)

## Notes
- Modify the JSON configuration file to customize compiler paths and project settings.
- Ensure the selected compiler supports the specified standards.
- Adjust the CMake generator if using a different build system.
