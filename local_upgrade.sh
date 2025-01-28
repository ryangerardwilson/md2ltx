#!/bin/bash

update_help_string() {
    local help_lib_file="string_lib.py"
    local readme_file="README.md"

    # Use awk to replace everything between:
    #   help_string = r"""
    # and
    #   """
    # with the contents of README.md
    awk -v rfile="$readme_file" '
    BEGIN {
        # Read the entire README.md into memory
        while ((getline line < rfile) > 0) {
            readme = readme line "\n"
        }
        close(rfile)
    }
    {
        # If we see the start of the help_string block,
        # print it and then print the README content.
        if ($0 ~ /^help_string = r"""/) {
            print "help_string = r\"\"\""
            print readme
            print "\"\"\""
            skip=1
            next
        }
        # Skip lines inside the old triple-quoted block
        if (skip == 1) {
            if ($0 ~ /^\"\"\"/) {
                skip=0
            }
            next
        }
        # Print lines outside the replaced block
        print
    }
    ' "$help_lib_file" > "${help_lib_file}.tmp" && mv "${help_lib_file}.tmp" "$help_lib_file"

    echo "string_lib.py updated with latest README.md content."
}

echo "Updating help_string in string_lib.py from README.md..."
update_help_string

rebuild_package() {
    python3 -m pip install --upgrade build
    rm -rf dist/*
    python3 -m build
}

uninstall_local_library() {
    local package_name=$(grep -E '^name\s*=\s*".*"' pyproject.toml | sed -E 's/name\s*=\s*"(.*)"/\1/')
    pip3 uninstall -y "$package_name"
}

install_local_version() {
    pip3 install .
}

echo "Rebuilding package..."
rebuild_package

echo "Uninstalling local library..."
uninstall_local_library

echo "Installing local version..."
install_local_version

echo "The local version of the package has been reinstalled."

