#!/usr/bin/env python

import re
import setuptools

version = "0.0.1"

with open("README.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="splashclient",
    version=version,
    author="yubang",
    author_email="yubang93@gmail.com",
    description="splash简单客户端",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yubang/splashclient",
    install_requires=[
        'requests>=2.20.0',
    ],
    packages=setuptools.find_packages(exclude=("test")),
    classifiers=(
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6"
    ),
    exclude_package_data={'': ["test.py", ]},
)