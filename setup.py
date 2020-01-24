#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

with open("requirements.txt") as requirements_file:
    requirements = requirements_file.read()

# requirements = ["numpy", ]

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest>=3"]

setup(
    author="Axel Schmidt",
    author_email="schmidt.axel.91@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="This packages provides methodes for calculating fiber-reinforced materials.",
    install_requires=requirements,
    license="MIT license",
    long_description_content_type="text/x-rst",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="clt_py",
    name="clt_py",
    packages=find_packages(include=["clt_py", "clt_py.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/axelschmidt91/clt_py",
    version="0.0.4",
    zip_safe=False,
)
