import os
import subprocess
import zipfile
import sys
import shutil

def create_directory(name):
    if not os.path.exists(name):
        os.makedirs(name)

def clear_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def install_packages(packages, install_path, architecture):
    if architecture == 'arm64':
        for package in packages:
            subprocess.check_call([
                'docker', 'run', '--rm', '--platform', 'linux/arm64', 
                '-v', f"{os.getcwd()}:/app", '-w', '/app', 'python:3.9', 
                'bash', '-c', f"pip install {package} -t {install_path}"
            ])
    else:
        for package in packages:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '-t', install_path, '--only-binary=:all:'])

def create_zip(source_path, zip_name):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(source_path):
            for file in files:
                full_path = os.path.join(root, file)
                zipf.write(full_path, os.path.relpath(full_path, source_path))

def main():
    zip_name = input("Enter the name of the zip file (don't include .zip in the name): ")
    architecture = input("Enter the architecture (x86_64 or arm64): ")
    packages = []
    while True:
        package = input("Enter a package (or press Enter to finish): ")
        if not package:
            break
        packages.append(package)

    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    base_path = os.path.join(os.getcwd(), 'files', 'python', 'lib', f'python{python_version}', 'site-packages')
    zip_path = os.path.join(os.getcwd(), 'layers_zips')

    clear_directory('files')
    create_directory(base_path)
    create_directory(zip_path)
    install_packages(packages, base_path, architecture)
    create_zip('files/python', os.path.join(zip_path, f'{zip_name}.zip'))

    print(f"'{zip_name}.zip' file created successfully.")

if __name__ == "__main__":
    main()
