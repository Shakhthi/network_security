from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    libraries = []
    try:
        with open('requirements.txt', "r") as file:
            raw_libraries = file.readlines()

            for lib in raw_libraries:
                lib = lib.strip()
                if lib and lib != "-e .":
                    libraries.append(lib)
    except FileNotFoundError:
        print("requirements.txt not found")
    return libraries 

setup(
    name = "Network-security",
    version = "0.0.1",
    author = "MK",
    author_email = "sakthikaliappan7797@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements()
)
