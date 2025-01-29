import re
import subprocess
import os
from shutil import rmtree


def update_help_string():
    help_lib_file = "src/md2ltx/lib/constants.py"
    readme_file = "README.md"

    with open(readme_file, 'r') as rf:
        readme_content = rf.read()

    with open(help_lib_file, 'r') as hf:
        lines = hf.readlines()

    with open(help_lib_file, 'w') as hf:
        skip = False
        for line in lines:
            if line.strip() == 'help_string = r"""':
                hf.write('help_string = r"""\n')
                hf.write(readme_content)
                hf.write('"""\n')
                skip = True
            elif skip and line.strip() == '"""':
                skip = False
            elif not skip:
                hf.write(line)

    print("constants.py updated with latest README.md content.")


def increment_version():
    version_file = "pyproject.toml"
    setup_file = "setup.cfg"

    # Read pyproject.toml
    with open(version_file, 'r') as vf:
        lines = vf.readlines()

    # Find and modify version line
    for i, line in enumerate(lines):
        if 'version = "' in line:
            current_version = re.search(r'\d+\.\d+\.\d+', line).group(0)
            version_parts = list(map(int, current_version.split('.')))
            version_parts[2] += 1  # Increment the patch version
            new_version = '.'.join(map(str, version_parts))
            lines[i] = f'version = "{new_version}"\n'
            break

    # Write back to pyproject.toml
    with open(version_file, 'w') as vf:
        vf.writelines(lines)

    # Read setup.cfg
    with open(setup_file, 'r') as sf:
        content = sf.read()

    # Modify version line
    content = re.sub(r'version = \d+\.\d+\.\d+', f'version = {new_version}', content)

    # Write back to setup.cfg
    with open(setup_file, 'w') as sf:
        sf.write(content)

    print(new_version)
    return new_version


def rebuild_package():
    subprocess.run(['python3', '-m', 'pip', 'install', '--upgrade', 'build', 'twine'], check=True)
    rmtree('dist/', ignore_errors=True)
    os.makedirs('dist/', exist_ok=True)
    subprocess.run(['python3', '-m', 'build'], check=True)


def upload_package():
    subprocess.run(['python3', '-m', 'twine', 'upload', 'dist/*'], check=True)


def verify_package(new_version):
    print(f"Execute this command after a minute to verify the new version {new_version}: pip3 install --upgrade md2ltx")


def main():
    print("Updating help string...")
    update_help_string()

    print("Incrementing version...")
    new_version = increment_version()

    print("Rebuilding package...")
    rebuild_package()

    print("Uploading package...")
    upload_package()

    print("Verifying package...")
    verify_package(new_version)


if __name__ == "__main__":
    main()
