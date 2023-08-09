#!/usr/bin/env python

from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="killeengeo",
    version="0.0.1",
    description="2D and 3D geometry in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Benjamin D. Killeen",
    author_email="killeen@jhu.edu",
    url="https://killeengeo.readthedocs.io/en/latest/",
    python_requires=">=3.10",
    install_requires=[
        "numpy",
        "scipy",
    ],
    packages=find_packages(),
    package_dir={"": "src"},
)
