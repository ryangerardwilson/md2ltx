import shutil
import subprocess
import re
from pathlib import Path

def update_help_string():
    help_lib_file = Path("constants.py")
    readme_file = Path("README.md")

    # Read the README contents
    with readme_file.open("r", encoding="utf-8") as f:
        readme_content = f.read()

    # Read the string_lib.py, update its content, and write it back
    with help_lib_file.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    new_content = []
    inside_help_string_block = False

    for line in lines:
        if not inside_help_string_block:
            new_content.append(line)

        if re.match(r'^help_string = r"""', line):
            inside_help_string_block = True
            new_content.append('help_string = r"""\n')
            new_content.append(readme_content)
            new_content.append('"""\n')
            continue

        if inside_help_string_block and re.match(r'^"""', line):
            inside_help_string_block = False
            continue

    # Write the updated content back to string_lib.py
    with help_lib_file.open("w", encoding="utf-8") as f:
        f.writelines(new_content)

    print("constants.py updated with latest README.md content.")

def rebuild_package():
    subprocess.run(["python3", "-m", "pip", "install", "--upgrade", "build"], check=True)
    shutil.rmtree("dist", ignore_errors=True)
    subprocess.run(["python3", "-m", "build"], check=True)

def uninstall_local_library():
    package_name = None
    with open("pyproject.toml", "r", encoding="utf-8") as f:
        for line in f:
            match = re.match(r'^name\s*=\s*"(.*)"', line)
            if match:
                package_name = match.group(1)
                break
    if package_name:
        subprocess.run(["pip3", "uninstall", "-y", package_name], check=True)

def install_local_version():
    subprocess.run(["pip3", "install", "."], check=True)

def main():
    print("Updating help_string in string_lib.py from README.md...")
    update_help_string()

    print("Rebuilding package...")
    rebuild_package()

    print("Uninstalling local library...")
    uninstall_local_library()

    print("Installing local version...")
    install_local_version()

    print("The local version of the package has been reinstalled.")

if __name__ == "__main__":
    main()

