#!/bin/bash

# Step 0: Update help_string in help_lib.py with the latest content from README.md
update_help_string() {
  local help_lib_file="src/md2ltx/lib/string_lib.py"
  local readme_file="README.md"

  # Entire AWK script in single quotes
  awk -v rfile="$readme_file" '
BEGIN {
    while ((getline line < rfile) > 0) {
        readme = readme line "\n"
    }
    close(rfile)
}
{
    if ($0 == "help_string = r\"\"\"") {
        print "help_string = r\"\"\""
        print readme
        print "\"\"\""
        skip=1
        next
    }
    if (skip == 1) {
        if ($0 == "\"\"\"") {
            skip=0
        }
        next
    }
    print
}
' "$help_lib_file" > "${help_lib_file}.tmp" && mv "${help_lib_file}.tmp" "$help_lib_file"

  echo "string_lib.py updated with latest README.md content."
}



# Step 1: Increment the version number in pyproject.toml and setup.cfg
increment_version() {
    local version_file="pyproject.toml"
    local setup_file="setup.cfg"

    # Extract the current version from pyproject.toml
    local version_line=$(grep -E 'version = "[0-9]+\.[0-9]+\.[0-9]+"' "$version_file")
    local current_version=$(echo "$version_line" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')

    # Increment the patch version
    IFS='.' read -r -a version_parts <<< "$current_version"
    version_parts[2]=$((version_parts[2] + 1))
    local new_version="${version_parts[0]}.${version_parts[1]}.${version_parts[2]}"

    # Update the version in pyproject.toml
    sed -i "s/version = \"$current_version\"/version = \"$new_version\"/" "$version_file"

    # Update the version in setup.cfg
    sed -i "s/version = $current_version/version = $new_version/" "$setup_file"

    echo "$new_version"
}

# Step 2: Clean the dist directory and rebuild the package
rebuild_package() {
    python3 -m pip install --upgrade build twine
    rm -rf dist/*
    python3 -m build
}

# Step 3: Upload the new version
upload_package() {
    python3 -m twine upload dist/*
}

# Step 4: Verify by installing the specific version
verify_package() {
    local new_version=$1
    echo "Execute this command after a minute to verify the new version $new_version: pip3 install --upgrade md2ltx"
}

echo "Incrementing version..."
new_version=$(increment_version)

echo "Rebuilding package..."
rebuild_package

echo "Uploading package..."
upload_package

echo "Verifying package..."
verify_package "$new_version"

