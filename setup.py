from setuptools import find_packages, setup

name = "build_py_project"
version = "0.0.1"

with open("requirements.txt", "r") as f:
    requirements = f.read().strip().split("\n")


setup(
    name=name,
    version=version,
    author="Ryan Ozelie",
    author_email="ryan.ozelie@gmail.com",
    description="",
    packages_dir={},
    packages=find_packages(".", exclude="tests"),
    classifiers=[
        "Programming Language :: Python :: 3.7.4",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7.4',
    include_package_data=True,
    zip_safe=True,
    install_requires=requirements,
)
