#!/bin/bash

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

